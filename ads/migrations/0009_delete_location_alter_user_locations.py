# Generated by Django 4.1.2 on 2022-10-29 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('ads', '0008_alter_ad_category_delete_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Location',
        ),
        migrations.AlterField(
            model_name='user',
            name='locations',
            field=models.ManyToManyField(related_name='users', to='locations.location', verbose_name='Локации'),
        ),
    ]
