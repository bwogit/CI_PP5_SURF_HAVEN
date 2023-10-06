# 3rd Party imports:
from phonenumber_field.modelfields import PhoneNumberField
# Internal imports
from django.db import models
from django.contrib.auth.models import User


# lesson times
lesson_times = (
    ('09:00', '09:00'),
    ('10:00', '10:00'),
    ('11:00', '11:00'),
    ('11:30', '11:30'),
    ('12:00', '12:00'),
    ('13:00', '13:00'),
    ('14:00', '14:00'),
    ('15:10', '15:10'),
    ('16:00', '16:00'),
    ('16:30', '16:30'),
)


# Status options for lesson time bookings
status_options = (
    ('Lesson Time Confirmed', 'Lesson Time Confirmed'),
    ('Lesson Time Rejected', 'Lesson Time Rejected'),
    ('Lesson Time Expired', 'Lesson Time Expired'),
)


class School(models.Model):
    """
    A class to create a surf school.

    """
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=200, unique=True, default='',)
    location = models.CharField(max_length=200)
    description = models.TextField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='school_images/',
                              null=True, blank=True)

    class Meta:
        ordering = ['school_name']

    def __str__(self):
        return self.school_name


class Booking(models.Model):
    """
    A class to create a booking for a surf lesson.
    """
    booking_id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    requested_date = models.DateField()
    requested_time = models.CharField(max_length=25, choices=lesson_times,
                                      default='12:00')
    school = models.ForeignKey(School, on_delete=models.CASCADE,
                               related_name="surf_school_name")
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=254, default="")
    phone = PhoneNumberField(null=True)
    status = models.CharField(max_length=25, choices=status_options,
                              default='Lesson Confirmed')
    surfers = (
        (1, "1 surfer"),
        (2, "2 surfers"),
        (3, "3 surfers"),
        (4, "4 surfers"),
        )
    surfer_count = models.IntegerField(choices=surfers, default=1)

    class Meta:
        ordering = ['-requested_time']
        unique_together = ('requested_date', 'requested_time', 'school')

    def __str__(self):
        return f"Booking {self.booking_id} - {self.status}"
