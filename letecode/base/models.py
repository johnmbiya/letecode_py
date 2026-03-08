from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

@register_setting
class NavigationSettings(BaseGenericSetting):
    linkedin_url = models.URLField(verbose_name="LinkedIn URL", blank=True)
    github_url = models.URLField(verbose_name="GitHub URL", blank=True)
    whatsapp_url = models.URLField(verbose_name="WhatsApp URL", blank=True)
    tiktok_url = models.URLField(verbose_name="Tiktok URL", blank=True)
    facebook_url = models.URLField(verbose_name="Facebook URL", blank=True)
    x_url = models.URLField(verbose_name="X URL", blank=True)

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("linkedin_url"),
                FieldPanel("github_url"),
                FieldPanel("whatsapp_url"),
                FieldPanel("tiktok_url"),
                FieldPanel("facebook_url"),
                FieldPanel("x_url"),
            ],
            "Social Settings"
        )
    ]

