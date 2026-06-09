from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from django.forms import BaseInlineFormSet
from .models import Circuit, CircuitUpgrade, Machine, TemperatureSensor, MachineComponent
from maintain.models import Maintain


class TemperatureSensorFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        type_values = [1, 2, 3, 4]
        for i, form in enumerate(self.forms):
            if i < len(type_values) and not form.instance.pk:
                form.initial['type'] = type_values[i]


class MachineComponentFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        component_types = ['IC', 'FM', 'DM', 'DR', 'EF', 'SM', 'SR', 'CF']
        for i, form in enumerate(self.forms):
            if i < len(component_types) and not form.instance.pk:
                form.initial['component_type'] = component_types[i]
                form.fields['component_type'].disabled = True


@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('number', 'description', 'version', 'color', 'created_at')
    list_filter = ('color',)
    search_fields = ('number', 'description')
    list_per_page = 10


@admin.register(CircuitUpgrade)
class CircuitUpgradeAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'updated_at', 'updated_by')
    list_filter = (('circuit', RelatedOnlyFieldListFilter),)
    list_select_related = ('circuit', 'updated_by')
    search_fields = ('circuit__number', 'circuit__description')
    list_per_page = 10


class TemperatureSensorInline(admin.StackedInline):
    model = TemperatureSensor
    fields = ('name', 'type', 'parameter_file')
    formset = TemperatureSensorFormSet
    extra = 4
    max_num = 4
    classes = ('collapse',)


class MachineComponentInline(admin.TabularInline):
    model = MachineComponent
    fieldsets = (
        ('種類', {'fields': ('component_type',)}),
        ('型號與序號', {'fields': ('model_number', 'serial_number', 'status',)}),
    )
    formset = MachineComponentFormSet
    extra = 8
    can_delete = True
    classes = ('collapse',)


class MaintainInline(admin.StackedInline):
    model = Maintain
    extra = 0
    classes = ('collapse',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('machine', 'created_by')


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('sn', 'name', 'typeof', 'generation', 'number', 'circuit', 'remote_id', 'mac', 'created_at', 'updated_at')
    list_filter = ('typeof', 'generation', ('circuit', RelatedOnlyFieldListFilter))
    list_select_related = ('circuit',)
    search_fields = ('sn', 'name', 'remote_id', 'mac')
    list_per_page = 10
    inlines = [TemperatureSensorInline, MachineComponentInline, MaintainInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本資訊', {'fields': (('sn', 'name', 'number'), ('typeof', 'generation'), 'circuit', 'description')}),
        ('遠端資訊', {'fields': (('remote_id', 'mac'),)}),
        ('建立時間', {'fields': ('created_at', 'updated_at', 'created_by')}),
        ('保固資訊', {'fields': (('warranty_start_date', 'warranty_end_date'), 'warranty_status')}),
    )


@admin.register(TemperatureSensor)
class TemperatureSensorAdmin(admin.ModelAdmin):
    list_display = ('machine', 'name', 'type', 'created_at')
    list_filter = (('machine', RelatedOnlyFieldListFilter), 'type')
    list_select_related = ('machine',)
    search_fields = ('machine__sn', 'machine__name', 'name')
    list_per_page = 10


@admin.register(MachineComponent)
class MachineComponentAdmin(admin.ModelAdmin):
    list_display = ('machine', 'component_type', 'model_number', 'serial_number', 'status', 'created_at')
    list_filter = (('machine', RelatedOnlyFieldListFilter), 'component_type', 'status')
    list_select_related = ('machine',)
    search_fields = ('machine__sn', 'machine__name', 'model_number', 'serial_number')
    list_per_page = 10
