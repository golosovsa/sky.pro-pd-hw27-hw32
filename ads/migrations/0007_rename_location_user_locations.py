# Generated by Django 4.1.2 on 2022-10-28 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0006_remove_user_location_user_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='location',
            new_name='locations',
        ),
    ]
