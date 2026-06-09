from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter
from .models import Mission, MissionMaintain, Maintain, QualityTest


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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('mission', 'maintain__machine')


@admin.register(Maintain)
class MaintainAdmin(admin.ModelAdmin):
    list_display = ('machine', 'created_at', 'created_by')
    list_filter = (('machine', RelatedOnlyFieldListFilter), 'created_at')
    list_select_related = ('machine', 'created_by')
    search_fields = ('machine__sn', 'machine__name')
    list_per_page = 10
    inlines = [MissionMaintainInline]


@admin.register(QualityTest)
class QualityTestAdmin(admin.ModelAdmin):
    list_display = ('machine', 'name', 'created_at')
    list_filter = (('machine', RelatedOnlyFieldListFilter),)
    list_select_related = ('machine',)
    search_fields = ('machine__sn', 'machine__name', 'name')
    list_per_page = 10
    fieldsets = (
        ('基本資訊', {'fields': ('machine', 'name', 'description', 'file0', 'created_by')}),
        ('第一校正', {'fields': (('temp1', 'temp2', 'temp3'),)}),
        ('校正後', {'fields': (('temp4', 'temp5', 'temp6'),)}),
    )
