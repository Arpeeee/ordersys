from django.contrib import admin
from .models import Mission, MissionMaintain, Maintain
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