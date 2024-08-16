from django.contrib.postgres.fields.array import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from solo.models import SingletonModel


def validate_unique_array(value):
    if len(value) != len(set(value)):
        raise ValidationError(
            _('Элементы в поле должны быть уникальными. Найдены дубликаты.')
        )


class TelegramBotConfiguration(SingletonModel):
    token = models.CharField(_('Token'), max_length=255, default='5706572197:AAHvVB1DQhlHSDI9kxuriZzpPUq8slsjrH8')
    admins = ArrayField(base_field=models.BigIntegerField(), verbose_name=_('Admins'), default=list,
                        validators=[validate_unique_array])
    secret_key = models.CharField(_('Secret key'), max_length=255, default='secret_key')
    bot_url = models.URLField(_('Bot URL'), max_length=255, default='https://t.me/learning_njrBot')

    class Meta:
        verbose_name = _('Telegram bot configuration')
        verbose_name_plural = _('Telegram bot configuration')

    def __str__(self):
        return f'{self.bot_url} | {self.token}'
