from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from .models import HopeJourney
from .content import GET_HOPE_DROPS_CONTENT
import logging

logger = logging.getLogger(__name__)

def send_subscriber_email_logic(subscriber):
    """
    Internal logic to send a specific day's email to a subscriber
    and increment their progress.
    """
    day = subscriber.current_day
    logger.info(f"Processing Daily Hope email for {subscriber.email} (Day {day})")
    content = GET_HOPE_DROPS_CONTENT.get(day)
    
    if not content:
        # If no content for this day, we might have finished the 21nd day
        if day > 21:
            subscriber.is_active = False
            subscriber.finished_at = timezone.now()
            subscriber.save()
        return False
        
    from django.conf import settings
    
    # Send email
    subject = f"Daily Hope Drop - Day {day}: {content['title']}"
    from_email = settings.DEFAULT_FROM_EMAIL
    to = subscriber.email
    
    text_content = f"Hi {subscriber.first_name},\n\nDay {day}: {content['title']}\n\n{content['description']}\n\nVerse of the Day:\n{content['verse']}"
    
    # HTML content with image and verse
    html_content = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #eee; padding: 20px; border-radius: 10px;">
                <h2 style="color: #6b634d;">Day {day}: {content['title']}</h2>
                <p>Hi {subscriber.first_name},</p>
                <p>{content['description']}</p>
                
                <div style="background-color: #f9f8f4; padding: 15px; border-left: 4px solid #b4c392; margin: 20px 0;">
                    <p style="font-style: italic; margin: 0;">"{content['verse']}"</p>
                </div>

                <div style="margin-top: 20px; text-align: center;">
                    <img src="{content['image_url']}" alt="Daily Hope Day {day}" style="max-width: 100%; height: auto; border-radius: 8px;">
                </div>
                
                <hr style="border: 0; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="font-size: 0.8em; color: #888; text-align: center;">
                    You are receiving this because you signed up for the 21-day Hope Journey at Hope Begins.
                </p>
            </div>
        </body>
    </html>
    """
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    
    try:
        logger.info(f"Attempting to send Daily Hope email (Day {day}) to {subscriber.email}")
        msg.send()
        logger.info(f"Successfully sent Daily Hope email (Day {day}) to {subscriber.email}")
        
        # Increment day or finish AFTER successful send
        if day >= 21:
            logger.info(f"Subscriber {subscriber.email} completed the 21-day journey")
            subscriber.is_active = False
            subscriber.finished_at = timezone.now()
        else:
            subscriber.current_day += 1
        
        subscriber.save()
        return True
        
    except Exception as e:
        # Log error
        logger.error(f"Error sending Daily Hope email to {subscriber.email}: {e}", exc_info=True)
        return False

@shared_task
def send_daily_hope_emails():
    logger.info("Task send_daily_hope_emails triggered")
    # Find all active subscribers
    active_subscribers = HopeJourney.objects.filter(is_active=True)
    
    logger.info(f"Found {active_subscribers.count()} active subscribers for Daily Hope emails")
    for subscriber in active_subscribers:
        send_subscriber_email_logic(subscriber)

@shared_task
def send_welcome_and_day_one(subscriber_id):
    """
    Called immediately upon signup.
    Sends Day 1 email and sets subscriber ready for Day 2 on next schedule.
    """
    logger.info(f"Task send_welcome_and_day_one triggered for subscriber_id={subscriber_id}")
    try:
        subscriber = HopeJourney.objects.get(id=subscriber_id)
        if subscriber.current_day == 1:
            send_subscriber_email_logic(subscriber)
            logger.info(f"Processed Day 1 email for subscriber_id={subscriber_id}")
    except HopeJourney.DoesNotExist:
        logger.warning(f"Subscriber with id={subscriber_id} does not exist. Cannot send Day 1 email.")
        pass
