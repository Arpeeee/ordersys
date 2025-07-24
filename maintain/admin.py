from django.contrib import admin
from .models import Mission, MissionMaintain, Maintain, QualityTest
# Register your models here.

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    list_per_page = 10

class MissionMaintainInline(admin.StackedInline):
    model = MissionMaintain
    extra = 0
    classes = ('collapse',)

@admin.register(Maintain)
class MaintainAdmin(admin.ModelAdmin):
    list_display = ('machine', 'created_at', 'created_by')
    list_filter = ('machine', 'created_at')
    search_fields = ('machine__sn', 'machine__name')
    list_per_page = 10
    inlines = [MissionMaintainInline]

@admin.register(QualityTest)
class QualityTestAdmin(admin.ModelAdmin):
    list_display = ('machine', 'name', 'created_at')
    list_filter = ('machine',)
    search_fields = ('machine__sn', 'machine__name', 'name')
    list_per_page = 10
    fieldsets = (
        ('基本資訊', {'fields': ('machine', 'name', 'description', 'file0', 'created_by')}),
        ('第一校正', {'fields': (('temp1', 'temp2', 'temp3'),)}),
        ('校正後', {'fields': (('temp4', 'temp5', 'temp6'),)}),
    )