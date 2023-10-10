from django.test import TestCase
from django.contrib.auth.models import User
from .models import School, Booking


class BookingModelTest(TestCase):
    def setUp(self):
        # Create a sample user
        self.user = User.objects.create_user(
            username='sample_user',
            password='sample_password'
        )

        # Create a sample school object
        self.school = School.objects.create(
            school_name="Sample School",
            slug="sample-school",
            location="Sample Location",
            description="Sample Description",
            available=True,
        )

        # Create a sample booking object
        self.booking = Booking.objects.create(
            requested_date="2023-10-10",
            requested_time="12:00",
            school=self.school,
            user=self.user,  # Assign the user to the booking
            name="Sample User",
            email="sample@email.com",
            phone="+1234567890",
            status="Lesson Time Confirmed",
            surfer_count=2,
        )

    def test_booking_str(self):
        # Test the __str__ method of the Booking model
        expected_str = f"Booking {self.booking.booking_id} - Lesson Time Confirmed"
        self.assertEqual(str(self.booking), expected_str)

    def test_booking_school_relation(self):
        # Test the relation between Booking and School
        self.assertEqual(self.booking.school, self.school)
