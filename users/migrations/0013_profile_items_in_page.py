# Generated by Django 3.1 on 2021-10-05 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20210903_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='items_in_page',
            field=models.IntegerField(default=10),
        ),
    ]