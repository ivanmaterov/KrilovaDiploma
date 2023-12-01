from typing import Any
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from apps.access_control.models import AccessControl
from apps.access_control.forms import (
    CreateAccessControlForm,
    UpdateAccessControlForm,
    AccessControlImportForm,
)
from import_export.admin import ImportExportMixinBase
from import_export.mixins import BaseImportMixin
from apps.access_control.resources import AccessControlResource
from import_export.tmp_storages import TempFolderStorage
from django.template.response import TemplateResponse
from apps.access_control.resources.format import AccessControlCSVFormat
from django.http import HttpRequest
from django.core.files.uploadedfile import InMemoryUploadedFile
from import_export.results import Result


class ImportAccessControlView(
    BaseImportMixin,
    ImportExportMixinBase,
    TemplateView,
):
    """View для импорта данных."""
    import_template_name = template_name = 'pages/import_access_control.html'
    form_class = AccessControlImportForm
    resource_class = AccessControlResource
    tmp_storage_class = TempFolderStorage
    model = AccessControl
    input_format = AccessControlCSVFormat

    def post(self, request: HttpRequest, *args, **kwargs) -> TemplateResponse:
        """Выполнить импорт на POST запрос."""
        context = self.get_context_data()
        import_form = context['form']

        if import_form.is_valid():
            import_file = import_form.cleaned_data["import_file"]
            result = self.import_resource(import_file)
            context['result'] = result

        return TemplateResponse(
            request,
            self.import_template_name,
            context,
        )

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Получить контекст с формой для импорта ресурса."""
        return {'form': self.get_import_form(self.request)}

    def get_import_form_kwargs(self, request: HttpRequest) -> dict[str, Any]:
        """Получить параметры для импорта из объекта `request`."""
        return {
            'data': request.POST or None,
            'files': request.FILES or None,
        }

    def get_import_form(
        self,
        request: HttpRequest,
        *args,
        **kwargs,
    ) -> AccessControlImportForm:
        return self.form_class(
            import_formats=self.get_import_formats(),
            **self.get_import_form_kwargs(request),
        )

    def import_resource(
        self,
        import_file: InMemoryUploadedFile,
        *args,
        **kwargs,
    ) -> Result:
        """Импортировать ресурс."""
        input_format = self.input_format()
        tmp_storage = self.write_to_tmp_storage(import_file, input_format)
        import_file.tmp_storage_name = tmp_storage.name

        data = tmp_storage.read()
        dataset = input_format.create_dataset(data)

        resource = self.resource_class()

        return resource.import_data(
            dataset,
            raise_errors=False,
            rollback_on_validation_errors=True,
            file_name=import_file.name,
        )

    def write_to_tmp_storage(
        self,
        import_file: InMemoryUploadedFile,
        input_format: AccessControlCSVFormat,
    ) -> TempFolderStorage:
        """Инициализировать и записать данные в temporary storage."""
        tmp_storage = self.tmp_storage_class(
            encoding='utf-8',
            read_mode=input_format.get_read_mode()
        )
        data = bytes()
        for chunk in import_file.chunks():
            data += chunk

        tmp_storage.save(data)
        return tmp_storage


class AccessControlDeleteView(DeleteView):
    model = AccessControl
    success_url = '/'


class AccessControlCreateView(CreateView):
    model = AccessControl
    form_class = CreateAccessControlForm
    template_name = 'pages/access_control.html'
    success_url = '/'


class AccessControlUpdateView(UpdateView):
    model = AccessControl
    form_class = UpdateAccessControlForm
    template_name = 'pages/access_control.html'
    success_url = '/'


class AccessControlListView(ListView):
    model = AccessControl
    context_object_name = 'access_control_items'
    template_name = 'pages/access_control_list.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data['column_names_mapping'] = {
            field.attname: field.verbose_name
            for field in AccessControl._meta.fields
        }
        context_data['statuses'] = AccessControl.StatusChoices.values
        return context_data
