from django.contrib import admin
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contact model.
    Displays contact messages in the admin panel.
    """
    list_display = ('name', 'email', 'created_date')
    list_filter = ('user', 'name', 'email', 'phone', 'created_date')
    search_fields = ('email',)
    readonly_fields = ('created_date',)

    fieldsets = (
        ('User Information', {
            'fields': ('user', 'name', 'email', 'phone'),
        }),
        ('Message', {
            'fields': ('message',),
        }),
        ('Timestamps', {
            'fields': ('created_date',),
        }),
    )

    ordering = ('-created_date',)