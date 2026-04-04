from datetime import time, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Booking, RestaurantTable


class BookingModelValidationTests(TestCase):
    def setUp(self):
        self.table_two_seats = RestaurantTable.objects.create(name="Test table", seats=2)

    def test_booking_date_cannot_be_in_the_past(self):
        booking = Booking(
            name="Alex",
            email="alex@example.com",
            booking_date=timezone.localdate() - timedelta(days=1),
            booking_time=time(18, 0),
            guests=2,
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_guests_must_be_at_least_one(self):
        booking = Booking(
            name="Alex",
            email="alex@example.com",
            booking_date=timezone.localdate() + timedelta(days=1),
            booking_time=time(18, 0),
            guests=0,
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()

    def test_guests_cannot_exceed_selected_table_seats(self):
        booking = Booking(
            name="Alex",
            email="alex@example.com",
            booking_date=timezone.localdate() + timedelta(days=1),
            booking_time=time(18, 0),
            table=self.table_two_seats,
            guests=3,
        )

        with self.assertRaises(ValidationError):
            booking.full_clean()


class BookingConflictTests(TestCase):
    def setUp(self):
        self.future_date = timezone.localdate() + timedelta(days=2)
        self.slot_time = time(19, 0)
        self.table = RestaurantTable.objects.create(name="Window", seats=4)

    def test_same_date_time_and_table_is_blocked(self):
        Booking.objects.create(
            name="Sam",
            email="sam@example.com",
            booking_date=self.future_date,
            booking_time=self.slot_time,
            table=self.table,
            guests=2,
        )

        second_booking = Booking(
            name="Jamie",
            email="jamie@example.com",
            booking_date=self.future_date,
            booking_time=self.slot_time,
            table=self.table,
            guests=2,
        )

        with self.assertRaises(ValidationError):
            second_booking.full_clean()

    def test_unassigned_slot_capacity_limit_is_blocked_after_five(self):
        for index in range(5):
            booking = Booking(
                name=f"Guest {index}",
                email=f"guest{index}@example.com",
                booking_date=self.future_date,
                booking_time=self.slot_time,
                guests=2,
            )
            booking.full_clean()
            booking.save()

        sixth_booking = Booking(
            name="Late guest",
            email="late@example.com",
            booking_date=self.future_date,
            booking_time=self.slot_time,
            guests=2,
        )

        with self.assertRaises(ValidationError):
            sixth_booking.full_clean()


class BookingCrudFlowTests(TestCase):
    def setUp(self):
        self.future_date = timezone.localdate() + timedelta(days=3)
        self.table = RestaurantTable.objects.create(name="Quiet area", seats=4)

    def test_create_update_and_delete_booking_flow(self):
        create_response = self.client.post(
            reverse("booking_create"),
            data={
                "name": "Taylor",
                "email": "taylor@example.com",
                "phone": "12345",
                "booking_date": self.future_date.isoformat(),
                "booking_time": "19:00",
                "table": str(self.table.pk),
                "guests": 2,
                "special_request": "Near candle",
            },
            follow=True,
        )
        self.assertEqual(create_response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 1)

        booking = Booking.objects.first()
        self.assertIsNotNone(booking)

        update_response = self.client.post(
            reverse("booking_update", args=[booking.pk]),
            data={
                "name": "Taylor Updated",
                "email": "taylor@example.com",
                "phone": "12345",
                "booking_date": self.future_date.isoformat(),
                "booking_time": "20:00",
                "table": str(self.table.pk),
                "guests": 2,
                "special_request": "Window side",
            },
            follow=True,
        )
        self.assertEqual(update_response.status_code, 200)
        booking.refresh_from_db()
        self.assertEqual(booking.name, "Taylor Updated")
        self.assertEqual(booking.booking_time, time(20, 0))

        delete_response = self.client.post(reverse("booking_delete", args=[booking.pk]), follow=True)
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(Booking.objects.count(), 0)


class KeyPageResponseTests(TestCase):
    def test_home_page_response(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_booking_list_page_response(self):
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)

    def test_booking_create_page_response(self):
        response = self.client.get(reverse("booking_create"))
        self.assertEqual(response.status_code, 200)

    def test_menu_page_response(self):
        response = self.client.get(reverse("menu"))
        self.assertEqual(response.status_code, 200)


class Custom404Tests(TestCase):
    @override_settings(DEBUG=False)
    def test_unknown_url_uses_custom_404_page(self):
        response = self.client.get("/not-a-real-page/")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "404", status_code=404)
        self.assertContains(response, "Go back home", status_code=404)
