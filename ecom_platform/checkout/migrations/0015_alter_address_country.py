# Generated by Django 5.0.4 on 2024-05-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0014_alter_order_cart_alter_order_shipping_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='United Arab Emirates', max_length=120),
        ),
    ]