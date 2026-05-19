from django.db import models

class PopoutSettings(models.Model):
    is_enabled = models.BooleanField(default=True)
    interval_seconds = models.IntegerField(default=15)

    class Meta:
        verbose_name = "Popout Settings"
        verbose_name_plural = "Popout Settings"

    def __str__(self):
        return "Popout Settings"

    def save(self, *args, **kwargs):
        if not self.pk and PopoutSettings.objects.exists():
            return
        return super().save(*args, **kwargs)

class PopoutItem(models.Model):
    message = models.CharField(max_length=255)
    button_text = models.CharField(max_length=50)
    link = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class JourneyContent(models.Model):
    title = models.CharField(max_length=255, default="A Word for You")
    description = models.TextField(default="Before anything else, we want you to hear this.")
    video_embed_url = models.URLField(default="https://www.youtube.com/embed/zHPaFDRZMUo?rel=0")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Journey Content"
        verbose_name_plural = "Journey Content"

    def __str__(self):
        return "Journey Content Settings"

    def save(self, *args, **kwargs):
        if not self.pk and JourneyContent.objects.exists():
            # Ensure only one instance exists
            return
        return super().save(*args, **kwargs)
