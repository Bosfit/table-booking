from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class RestaurantTable(models.Model):
    """
    Simple table model to show a relationship between data types.
    """

    name = models.CharField(max_length=50, unique=True)
    seats = models.PositiveIntegerField(default=2)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.seats} seats)"


class Booking(models.Model):
    """
    Very simple booking model for a restaurant.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    table = models.ForeignKey(
        RestaurantTable,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookings",
    )
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

        # if a table is selected, guests should fit that table
        if self.table and self.guests and self.guests > self.table.seats:
            raise ValidationError("Guests exceed the number of seats for this table.")

        # We use this queryset to avoid checking against this same booking
        # when the user edits an existing record.
        same_slot_bookings = Booking.objects.filter(
            booking_date=self.booking_date,
            booking_time=self.booking_time,
        ).exclude(pk=self.pk)

        # Stop double-booking the same table at the same date and time.
        if self.table and same_slot_bookings.filter(table=self.table).exists():
            raise ValidationError(
                "This table is already booked for that date and time. "
                "Please choose another table or time."
            )

        # If no table is selected, we keep a simple safety limit for each slot.
        # This keeps the booking list realistic and easy for beginners to follow.
        max_unassigned_bookings_per_slot = 5
        if not self.table:
            unassigned_in_slot = same_slot_bookings.filter(table__isnull=True).count()
            if unassigned_in_slot >= max_unassigned_bookings_per_slot:
                raise ValidationError(
                    "This time slot is full for unassigned tables. "
                    "Please pick a table or choose another time."
                )

