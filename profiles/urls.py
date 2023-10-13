# 3rd Party Imports
from django.urls import path
# Internal Imports
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history,
         name='order_history'),
]
