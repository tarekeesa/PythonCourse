# Generated by Django 5.0.4 on 2024-05-12 10:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Card',
        ),
    ]