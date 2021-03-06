# Generated by Django 3.1.7 on 2021-03-27 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
        ('parkinglot', '0005_auto_20210327_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='charges',
            name='vehicle_type',
            field=models.IntegerField(choices=[(0, 'TWO_WHEELER'), (1, 'THREE_WHEELER'), (2, 'FOUR_WHEELER')], default=0),
        ),
        migrations.AddField(
            model_name='parking',
            name='vehicle_ref',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='customer.vehicle'),
            preserve_default=False,
        ),
    ]
