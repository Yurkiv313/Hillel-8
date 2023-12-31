# Generated by Django 4.2.6 on 2023-10-28 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Cars", "0008_remove_orderquantity_car_type_orderquantity_car_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderquantity",
            name="order",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="car_types",
                to="Cars.order",
            ),
        ),
    ]
