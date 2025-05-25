from django.contrib import admin
from .models import Circuit, CircuitUpgrade, Machine, TemperatureSensor, QualityTest
from maintain.models import Maintain
# Register your models here.

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    list_display = ('number', 'description', 'version', 'color', 'created_at')
    list_filter = ('color',)
    search_fields = ('number', 'description')
    list_per_page = 10

@admin.register(CircuitUpgrade)
class CircuitUpgradeAdmin(admin.ModelAdmin):
    list_display = ('circuit', 'updated_at', 'updated_by')
    list_filter = ('circuit',)
    search_fields = ('circuit__number', 'circuit__description')
    list_per_page = 10

class TemperatureSensorInline(admin.StackedInline):
    model = TemperatureSensor
    fields = ('name', 'type', 'parameter_file')
    extra=4
    classes = ('collapse',)

class QualityTestInline(admin.StackedInline):
    model = QualityTest
    extra = 0
    classes = ('collapse',)

class MaintainInline(admin.StackedInline):
    model = Maintain
    extra = 0
    classes = ('collapse',)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('sn', 'name', 'typeof', 'generation', 'number', 'circuit', 'remote_id', 'mac', 'created_at', 'updated_at')
    list_filter = ('typeof', 'generation', 'circuit')
    search_fields = ('sn', 'name', 'typeof', 'generation', 'number', 'circuit', 'remote_id', 'mac')
    list_per_page = 10
    inlines = [TemperatureSensorInline, QualityTestInline, MaintainInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('基本資訊', {'fields': (('sn', 'name','number'), ('typeof', 'generation') , 'circuit', )}),
        ('遠端資訊', {'fields': (('remote_id', 'mac'),)}),
        ('建立時間', {'fields': ('created_at', 'updated_at')}),
        # ('品質測試', {'fields': ('quality_test',)}),
    )

@admin.register(TemperatureSensor)
class TemperatureSensorAdmin(admin.ModelAdmin):
    list_display = ('machine', 'name', 'type', 'created_at')
    list_filter = ('machine', 'type')
    search_fields = ('machine__sn', 'machine__name', 'name')
    list_per_page = 10

@admin.register(QualityTest)
class QualityTestAdmin(admin.ModelAdmin):
    list_display = ('machine', 'name', 'created_at')
    list_filter = ('machine',)
    search_fields = ('machine__sn', 'machine__name', 'name')
    list_per_page = 10
