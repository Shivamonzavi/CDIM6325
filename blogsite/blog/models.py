from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


# Create your models here.
class Post(models.Model):

    # Define Status Choices
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    # Model Fields
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, 
        unique_for_date="publish"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,  # Use Status.choices instead of Status
        default=Status.DRAFT
    )

    # Custom Manager
    class PublishedManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

    # Model Managers
    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager for published posts

    # Meta Options
    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"])
        ]

    # String Representation
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug]
        )
