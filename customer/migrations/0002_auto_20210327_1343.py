# Generated by Django 3.1.7 on 2021-03-27 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='vehicle',
            unique_together={('customer_ref', 'vehicle_no')},
        ),
    ]
