from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Booking(models.Model):
    """
    Very simple booking model for a restaurant.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    guests = models.PositiveIntegerField()
    special_request = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["booking_date", "booking_time"]

    def __str__(self) -> str:
        return f"{self.name} - {self.booking_date} {self.booking_time}"

    def clean(self) -> None:
        """
        Basic validation rules.

        We also do these in the form, but having them here keeps
        the rules close to the data.
        """

        # name cannot be empty (Django already checks this, but we keep it clear)
        if not self.name:
            raise ValidationError("Name cannot be empty.")

        # booking date cannot be in the past
        if self.booking_date:
            today = timezone.localdate()
            if self.booking_date < today:
                raise ValidationError("Booking date cannot be in the past.")

        # guests must be at least 1
        if self.guests is not None and self.guests < 1:
            raise ValidationError("Guests must be at least 1.")

