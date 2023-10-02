# Imports
# 3rd party:
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.core.paginator import Paginator
import datetime
# Internal:
from .models import School, Booking
from .forms import BookingForm
from products.models import Product, Category


# 


class AllSchools(generic.ListView):
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
            # 'postings': postings
        }

        return render(
            request,
            'bookings/school_list.html',
            context
        )


class SchoolDetail(View):
    template_name = 'bookings/school_detail.html'
    success_message = 'Booking has been made.'

    def get(self, request, slug, *args, **kwargs):
        school = get_object_or_404(School.objects.filter(available=1), slug=slug)
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
            'booking_form': booking_form
        }

        return render(request, self.template_name, context)


# Show all of the user's current bookings.
# Bookings that have a date in the past will be marked as expired.
# Once a booking is expired, the user cannot modify or cancel it.


class BookingList(generic.ListView):
    """
   
    """
    model = Booking
    queryset = Booking.objects.filter().order_by('-created_date')
    template_name = 'booking_list.html'
    paginated_by = 4

    def get(self, request, *args, **kwargs):

        booking = Booking.objects.all()
        paginator = Paginator(School.objects.filter(user=request.user), 4)
        page = request.GET.get('page')
        booking_page = paginator.get_page(page)
        today = datetime.datetime.now().date()

        for date in booking:
            if date.requested_date < today:
                date.status = 'Booking is Expired'

        if request.user.is_authenticated:
            bookings = Booking.objects.filter(user=request.user)
            return render(
                request,
                'bookings/booking_list.html',
                {
                    'booking': booking,
                    'bookings': bookings,
                    'booking_page': booking_page})
        else:
            return redirect('accounts/login.html')


# Opens the booking editing page and form, 
# allowing the user to make any desired changes to the booking details and save the updates.


class EditBooking(SuccessMessageMixin, UpdateView):
    """
    
    """
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/edit_booking.html'
    success_message = 'Booking has been updated.'

    def get_success_url(self, **kwargs):
        return reverse('booking_list')


# Deletes the selected booking the user wishes to cancel

def cancel_booking(request, pk):
    """
    
    """
    booking = Booking.objects.get(pk=pk)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking has been cancelled")
        return redirect('booking_list')

    return render(
        request, 'bookings/cancel_booking.html', {'booking': booking})
