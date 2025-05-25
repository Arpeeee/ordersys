from django.contrib import admin
from .models import Customer, Contact, Order
# Register your models here.

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'geo', 'address2', 'is_active', 'is_agent', 'tax_number', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_agent')
    search_fields = ('name', 'address', 'address2')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本資訊', {'fields': (('name', 'address'), 'geo', 'address2', 'is_active', 'is_agent', 'tax_number')}),
        ('建立時間', {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 10

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'is_active', 'customer', 'created_at', 'updated_at')
    list_filter = ('is_active', 'customer')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本資訊', {'fields': (('name', 'customer', 'is_active'), ('email', 'email2'), ('phone', 'phone2'))}),
        ('建立時間', {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order_number', 'order_date', 'location', 'created_at', 'updated_at')
    list_filter = ('customer','machine')
    search_fields = ('order_number', 'customer__name')
    list_per_page = 10
