# 3rd party imports:
from django.urls import path
# Internal imports
from contact import views

urlpatterns = [
    path('contact/', views.ContactUser.as_view(), name='contact'),
    path('success/', views.ContactUser.as_view(), name='success'),
]
