# Generated by Django 5.1.2 on 2024-11-26 04:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_category_instruction_alter_brand_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offers', to='catalog.brand', verbose_name='Бренд'),
        ),
    ]
