from django.db import models
from wagtail.admin.panels import (
    FieldPanel,
    MultiFieldPanel,
    PublishingPanel
)
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    register_setting,
)

from wagtail.fields import RichTextField
from wagtail.models import (
    DraftStateMixin,
    PreviewableMixin,
    RevisionMixin,
    TranslatableMixin
)

from wagtail.snippets.models import register_snippet

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


@register_snippet
class FooterText(
    DraftStateMixin,
    RevisionMixin,
    PreviewableMixin,
    TranslatableMixin,
    models.Model
):
    body = RichTextField()

    panels = [
        FieldPanel("body"),
        PublishingPanel(),
    ]

    def __str__(self):
        return "Footer text"
    
    def get_preview_template(self, request, mode_name):
        return "base.html"
    
    def get_preview_context(self, request, mode_name):
        return {"footer_text": self.body}
    
    class Meta(TranslatableMixin.Meta):
        verbose_name_plural = "Footer Text"
