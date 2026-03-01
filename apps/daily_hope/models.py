from django.db import models
import uuid

class HopeJourney(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    current_day = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Hope Journey"
        verbose_name_plural = "Hope Journeys"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Day {self.current_day}"
