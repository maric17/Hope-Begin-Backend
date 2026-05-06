from django.db import models
import uuid

class HopeStory(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255, blank=True, null=True)
    testimonial = models.TextField()
    photo = models.ImageField(upload_to='hope_stories/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Hope Stories"

    def __str__(self):
        return f"{self.full_name} - {self.status}"
