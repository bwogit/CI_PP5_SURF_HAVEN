# 3rd Party imports
from .forms import ContactForm
# Internal imports
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect


class ContactUser(View):
    """
    A view that allows authenticated users to access the contact form.
    When accessed, the form is pre-filled with the user's email and name.
    When the form is submitted, the message is saved and message is displayed.
    """
    template_name = 'contact/contact.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        initial_data = {'email': user.email,
                        'name': user.username} if user.is_authenticated else {}
        contact_form = ContactForm(initial=initial_data)
        return render(request, self.template_name,
                      {'contact_form': contact_form})

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact_form.save()
            messages.success(request, "Message submitted. Thank you!")
            # Redirect the user to the success page
            return render(request, 'contact/success.html')
        return render(request, self.template_name,
                      {'contact_form': contact_form})
