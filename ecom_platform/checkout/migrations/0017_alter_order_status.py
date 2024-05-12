# Generated by Django 5.0.4 on 2024-05-12 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0016_order_billing_id_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('paid', 'paid'), ('deliveried', 'deliveried'), ('pending', 'pending'), ('canceled', 'canceled')], default='cash_on_delivery', max_length=120, null=True),
        ),
    ]