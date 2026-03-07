from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from wagtail import blocks
from wagtail.admin.panels import MultiFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds import blocks as embed_blocks
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page, Orderable
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtailcodeblock.blocks import CodeBlock

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    def get_context(self, request):
      context = super().get_context(request)
      # Get list of blog pages that are descendants of this page ordered by most recent first
      blogpages = self.get_children().live().order_by("-first_published_at")
      context["blogpages"] = blogpages
      return context

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

    authors = ParentalManyToManyField('blog.Author', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(["date", "authors"], heading="Blog information"),
        "intro", "body", "gallery_images"
    ]

# BlogPageGalleryImage is a child of BlogPage, and is used to store images related to a blog post
class BlogPageGalleryImage(Orderable):
  page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name="gallery_images")
  image = models.ForeignKey(
    "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
  )
  caption = models.CharField(blank=True, max_length=250)

  panels = [
    "image",
    "caption",
  ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = ["name", "author_image"]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'
