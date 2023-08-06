from aldryn_forms.cms_plugins import Field
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from .fields import HoneypotField
from .widgets import HoneypotInput


class HoneypotCaptchaPlugin(Field):
    name = _("Honeypot Captcha")
    parent_classes = ["FormPlugin", "EmailNotificationForm"]  # allow to use inside forms only
    allow_children = False  # do not allow use other children

    form_field = HoneypotField
    form_field_widget = HoneypotInput

    form_field_enabled_options = []
    fieldset_general_fields = []
    fieldset_advanced_fields = []


plugin_pool.register_plugin(HoneypotCaptchaPlugin)
