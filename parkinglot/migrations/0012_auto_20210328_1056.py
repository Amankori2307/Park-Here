# Generated by Django 3.1.7 on 2021-03-28 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0011_auto_20210327_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parking',
            name='entry_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]