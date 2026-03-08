from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet

from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class HomePage(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Homepage image",
    )

    hero_title = models.CharField(
        blank=True,
        max_length=255,
        help_text="Write an introduction for the site"
    )
    hero_description = models.TextField(
        blank=True,
        max_length=500,
        help_text="Write an introduction for the site"
    )

    hero_about_cta = models.CharField(
        blank=True,
        verbose_name="About CTA",
        max_length=255,
        help_text="Text to display on About button",
    )

    hero_about_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="About link",
        help_text="Choose a page to link to for the About to Action",
    )

    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
                FieldPanel("hero_about_cta"),
                FieldPanel("hero_about_cta_link"),
            ],
            heading="Hero section"
        ),
        FieldPanel("body")
    ]

class About(Page):
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="About image",
    )

    hero_title = models.CharField(
        blank=True,
        max_length=255,
        help_text="Write an introduction for the page"
    )
    hero_description = models.TextField(
        blank=True,
        max_length=500,
        help_text="Write an introduction for the about page"
    )

    mission_body = RichTextField(blank=True)

    lead_image =  models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Lead profile",
    )

    lead_name = models.CharField(
        blank=True,
        max_length=255,
        help_text="Write the Lead's name"
    )

    lead_role = models.CharField(
        blank=True,
        max_length=255,
        help_text="Write the Lead's role"
    )

    counters = ParentalManyToManyField('home.StatCounter', blank=True)

    values_title = models.CharField(
        blank=True,
        max_length=255,
        help_text="Our values"
    )
    values_description = models.TextField(
        blank=True,
        max_length=500,
        help_text="Write an description"
    )
    values = ParentalManyToManyField('home.CommunityValue', blank=True)

    presence_body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_title"),
                FieldPanel("hero_description"),
            ],
            heading="Hero section"
        ),
        FieldPanel("mission_body"),
        MultiFieldPanel(
            [
                FieldPanel("lead_image"),
                FieldPanel("lead_name"),
                FieldPanel("lead_role"),
            ],
            heading="Lead section"
        ),
        FieldPanel("counters", widget=forms.CheckboxSelectMultiple),
        MultiFieldPanel(
            [
                FieldPanel("values_title"),
                FieldPanel("values_description"),
                FieldPanel("values", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Values section"
        ),
        FieldPanel("presence_body"),
    ]


class TermsPage(Page):
    date = models.DateField("Last updated")
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + ["date", "body"]



@register_snippet
class StatCounter(models.Model):
    label = models.CharField(max_length=100)
    value = models.CharField(max_length=10)

    panels = ["label", "value"]

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = 'Counters'

@register_snippet
class CommunityValue(models.Model):
    # TODO:add icon

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    panels = ["title", "description"]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Values'

