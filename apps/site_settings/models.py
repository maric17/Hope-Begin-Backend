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
