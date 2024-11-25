# Generated by Django 5.1.2 on 2024-10-09 08:16

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_remove_category_instruction'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='instruction',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(base_url='/files', location='C:\\Users\\amur_\\Desktop\\NDA\\NDA_app\\privateprivate/'), upload_to='instructions', verbose_name='Инструкция'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=128, null=True, unique=True, verbose_name='Бренд'),
        ),
    ]
