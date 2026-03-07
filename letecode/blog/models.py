from django.db import models

from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds import blocks as embed_blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.search import index

from wagtailcodeblock.blocks import CodeBlock

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + ["intro"]


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("code", CodeBlock()),
            ("embed", embed_blocks.EmbedBlock()),
            ("heading", blocks.CharBlock(classname="full title")),
            ("quote", blocks.BlockQuoteBlock()),
            ("table", TableBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        "date",
        "intro",
        "body",
    ]
