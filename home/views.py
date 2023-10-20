# 3rd Imports
from django.shortcuts import render


def home(request):
    """
    A view to display the homepage
    """
    return render(request, 'home/index.html')
