# Generated by Django 3.1 on 2022-04-01 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20211008_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='items_in_page',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='list_rows',
            field=models.PositiveIntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_level',
            field=models.PositiveIntegerField(default=10),
        ),
    ]