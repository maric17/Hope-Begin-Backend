from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Prayer, PrayerResponse
from apps.users.tasks import send_prayer_encouragement_email
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Prayer)
def capture_old_status(sender, instance, **kwargs):
    try:
        old_instance = Prayer.objects.get(pk=instance.pk)
        instance._old_status = old_instance.status
    except Prayer.DoesNotExist:
        instance._old_status = None

@receiver(post_save, sender=Prayer)
def send_prayer_notification(sender, instance, created, **kwargs):
    # Check if status changed to COMPLETED
    old_status = getattr(instance, '_old_status', None)
    
    if instance.status == 'COMPLETED' and old_status != 'COMPLETED':
        logger.info(f"Prayer {instance.id} marked as COMPLETED. Sending notification email to {instance.email}.")
        
        # 1. Prepare email content
        subject = "HopeBegins - Someone prayed for you!"
        message = (
            f"Hello,\n\n"
            f"A Hope Carrier has just finished praying for your request: \"{instance.title}\".\n\n"
            f"Your prayer request was:\n"
            f"--------------------------------------------------\n"
            f"\"{instance.content}\"\n"
            f"--------------------------------------------------\n\n"
        )
        
        # 2. Look for the latest encouragement note (PrayerResponse)
        latest_response = PrayerResponse.objects.filter(prayer=instance).order_by('-created_at').first()
        if latest_response:
            message += (
                f"They shared a word of encouragement with you:\n"
                f"--------------------------------------------------\n"
                f"\"{latest_response.content}\"\n"
                f"--------------------------------------------------\n\n"
            )
            
        message += (
            "We are standing in agreement with you.\n\n"
            "Blessings,\n"
            "The Hope Begins Team"
        )
        
        # 3. Send email asynchronously using Celery
        send_prayer_encouragement_email.delay(instance.email, subject, message)
