# Generated by Django 4.2.6 on 2023-10-25 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cars", "0005_remove_order_dealership_order_car"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="car",
        ),
        migrations.AddField(
            model_name="order",
            name="dealership",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to="Cars.dealership",
            ),
            preserve_default=False,
        ),
    ]
