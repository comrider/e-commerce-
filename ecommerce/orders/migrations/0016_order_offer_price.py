# Generated by Django 4.1.1 on 2022-10-08 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0015_razororder"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="offer_price",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
