from django.db import migrations, models
import apps.site_settings.models


DEFAULT_STEPS = [
    {"key": "welcome", "label": "Welcome"},
    {"key": "word", "label": "A Word for You"},
    {"key": "prayer", "label": "Guided Prayer"},
    {"key": "devotional", "label": "Devotional"},
    {"key": "next-steps", "label": "Next Steps"},
]

DEFAULT_WELCOME_SECTION = {
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

DEFAULT_WORD_SECTION = {
    "title": "A Word for You",
    "description": "Before anything else, we want you to hear this.",
    "video_embed_url": "https://www.youtube.com/embed/zHPaFDRZMUo?rel=0",
    "verse_text": "He heals the brokenhearted and binds up their wounds.",
    "verse_reference": "Psalm 147:3",
    "previous_button_text": "Previous",
    "next_button_text": "Continue",
}

DEFAULT_PRAYER_SECTION = {
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

DEFAULT_DEVOTIONAL_SECTION = {
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

DEFAULT_NEXT_STEPS_SECTION = {
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

DEFAULT_CRISIS_SECTION = {
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


def migrate_legacy_word_section(apps, schema_editor):
    JourneyContent = apps.get_model('site_settings', 'JourneyContent')

    for content in JourneyContent.objects.all():
        word_section = dict(DEFAULT_WORD_SECTION)
        word_section.update(
            {
                "title": content.title,
                "description": content.description,
                "video_embed_url": content.video_embed_url,
            }
        )
        content.word_section = word_section
        content.save(update_fields=['word_section', 'updated_at'])


class Migration(migrations.Migration):
    dependencies = [
        ('site_settings', '0002_journeycontent'),
    ]

    operations = [
        migrations.AddField(
            model_name='journeycontent',
            name='page_title',
            field=models.CharField(default='Hopeful Beginning', max_length=255),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='page_subtitle',
            field=models.TextField(default='A journey toward hope, one step at a time.'),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='steps',
            field=models.JSONField(default=apps.site_settings.models.default_journey_steps),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='welcome_section',
            field=models.JSONField(default=apps.site_settings.models.default_journey_welcome_section),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='word_section',
            field=models.JSONField(default=apps.site_settings.models.default_journey_word_section),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='prayer_section',
            field=models.JSONField(default=apps.site_settings.models.default_journey_prayer_section),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='devotional_section',
            field=models.JSONField(default=apps.site_settings.models.default_journey_devotional_section),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='next_steps_section',
            field=models.JSONField(default=apps.site_settings.models.default_journey_next_steps_section),
        ),
        migrations.AddField(
            model_name='journeycontent',
            name='crisis_section',
            field=models.JSONField(default=apps.site_settings.models.default_journey_crisis_section),
        ),
        migrations.RunPython(migrate_legacy_word_section, migrations.RunPython.noop),
    ]
