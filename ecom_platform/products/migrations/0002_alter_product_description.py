# Generated by Django 5.0.4 on 2024-04-30 08:26

import django_quill.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
