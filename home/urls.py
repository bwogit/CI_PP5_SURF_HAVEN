# 3rd Party imports
from django.contrib import admin
from django.urls import path

# Internal imports
from . import views

# URL for the home page
urlpatterns = [
    path('', views.home, name="home"),
]
