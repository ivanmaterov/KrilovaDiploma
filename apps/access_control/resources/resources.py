from import_export import resources
from apps.access_control.models import AccessControl


class AccessControlResource(resources.ModelResource):
    class Meta:
        model = AccessControl
        import_id_fields = (
            'computer_name',
            'device_system_name',
        )
        fields = (
            'computer_name',
            'username',
            'device_display_name',
            'device_system_name',
            'device_serial_id',
        )

    def before_save_instance(self, instance, using_transactions, dry_run):
        access_request_fields = [instance.soi_id, instance.sadd_id]

        is_any_field_filled = any(access_request_fields)
        is_all_fields_filled = all(access_request_fields)

        if instance._state.adding:
            instance.status = AccessControl.StatusChoices.PROHIBITED
        else:
            if not is_any_field_filled:
                instance.status = AccessControl.StatusChoices.PROHIBITED

            if is_all_fields_filled:
                instance.status = AccessControl.StatusChoices.GRANTED

        return super().before_save_instance(
            instance,
            using_transactions,
            dry_run,
        )
