import os

from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import CarMaker, CarModel, Car, Owner, Provider, Spare, Order
from .ocr_module import *
from DPL.settings import MEDIA_ROOT

admin.site.site_header = "Wings for the car"
admin.site.site_title = "Admin Panel"


@admin.action(description='Set the status to FINISHED')
def status_to_finished(modeladmin, request, queryset):
    queryset.update(status='FINISHED')


@admin.action(description='Set the status to CANCELED')
def status_to_cancelled(modeladmin, request, queryset):
    queryset.update(status='CANCELED')


@admin.action(description='Set the status to IN_WORK')
def status_to_in_work(modeladmin, request, queryset):
    queryset.update(status='IN_WORK')


@admin.action(description='Set the status to FOR_ISSUE')
def status_to_for_issue(modeladmin, request, queryset):
    queryset.update(status='FOR_ISSUE')


class CarMakerAdmin(admin.ModelAdmin):
    # list_display = ['car_maker']
    search_fields = ['car_maker__startswith']


class CarModelAdmin(admin.ModelAdmin):
    images = Car.images
    list_display = ['car_maker', 'car_model']
    ordering = ['car_maker', 'car_model']
    list_filter = ['car_maker']
    list_per_page = 20


class CarAdmin(admin.ModelAdmin):

    list_display = ['model', 'owner', 'vin', 'number_plate', 'year', 'color', 'images']
    readonly_fields = ['sts']

    @admin.display(description="Image")
    def sts(self, car: Car):
        if car.images:
            return mark_safe(f"<img src='{car.images.url}' width=600>")
        return "without image"

    fieldsets = [
        (
            'Vehicle registration certificate (CTC)',
            {
                'classes': ['wide'],
                'fields': ['images', 'sts'],

            },
        ),
        (

            'Comments',
            {
                'classes': ['collapse'],
                'description': 'Data from OCR',
                'fields': ['comments'],
            },
        ),
        (
            'Car identifiers',

            {
                'fields': ['model', ('vin', 'number_plate'), ('year', 'color'), ],
            }
        ),
        (
            'Owner',
            {
                'classes': ['wide'],
                'fields': ['owner'],
            }

        )
    ]


admin.site.register(Car, CarAdmin)
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMaker, CarMakerAdmin)
admin.site.register(Owner)
admin.site.register(Order)
admin.site.register(Provider)
admin.site.register(Spare)
