# Generated by Django 5.1.2 on 2024-10-09 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_alter_category_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='instruction',
        ),
    ]
