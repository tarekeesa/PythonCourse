# Generated by Django 5.0.4 on 2024-05-08 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_remove_address_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
