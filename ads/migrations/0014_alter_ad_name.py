# Generated by Django 4.1.2 on 2022-11-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0013_alter_ad_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Заголовок'),
        ),
    ]
