# Generated by Django 4.2.3 on 2023-08-21 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_organization'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='Product',
            new_name='product',
        ),
    ]
