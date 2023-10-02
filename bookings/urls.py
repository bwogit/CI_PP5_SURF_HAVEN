# Imports
from django.urls import path
# Internal:
from bookings import views

# Urls for all the pages in the bookings app
urlpatterns = [
    path('bookings/', views.AllSchools.as_view(), name='school_list'),
    path('schools_detail/<slug:slug>/', views.SchoolDetail.as_view(), name='school_detail'),
#     path('confirmed', views.Confirmed.as_view(), name='confirmed'),
#     path('booking_list', views.BookingList.as_view(), name='booking_list'),
#     path('edit_booking/<int:pk>',
#          views.EditBooking.as_view(), name='edit_booking'),
#     path('cancel_booking/<int:pk>',
#          views.cancel_booking, name='cancel_booking'),
]
