# Generated by Django 5.0.4 on 2024-05-09 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_remove_order_checkout_or_user_id_6a73f6_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
