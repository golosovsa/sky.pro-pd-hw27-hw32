# Generated by Django 4.1.2 on 2022-11-03 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_managers_user_date_joined_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Возраст, полных лет'),
        ),
    ]