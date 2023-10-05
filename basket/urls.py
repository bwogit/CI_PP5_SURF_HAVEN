# 3rd party Imports
from django.contrib import admin
from django.urls import path
# Internal Imports
from . import views


# url for the home page
urlpatterns = [
    path('', views.view_basket, name="view_basket"),
    path('add/<item_id>/', views.add_to_basket, name='add_to_basket'),
    path('update/<item_id>/', views.update_basket, name='update_basket'),
    path('remove/<item_id>/', views.remove_from_basket, name='remove_from_basket'),
]
