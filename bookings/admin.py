from django.contrib import admin

from .models import Booking, RestaurantTable


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ("name", "seats")
    search_fields = ("name",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "booking_date", "booking_time", "table", "guests", "email")
    list_filter = ("booking_date", "table")
    search_fields = ("name", "email")
