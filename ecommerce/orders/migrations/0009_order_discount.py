# Generated by Django 4.1.1 on 2022-10-02 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0008_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="discount",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]