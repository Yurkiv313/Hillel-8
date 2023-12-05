# Generated by Django 4.2.6 on 2023-10-28 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cars", "0007_orderquantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderquantity",
            name="car_type",
        ),
        migrations.AddField(
            model_name="orderquantity",
            name="car",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="order_quantities",
                to="Cars.car",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="orderquantity",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="car",
                to="Cars.order",
            ),
        ),
    ]
