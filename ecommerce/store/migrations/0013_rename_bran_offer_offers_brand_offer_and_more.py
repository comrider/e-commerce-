# Generated by Django 4.1.1 on 2022-10-05 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0012_rename_brand_offer_offers_bran_offer_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="offers",
            old_name="bran_offer",
            new_name="brand_offer",
        ),
        migrations.RenameField(
            model_name="offers",
            old_name="cat_offer",
            new_name="category_offer",
        ),
        migrations.RenameField(
            model_name="offers",
            old_name="pro_offer",
            new_name="product_offer",
        ),
    ]
