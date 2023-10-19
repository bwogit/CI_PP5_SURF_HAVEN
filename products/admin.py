# 3rd Party Imports
from django.contrib import admin

# Internal
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'category',
        'name',
        'brand',
        'price',
        'rating',
        'image',
    )

    ordering = ('code',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
