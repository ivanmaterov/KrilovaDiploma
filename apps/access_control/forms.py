from typing import Any
from django.forms import ModelForm
from apps.access_control.models import AccessControl
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from import_export.forms import ImportForm


class AccessControlImportForm(ImportForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._init_helper()

    def _init_helper(self):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Импортировать таблицу доступов к устройствам',
                'import_file',
                'input_format',
            ),
            Submit(
                'submit',
                'Импортировать',
                css_class='btn btn-success',
            ),
            HTML(
                '<a class="btn btn-warning form-group" href="javascript:history.back()">Назад</a>',
            ),
        )
        


class CreateAccessControlForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._init_helper()

    def _init_helper(self):
        # See crispy forms layout configuration
        # https://django-crispy-forms.readthedocs.io/en/latest/layouts.html#layouts  # noqa
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Информация об устройствах',
                'computer_name',
                'username',
                'device_display_name',
                'device_system_name',
                'device_serial_id',
            ),
            Fieldset(
                'Заявки на доступ',
                'soi_id',
                'sadd_id',
                'comment',
            ),
            Submit(
                'submit',
                'Создать',
                css_class='button white',
            ),
        )

    class Meta:
        model = AccessControl
        fields = (
            'computer_name',
            'username',
            'device_display_name',
            'device_system_name',
            'device_serial_id',

            'soi_id',
            'sadd_id',
            'comment',
        )

    def save(self, commit: bool = True) -> AccessControl:
        """Проставить статусы перед созданием инстанца.

        Выставить статус или выбросить исключение в зависимости от состояния
        полей `soi_id` и `sadd_id`:
            * Если все поля заявок заполнены - статус "в процессе" (In progress)
            * Если все поля не заполнены - статус "запрещено" (Prohibited)

        """

        access_request_fields = [self.instance.soi_id, self.instance.sadd_id]
        is_all_fields_filled = all(access_request_fields)
        is_any_field_filled = any(access_request_fields)

        if is_all_fields_filled:
            self.instance.status = AccessControl.StatusChoices.IN_PROGRESS

        if not is_any_field_filled:
            self.instance.status = AccessControl.StatusChoices.PROHIBITED
        
        return super().save(commit)


class UpdateAccessControlForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        """Инициализировать поля в зависимости от состояния инстанца.
        
        * Если статус `разрешено` (Granted) - выключить поля `soi_id`, `sadd_id`,
            `status`
        * Если статус `в процессе` (In progess) - выключить поля `soi_id`,
            `sadd_id` и выставить допустимые значения для `status`
        
        """
        super().__init__(*args, **kwargs)

        is_granted = self.instance.status == AccessControl.StatusChoices.GRANTED
        is_in_progress = self.instance.status == AccessControl.StatusChoices.IN_PROGRESS

        self.fields['status'].disabled = True

        if is_granted or is_in_progress:
            self.fields['soi_id'].disabled = True
            self.fields['sadd_id'].disabled = True

        self._init_helper()
    
    def _init_helper(self):
        # See crispy forms layout configuration
        # https://django-crispy-forms.readthedocs.io/en/latest/layouts.html#layouts  # noqa
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Заявки на доступ',
                'soi_id',
                'sadd_id',
                'status',
                'comment',
            ),
            Submit(
                'submit',
                'Обновить',
                css_class='button white',
            ),
        )

    class Meta:
        model = AccessControl
        fields = (
            'soi_id',
            'sadd_id',
            'status',
            'comment',
        )
