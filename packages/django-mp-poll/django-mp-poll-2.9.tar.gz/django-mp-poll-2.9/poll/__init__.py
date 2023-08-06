
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PollConfig(AppConfig):
    name = 'poll'
    verbose_name = _("Poll")


default_app_config = 'poll.PollConfig'
