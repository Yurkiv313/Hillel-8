# Generated by Django 4.2.6 on 2023-10-25 20:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cars", "0004_dealership_order"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="dealership",
        ),
        migrations.AddField(
            model_name="order",
            name="car",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="Cars.car",
            ),
            preserve_default=False,
        ),
    ]
