# Generated by Django 4.2.2 on 2023-06-20 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swimapp', '0007_remove_availability_availability_user_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
