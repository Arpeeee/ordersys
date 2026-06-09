from django import forms
from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.contrib.gis.geos import Point
from .models import Customer, Contact, Order


class PointLatLngWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.NumberInput(attrs={
                'placeholder': '緯度 Latitude (e.g. 25.0330)',
                'step': 'any', 'style': 'width:200px; margin-right:8px',
            }),
            forms.NumberInput(attrs={
                'placeholder': '經度 Longitude (e.g. 121.5654)',
                'step': 'any', 'style': 'width:200px',
            }),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value and hasattr(value, 'y'):
            return [value.y, value.x]
        return [None, None]


class PointLatLngField(forms.MultiValueField):
    widget = PointLatLngWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.FloatField(required=False),
            forms.FloatField(required=False),
        )
        super().__init__(fields=fields, require_all_fields=False, *args, **kwargs)

    def compress(self, data_list):
        if data_list and len(data_list) == 2:
            lat, lng = data_list
            if lat is not None and lng is not None:
                return Point(float(lng), float(lat), srid=4326)
        return None


class CustomerForm(forms.ModelForm):
    geo = PointLatLngField(required=False, label='公司座標 (緯度, 經度)')

    class Meta:
        model = Customer
        fields = '__all__'


class OrderForm(forms.ModelForm):
    location_geo = PointLatLngField(required=False, label='地點座標 (緯度, 經度)')

    class Meta:
        model = Order
        fields = '__all__'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    form = CustomerForm
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
    list_filter = ('is_active', ('customer', RelatedOnlyFieldListFilter))
    list_select_related = ('customer',)
    search_fields = ('name', 'email', 'phone', 'customer__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本資訊', {'fields': (('name', 'customer', 'is_active'), ('email', 'email2'), ('phone', 'phone2'))}),
        ('建立時間', {'fields': ('created_at', 'updated_at')}),
    )
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    list_display = ('customer', 'order_number', 'order_date', 'location', 'created_at', 'updated_at')
    list_filter = (('customer', RelatedOnlyFieldListFilter), ('machine', RelatedOnlyFieldListFilter))
    list_select_related = ('customer', 'machine')
    search_fields = ('order_number', 'customer__name')
    list_per_page = 10


admin.site.site_header = 'GOGOLEE 機器維修保養系統'
admin.site.site_title = 'GOGOLEE 機器維修保養系統'
admin.site.index_title = 'GOGOLEE 機器維修保養系統'
