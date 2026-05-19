from django.contrib import admin
from .models import PopoutSettings, PopoutItem

@admin.register(PopoutSettings)
class PopoutSettingsAdmin(admin.ModelAdmin):
    list_display = ('is_enabled', 'interval_seconds')
    
    def has_add_permission(self, request):
        # Only allow one instance of settings
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(PopoutItem)
class PopoutItemAdmin(admin.ModelAdmin):
    list_display = ('message', 'button_text', 'link', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('message', 'button_text')
