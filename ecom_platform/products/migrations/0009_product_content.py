# Generated by Django 5.0.4 on 2024-05-05 14:22

import tinymce.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_remove_product_products_pr_title_c8aec9_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='content',
            field=tinymce.models.HTMLField(null=True),
        ),
    ]
