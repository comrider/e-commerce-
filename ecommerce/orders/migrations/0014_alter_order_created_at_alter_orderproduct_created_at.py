# Generated by Django 4.1.1 on 2022-10-04 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0013_alter_order_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="orderproduct",
            name="created_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
