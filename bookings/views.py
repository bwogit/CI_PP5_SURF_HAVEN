# 3rd Party imports
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.contrib import messages
from django.urls import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
from datetime import datetime
from django.utils import timezone
# Internal Imports
from .models import School, Booking
from .forms import BookingForm
from products.models import Product, Category


class AllSchools(generic.ListView):
    """
    A class for listing all schools.
    """
    model = School
    queryset = School.objects.filter(available=1).order_by('school_name')
    template_name = 'school_list.html'
    paginated_by = 4

    def get(self, request, *args, **kwargs):
        """
        This view renders the list of all partner surfschools
        """
        schools = School.objects.all()
        queryset = School.objects.filter(available=1).order_by('school_name')
        paginator = Paginator(School.objects.all(), 4)
        page = request.GET.get('page')
        postings = paginator.get_page(page)
        products = Product.objects.all()
        categories_list = Category.objects.all()

        context = {
            'products': products,
            'categories_list': categories_list,
            'schools': postings,
            'postings': postings
        }

        return render(
            request,
            'bookings/school_list.html',
            context
        )


class SchoolDetail(View):
    """
    A class for giving a detailed view of the schools.
    """
    template_name = 'bookings/school_detail.html'
    success_message = 'Booking has been made.'

    def get(self, request, slug, *args, **kwargs):
        school = get_object_or_404(School.objects.
                                   filter(available=1), slug=slug)
        products = Product.objects.all()
        categories_list = Category.objects.all()

        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'email': request.user.email,
                'school': school,
            }

        booking_form = BookingForm(initial=initial_data)

        context = {
            'products': products,
            'categories_list': categories_list,
            'school': school,
            'booking_form': booking_form,
        }

        return render(request, self.template_name, context)

    def post(self, request, slug, *args, **kwargs):
        queryset = School.objects.filter(available=1)
        school_instance = get_object_or_404(queryset, slug=slug)
        booking_form = BookingForm(data=request.POST)
        template_name = 'bookings/school_detail.html'

        context = {
            'school': school_instance,
            'booking_form': booking_form,
            'slug': slug
        }

        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.school = school_instance
            booking.save()
            messages.success(
                request, "Booking successful")
            return render(request, 'bookings/booking_created.html')
        return render(
            request, 'bookings/school_detail.html', context)


class BookingList(LoginRequiredMixin, generic.ListView):
    """
    Show all of the user's current bookings.
    Bookings that have a date in the past will be marked as expired.
    Once a booking is expired, the user cannot modify or cancel it.
    """
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # Filter bookings for the authenticated user
            return Booking.objects.filter(user=user).order_by('-created_date')
        return Booking.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_page = context['page_obj']

        today = timezone.now().date()  # Use timezone-aware datetime

        # Update the status of bookings based on the requested_date
        for booking in booking_page:
            if booking.requested_date < today:
                booking.status = 'Booking is Expired'

        context['booking_page'] = booking_page
        return context


class EditBooking(SuccessMessageMixin, UpdateView):
    """
    A class to Open the booking page and form
    to allow user to make any desired changes to the
    booking details and save the updates
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/edit_booking.html'
    success_message = 'Booking has been updated.'
    categories_list = Category.objects.all()

    def get_success_url(self, **kwargs):
        return reverse('booking_list')


def cancel_booking(request, pk):
    """
    A class to Deletes the selected booking
    """
    booking = Booking.objects.get(pk=pk)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking has been cancelled")
        return redirect('booking_list')

    return render(
        request, 'bookings/cancel_booking.html', {'booking': booking})
