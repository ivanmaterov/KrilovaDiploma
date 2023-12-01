from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Base user model."""

    middle_name = CharField(
        verbose_name=_('Middle name'),
        max_length=150,
        blank=True,
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self) -> str:
        return self.username

    @property
    def full_name(self) -> str:
        return ' '.join(filter(
            lambda x: x,
            [self.first_name, self.middle_name, self.last_name],
        ))
