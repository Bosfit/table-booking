from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import BookingForm
from .models import Booking


def home(request):
    """
    Simple home page.
    """
    return render(request, "bookings/home.html")


def booking_list(request):
    """
    Show all bookings.
    """
    bookings = Booking.objects.all()
    return render(request, "bookings/booking_list.html", {"bookings": bookings})


def booking_create(request):
    """
    Create a new booking.
    """
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # simple extra safety check for past dates
            if booking.booking_date < timezone.localdate():
                messages.error(request, "This booking date is invalid.")
            else:
                booking.save()
                messages.success(request, "Booking created successfully.")
                return redirect("booking_list")
    else:
        form = BookingForm()

    return render(request, "bookings/booking_form.html", {"form": form, "title": "Book a table"})


def booking_update(request, pk):
    """
    Edit an existing booking.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save(commit=False)

            if updated_booking.booking_date < timezone.localdate():
                messages.error(request, "This booking date is invalid.")
            else:
                updated_booking.save()
                messages.success(request, "Booking updated successfully.")
                return redirect("booking_list")
    else:
        form = BookingForm(instance=booking)

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "title": "Edit booking"},
    )


def booking_delete(request, pk):
    """
    Confirm and delete a booking.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
        return redirect("booking_list")

    return render(request, "bookings/booking_confirm_delete.html", {"booking": booking})


def menu(request):
    """
    Very simple menu page.
    """
    items = [
        {"name": "Margherita Pizza", "description": "Classic pizza with tomato and mozzarella.", "price": "£9.50"},
        {"name": "Pasta Alfredo", "description": "Creamy pasta with parmesan.", "price": "£11.00"},
        {"name": "House Salad", "description": "Fresh mixed salad with house dressing.", "price": "£6.00"},
    ]
    return render(request, "bookings/menu.html", {"items": items})

