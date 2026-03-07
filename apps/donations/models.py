from django.db import models
import uuid

class Donation(models.Model):
    TYPE_CHOICES = [
        ('ONE_TIME', 'One-Time'),
        ('MONTHLY', 'Monthly'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donation_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='ONE_TIME')
    date = models.DateField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} - ${self.amount} ({self.donation_type})"
