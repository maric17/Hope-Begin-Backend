from django.db import models


def default_journey_steps():
    return [
        {"key": "welcome", "label": "Welcome"},
        {"key": "word", "label": "A Word for You"},
        {"key": "prayer", "label": "Guided Prayer"},
        {"key": "devotional", "label": "Devotional"},
        {"key": "next-steps", "label": "Next Steps"},
    ]


def default_journey_welcome_section():
    return {
        "title": "Your Hopeful Beginning",
        "body": (
            "It's okay to feel this way. You're not broken - you're here, and that matters.\n"
            "We've prepared a short journey for you. Take it at your own pace."
        ),
        "expectations_title": "What to expect:",
        "expectations": [
            "A short video message of encouragement",
            "A guided prayer to help you exhale",
            "A devotional about the true meaning of hope",
            "Gentle next steps when you're ready",
        ],
        "button_text": "Continue",
    }


def default_journey_word_section():
    return {
        "title": "A Word for You",
        "description": "Before anything else, we want you to hear this.",
        "video_embed_url": "https://www.youtube.com/embed/zHPaFDRZMUo?rel=0",
        "verse_text": "He heals the brokenhearted and binds up their wounds.",
        "verse_reference": "Psalm 147:3",
        "previous_button_text": "Previous",
        "next_button_text": "Continue",
    }


def default_journey_prayer_section():
    return {
        "title": "Guided Prayer",
        "description": "Let's take a moment together. Follow each step at your own pace.",
        "steps": [
            {
                "title": "Be Still",
                "text": (
                    "Let's take a moment together. Quiet your thoughts for just a second. "
                    "You are in a safe place."
                ),
            },
            {
                "title": "Acknowledge",
                "text": (
                    "Acknowledge the heavy feelings without judgment. It's okay to not be "
                    "okay right now. Breath in slowly..."
                ),
            },
            {
                "title": "Release",
                "text": (
                    "I release my fear, my pain, and my worry into Your hands. I don't "
                    "have to carry this alone. You said to cast my burdens on You - so "
                    "here they are."
                ),
            },
            {
                "title": "Receive",
                "text": (
                    "I receive Your peace that passes understanding. I receive Your love "
                    "that never fails. I receive the hope that You are working all things "
                    "together for my good."
                ),
            },
            {
                "title": "Rest",
                "text": (
                    "I rest in You, Lord. Not because everything is okay, but because You "
                    "are okay, and You are with me. Amen."
                ),
            },
        ],
        "back_button_text": "Back",
        "next_button_text": "Next",
        "final_button_text": "Continue to Devotional",
    }


def default_journey_devotional_section():
    return {
        "title": "What is Hope?",
        "subtitle": "A short devotional to anchor your heart.",
        "content_cards": [
            (
                "Hope is not the absence of pain - it's the belief that pain is not "
                "the final word. It's that quiet voice inside saying, \"There's more "
                "ahead for you.\""
            ),
            (
                "The Bible describes hope as an anchor for the soul - firm and secure. "
                "Not because life is easy, but because the One who holds tomorrow also "
                "holds you today. Even when you can't see it, hope is there."
            ),
        ],
        "verse_text": "We have this hope as an anchor for the soul, firm and secure.",
        "verse_reference": "Hebrews 6:19",
        "good_news_title": "The Good News",
        "good_news_body": (
            "You are loved - not because of what you've done, but because of who you are. "
            "God sent His Son, Jesus, so that you would never have to walk through "
            "darkness alone. He meets you right here, right now, exactly as you are."
        ),
        "reflection_title": "Reflect on this:",
        "reflection_prompt": (
            "What would it look like to believe - even just a little - that tomorrow "
            "could be different?"
        ),
        "previous_button_text": "Previous",
        "next_button_text": "Continue",
    }


def default_journey_next_steps_section():
    return {
        "title": "Your Next Step",
        "description": (
            "You've made it through this journey, and that matters more than you know. "
            "Whenever you're ready, here are some ways to keep going."
        ),
        "actions": [
            {"title": "I Need Someone to Pray for Me", "href": "/prayers", "icon": "heart"},
            {"title": "Start Daily Hope Drops", "href": "/daily-hope", "icon": "mail"},
            {"title": "Talk to Hope AI", "href": "/hope-ai", "icon": "message-square"},
            {"title": "Listen to a HopeCast", "href": "/hopecasts", "icon": "headphones"},
        ],
        "home_link_text": "Back to Home",
    }


def default_journey_crisis_section():
    return {
        "heading": "If you're in crisis, please reach out:",
        "contacts": [
            {
                "title": "National Center for Mental Health 24/7 Crisis Hotline",
                "icon": "heart",
                "lines": [
                    {"label": "Landline (nationwide):", "value": "1553"},
                    {"label": "Mobile:", "value": "0917-899-8727 / 0966-351-4518"},
                ],
            },
            {
                "title": "Hopeline Philippines Emotional Crisis Support",
                "icon": "message-square",
                "lines": [
                    {"label": "Call:", "value": "(02) 8804-4673"},
                    {"label": "Mobile:", "value": "0917-558-4673 / 0918-873-4673"},
                ],
            },
            {
                "title": "In Touch Community Services Crisis Line (24/7)",
                "icon": "heart",
                "lines": [
                    {"label": "Call:", "value": "(02) 8893-7603"},
                    {"label": "Mobile:", "value": "0917-800-1123"},
                ],
            },
        ],
    }


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
    page_title = models.CharField(max_length=255, default="Hopeful Beginning")
    page_subtitle = models.TextField(default="A journey toward hope, one step at a time.")
    steps = models.JSONField(default=default_journey_steps)
    welcome_section = models.JSONField(default=default_journey_welcome_section)
    word_section = models.JSONField(default=default_journey_word_section)
    prayer_section = models.JSONField(default=default_journey_prayer_section)
    devotional_section = models.JSONField(default=default_journey_devotional_section)
    next_steps_section = models.JSONField(default=default_journey_next_steps_section)
    crisis_section = models.JSONField(default=default_journey_crisis_section)
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
