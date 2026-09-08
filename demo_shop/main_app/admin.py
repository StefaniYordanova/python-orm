from django.contrib import admin

# Register your models here.

from main_app.models import Customers

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'middle_name', 'last_name', 'email']
    list_filter = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    fieldsets = [
        ('Personal information', {
            'fields': ('first_name', 'middle_name', 'last_name', 'age', 'gender')
        }),
        ('Contacts', {
            'fields': ('phone_number', 'email')
        })
    ]
