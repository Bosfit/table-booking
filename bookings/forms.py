from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Simple form for creating and editing bookings.
    """

    class Meta:
        model = Booking
        fields = [
            "name",
            "email",
            "phone",
            "booking_date",
            "booking_time",
            "guests",
            "special_request",
        ]

