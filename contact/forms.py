# 3rd Party Imports
from django import forms
from crispy_forms.helper import FormHelper
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError  # Import ValidationError

# Internal Imports
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    A form to collect contact information and message.
    from Contact model and provides validation.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)

    phone = PhoneNumberField(widget=forms.TextInput(
        attrs={'placeholder': ('+353123456789')}))

    class Meta:
        model = Contact
        fields = ['email', 'name', 'message', 'phone']

    def clean_email(self):
        """
        Custom validation for the 'email' field.
        """
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):
            raise ValidationError("Please use a valid example.com email address.")
        return email    
