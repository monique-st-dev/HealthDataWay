from django.contrib import admin
from .models import DirectionType, CardiologyRecord, EndocrinologyRecord
from common.admin_mixins import ReadOnlyAdminMixin

@admin.register(DirectionType)
class DirectionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(CardiologyRecord)
class CardiologyRecordAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('patient', 'systolic', 'diastolic', 'pulse', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('patient__email', 'systolic', 'diastolic', 'pulse')
    readonly_fields = ('created_at',)


@admin.register(EndocrinologyRecord)
class EndocrinologyRecordAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    list_display = ('patient', 'blood_sugar', 'date', 'time')
    list_filter = ('date',)
    search_fields = ('patient__email', 'blood_sugar')
    readonly_fields = ('created_at',)
