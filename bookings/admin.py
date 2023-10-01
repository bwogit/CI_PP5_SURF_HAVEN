from django.contrib import admin
from .models import School, Booking


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    summernote_fields = ('description',)
    list_display = ('school_name', 'location', 'description', 'is_available')
    list_filter = ('location',)
    search_fields = ('school_name', 'location', 'description')
    prepopulated_fields = {'slug': ('school_name',)}

    def is_available(self, obj):
        return obj.available

    is_available.boolean = True  # 
    is_available.short_description = 'Available'  # 


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'created_date', 'requested_date', 'requested_time', 'school', 'user', 'status')
    list_filter = ('requested_date', 'school', 'user', 'status')
    search_fields = ('booking_id', 'user__username')  # Example: Searching by user's username

    actions = ['confirm_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(status='Booking Confirmed')
    confirm_bookings.short_description = "Confirm selected bookings"
