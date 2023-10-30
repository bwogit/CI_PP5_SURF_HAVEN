# 3rd party imports
from crispy_forms.helper import FormHelper
from django import forms
from datetime import datetime
from phonenumber_field.formfields import PhoneNumberField
# Internal imports
from .models import Booking


class BookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    requested_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min':
                               datetime.now().date()}))

    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':
                             ('+353123456789')}))

    class Meta:
        model = Booking
        fields = (
            'name',
            'email',
            'phone',
            'school',
            'surfer_count',
            'requested_date',
            'requested_time',
        )
