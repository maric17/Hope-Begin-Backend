from django.db import models
import uuid

class HopecastCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Hopecast Categories"

    def __str__(self):
        return self.name

class Hopecast(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255, blank=True, null=True)
    verse = models.TextField(blank=True, null=True)
    mp4_link = models.URLField(max_length=500)
    categories = models.ManyToManyField(HopecastCategory, related_name='hopecasts')
    play_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
