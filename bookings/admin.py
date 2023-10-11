# 3rd party imports
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
# Internal imports
from .models import School, Booking


# SchoolAdmin class
@admin.register(School)
class SchoolAdmin(SummernoteModelAdmin):
    """
    Admin class for the School model.
    """

    summernote_fields = ('description',)
    list_display = ('school_name', 'location', 'description', 'is_available')
    list_filter = ('location',)
    search_fields = ('school_name', 'location', 'description')
    prepopulated_fields = {'slug': ('school_name',)}

    def is_available(self, obj):
        """
        Returns whether or not the school is available.
        """

        return obj.available

    is_available.boolean = True
    is_available.short_description = 'Available'


# BookingAdmin class
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin class for the Booking model.
    """

    list_display = ('booking_id', 'created_date', 'requested_date',
                    'requested_time', 'school', 'user', 'status')
    list_filter = ('requested_date', 'school', 'user', 'status')
    search_fields = ('booking_id', 'user__username')

    actions = ['confirm_bookings']

    def confirm_bookings(self, request, queryset):
        """
        Confirms the selected bookings.
        """

        queryset.update(status='Lesson Time Confirmed')

    confirm_bookings.short_description = "Confirm selected bookings"
