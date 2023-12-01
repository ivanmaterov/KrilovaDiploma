from collections.abc import Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class AccessControl(models.Model):
    """Модель для таблицы `AccessControl` (Контроль доступа).
    
    Содержит сведения о компьютерах и устройствах. 
    
    """

    computer_name = models.CharField(
        max_length=256,
        verbose_name='Имя ПК',
        help_text='Имя компьютера',
    )
    username = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Пользователь',
        help_text='Имя пользователя',
    )
    device_display_name = models.CharField(
        max_length=512,
        blank=True,
        verbose_name='Отображаемое имя устройства',
        help_text='Отображаемое имя устройства',
    )
    device_system_name = models.CharField(
        max_length=256,
        verbose_name='Системное имя устройства',
        help_text='Системное имя устройства',
    )
    device_serial_id = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='Серийный №',
        help_text='Серийный номер устройства',
    )
    soi_id = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='№ заявки СОУ',
        help_text='Номер заявки СОУ',
    )
    sadd_id = models.CharField(
        max_length=256,
        blank=True,
        verbose_name='№ заявки САДД',
        help_text='Номер заявки САДД',
    )
    
    class StatusChoices(models.TextChoices):
        """Статусы для контроля доступа.

        PROHIBITED - компьютер взаимодействует с устройством без разрешения.
            Отсутствуют заявки СОУ И САДД.
        IN_PROGRESS - заявка на предоставление доступа в процессе
        GRANTED - доступ к устройству разрешен

        """
        PROHIBITED = 'prohibited', _('prohibited')
        IN_PROGRESS = 'in_progress', _('In progress')
        GRANTED = 'correct', _('Correct')
    
    status = models.CharField(
        verbose_name='Статус',
        help_text='Статус контроля доступа',
        choices=StatusChoices.choices,
        default=StatusChoices.GRANTED,
        max_length=12,
    )
    comment = models.TextField(
        blank=True,
        verbose_name='Комментарий',
        help_text='Комментарий к заявке',
    )
    
    class Meta:
        verbose_name = 'Контроль доступа'

    def __repr__(self) -> str:
        return (
            f'{self.computer_name}:{self.device_display_name} ({self.status})'
        )

    def clean(self) -> None:
        fields_values = {
            'soi_id': self.soi_id,
            'sadd_id': self.sadd_id,
        }
        is_all_fields_filled = all(fields_values.values())
        is_any_field_filled = any(fields_values.values())

        if is_any_field_filled and not is_all_fields_filled:
            empty_request_field = list(filter(
                lambda item: not bool(item[1]),
                fields_values.items(),
            ))[0][0]
            raise ValidationError(
                {empty_request_field: 'Заполните поле'},
                code='invalid',
            )
        
        return super().clean()
