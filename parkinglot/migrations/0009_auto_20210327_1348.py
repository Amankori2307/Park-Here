# Generated by Django 3.1.7 on 2021-03-27 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parkinglot', '0008_parkinglot_longcord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='parkinglot',
            old_name='latCord',
            new_name='lat',
        ),
        migrations.RenameField(
            model_name='parkinglot',
            old_name='longCord',
            new_name='long',
        ),
    ]
