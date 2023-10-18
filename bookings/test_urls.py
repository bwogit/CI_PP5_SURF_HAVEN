# 3rd Party Imports
from django.test import SimpleTestCase
from django.urls import reverse, resolve
# Internel Imports
from bookings.views import AllSchools,
SchoolDetail, BookingList, EditBooking, cancel_booking


class TestUrls(SimpleTestCase):
    def test_school_list_url_resolves(self):
        url = reverse('school_list')
        self.assertEqual(resolve(url).func.view_class, AllSchools)

    def test_school_detail_url_resolves(self):
        url = reverse('school_detail', kwargs={'slug': 'sample-slug'})
        self.assertEqual(resolve(url).func.view_class, SchoolDetail)

    def test_booking_list_url_resolves(self):
        url = reverse('booking_list')
        self.assertEqual(resolve(url).func.view_class, BookingList)

    def test_edit_booking_url_resolves(self):
        url = reverse('edit_booking', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, EditBooking)

    def test_cancel_booking_url_resolves(self):
        url = reverse('cancel_booking', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func, cancel_booking)
