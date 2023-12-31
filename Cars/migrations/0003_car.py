# Generated by Django 4.2.6 on 2023-10-21 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cars", "0002_cartype"),
    ]

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(max_length=50)),
                ("year", models.IntegerField()),
                (
                    "car_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Cars.cartype"
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="cars",
                        to="Cars.client",
                    ),
                ),
            ],
        ),
    ]
