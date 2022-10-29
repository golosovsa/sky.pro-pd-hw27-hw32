# Generated by Django 4.1.2 on 2022-10-29 06:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('ads', '0010_remove_user_locations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to='users.user', verbose_name='Автор'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
