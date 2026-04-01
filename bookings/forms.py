from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    """
    Simple form for creating and editing bookings.
    """

    TIME_SLOT_CHOICES = [
        ("12:00", "12:00"),
        ("12:30", "12:30"),
        ("13:00", "13:00"),
        ("13:30", "13:30"),
        ("14:00", "14:00"),
        ("17:00", "17:00"),
        ("17:30", "17:30"),
        ("18:00", "18:00"),
        ("18:30", "18:30"),
        ("19:00", "19:00"),
        ("19:30", "19:30"),
        ("20:00", "20:00"),
        ("20:30", "20:30"),
        ("21:00", "21:00"),
    ]

    booking_date = forms.DateField(
        input_formats=["%Y-%m-%d"],
        widget=forms.DateInput(
            attrs={"type": "date", "lang": "en-GB"},
            format="%Y-%m-%d",
        ),
    )
    booking_time = forms.TimeField(
        input_formats=["%H:%M"],
        widget=forms.Select(choices=TIME_SLOT_CHOICES),
    )

    class Meta:
        model = Booking
        fields = [
            "name",
            "email",
            "phone",
            "booking_date",
            "booking_time",
            "table",
            "guests",
            "special_request",
        ]

