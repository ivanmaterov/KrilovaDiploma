from import_export.formats.base_formats import CSV


UNKNOWN_HEADER = ''


class AccessControlCSVFormat(CSV):
    HEADERS = (
        'computer_name',
        'access',
        'device_display_name',
        UNKNOWN_HEADER,
        'producer',
        'device_serial_id',
        'username',
        UNKNOWN_HEADER,
        'device_system_name',
    )
    DELIMITER = '#'

    def create_dataset(self, in_stream, **kwargs):
        dataset = super().create_dataset(
            in_stream,
            delimiter=self.DELIMITER,
            headers=False,
            **kwargs,
        )
        dataset.headers = self.HEADERS
        return dataset
