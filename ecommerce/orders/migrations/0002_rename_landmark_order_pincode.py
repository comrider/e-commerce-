# Generated by Django 4.1.1 on 2022-09-25 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='landmark',
            new_name='pincode',
        ),
    ]
