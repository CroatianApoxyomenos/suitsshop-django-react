# Generated by Django 4.1.6 on 2023-02-07 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_orderitem_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='unit_price',
            new_name='total_price',
        ),
    ]