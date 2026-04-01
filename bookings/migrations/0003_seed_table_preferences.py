from django.db import migrations


def create_default_table_preferences(apps, schema_editor):
    restaurant_table_model = apps.get_model("bookings", "RestaurantTable")

    default_preferences = [
        ("Near window", 2),
        ("Quiet section", 2),
        ("Near bathroom", 2),
        ("Main dining area", 4),
        ("Not bothered (any table)", 4),
    ]

    for name, seats in default_preferences:
        restaurant_table_model.objects.get_or_create(
            name=name,
            defaults={"seats": seats},
        )


def remove_default_table_preferences(apps, schema_editor):
    restaurant_table_model = apps.get_model("bookings", "RestaurantTable")
    names = [
        "Near window",
        "Quiet section",
        "Near bathroom",
        "Main dining area",
        "Not bothered (any table)",
    ]
    restaurant_table_model.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("bookings", "0002_restauranttable_booking_table"),
    ]

    operations = [
        migrations.RunPython(
            create_default_table_preferences,
            reverse_code=remove_default_table_preferences,
        ),
    ]
