#!/usr/bin/env python
import os
import django
import logging
from datetime import datetime
import sys

# Setup logging to print to console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('daily_hope_test')

def run_test():
    """Test script to manually trigger and verify daily hope emails"""
    logger.info("Setting up Django environment...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')
    django.setup()

    try:
        from apps.daily_hope.tasks import send_daily_hope_emails
        from apps.daily_hope.models import HopeJourney
    except ImportError as e:
        logger.error(f"Failed to import necessary modules: {e}")
        sys.exit(1)

    logger.info(f"Current server time: {datetime.now()}")
    
    # 1. Check current state
    logger.info("Checking for active subscribers...")
    active_subscribers = HopeJourney.objects.filter(is_active=True)
    count = active_subscribers.count()
    logger.info(f"Found {count} active subscribers.")
    
    if count == 0:
        logger.warning("No active subscribers found. Exiting test.")
        logger.info("If you want to test, sign up a test user first.")
        sys.exit(0)

    logger.info("\nCurrent State:")
    for sub in active_subscribers:
        logger.info(f" - {sub.email}: Current Day = {sub.current_day}")

    # 2. Run the task
    logger.info("\n--- EXECUTING send_daily_hope_emails SYNCHRONOUSLY ---")
    try:
        send_daily_hope_emails()
        logger.info("--- EXECUTION COMPLETED ---")
    except Exception as e:
        logger.error(f"--- EXECUTION FAILED: {e} ---", exc_info=True)
        sys.exit(1)

    # 3. Verify changes
    logger.info("\nVerifying State After Execution:")
    updated_subscribers = HopeJourney.objects.filter(id__in=[s.id for s in active_subscribers])
    all_success = True
    
    for old_sub in active_subscribers:
        new_sub = updated_subscribers.get(id=old_sub.id)
        
        # Check if day number increased
        if not new_sub.is_active:
             logger.info(f" - ✅ {new_sub.email} completed the 21-day journey and is now inactive.")
        elif new_sub.current_day > old_sub.current_day:
            logger.info(f" - ✅ SUCCESS: {new_sub.email} advanced from Day {old_sub.current_day} to Day {new_sub.current_day}.")
        else:
            logger.error(f" - ❌ FAILURE: {new_sub.email} is still on Day {new_sub.current_day}. Email likely failed to send.")
            all_success = False

    if all_success:
        logger.info("\n✅ All active subscribers processed successfully.")
    else:
        logger.warning("\n⚠️ Some subscribers were not successfully processed. Check logs for details.")

if __name__ == "__main__":
    run_test()
