# Imports
# 3rd party:
from django.urls import path
# Internal:
# from .views import ContactUser
from contact import views

urlpatterns = [
    path('contact/', views.ContactUser.as_view(), name='contact'),
]