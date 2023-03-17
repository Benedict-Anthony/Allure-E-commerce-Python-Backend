# Generated by Django 4.1.5 on 2023-03-17 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_alter_service_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='price',
        ),
        migrations.AddField(
            model_name='bookings',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
