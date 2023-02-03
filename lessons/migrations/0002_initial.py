# Generated by Django 4.1.5 on 2023-02-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='assets',
            field=models.ManyToManyField(blank=True, to='products.products'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='instructions',
            field=models.ManyToManyField(to='lessons.instruction'),
        ),
    ]