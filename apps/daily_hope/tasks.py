from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from .models import HopeJourney
from .content import GET_HOPE_DROPS_CONTENT

@shared_task
def send_daily_hope_emails():
    # Find all active subscribers
    active_subscribers = HopeJourney.objects.filter(is_active=True)
    
    for subscriber in active_subscribers:
        day = subscriber.current_day
        content = GET_HOPE_DROPS_CONTENT.get(day)
        
        if not content:
            # If no content for this day, we might have finished the 21 days
            if day > 21:
                subscriber.is_active = False
                subscriber.finished_at = timezone.now()
                subscriber.save()
            continue
            
        # Send email
        subject = f"Daily Hope Drop - Day {day}: {content['title']}"
        from_email = 'noreply@hopebegins.org'
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
            msg.send()
            
            # Increment day or finish
            if day >= 21:
                subscriber.is_active = False
                subscriber.finished_at = timezone.now()
            else:
                subscriber.current_day += 1
            
            subscriber.save()
            
        except Exception as e:
            # Log error (could use celery logger)
            print(f"Error sending email to {subscriber.email}: {e}")

@shared_task
def send_welcome_email(subscriber_id):
    try:
        subscriber = HopeJourney.objects.get(id=subscriber_id)
        # You could send a separate welcome email here or just wait for the first beat
        # For now, let's just trigger the first day email immediately if you want
        pass
    except HopeJourney.DoesNotExist:
        pass
