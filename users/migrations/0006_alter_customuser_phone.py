# Generated by Django 4.1.5 on 2023-05-30 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_alter_userprofile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
