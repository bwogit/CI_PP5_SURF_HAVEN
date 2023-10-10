# 3rd party Imports
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import School  # 


class TestBookingsViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.school_list_url = reverse('school_list')
        self.school_detail_url = reverse(
            'school_detail',
            kwargs={'slug': 'test_school_1'}  #
        )
        self.booking_list_url = reverse('booking_list')

        # Create a test user (optional)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_all_schools_GET(self):
        response = self.client.get(self.school_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/school_list.html')

    def test_school_detail_GET(self):
        # Create a test school
        school = School.objects.create(
            school_name='Test School',
            slug='test_school_1'  # 
        )

        response = self.client.get(self.school_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/school_detail.html')

    def test_booking_list_GET(self):
        # Login the test user (optional)
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.booking_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bookings/booking_list.html')
