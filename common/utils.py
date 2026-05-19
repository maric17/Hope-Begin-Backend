import logging
import time

logger = logging.getLogger(__name__)

def validate_form_time(start_time_ms, min_seconds=3):
    """
    Validates that the form took at least min_seconds to submit.
    start_time_ms is the timestamp from the frontend in milliseconds.
    """
    if not start_time_ms:
        return False
        
    try:
        start_time = int(start_time_ms) / 1000.0
        current_time = time.time()
        duration = current_time - start_time
        
        # If duration is negative (clock skew) or too short, it's likely a bot
        if duration < min_seconds or duration > 3600: # Max 1 hour
            return False
        return True
    except (ValueError, TypeError):
        return False

def check_spam_keywords(text):
    """
    Checks if the text contains common spam/phishing keywords.
    """
    if not text:
        return False
        
    spam_keywords = [
        'crypto', 'bitcoin', 'ethereum', 'seo', 'marketing', 
        'click here', 'buy now', 'money back', 'win prize',
        'casino', 'porn', 'cheap', 'discount', 'viagra'
    ]
    
    text_lower = text.lower()
    for keyword in spam_keywords:
        if keyword in text_lower:
            return True
    return False
