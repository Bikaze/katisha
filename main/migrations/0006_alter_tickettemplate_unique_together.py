# Generated by Django 5.0.6 on 2024-05-31 11:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_passenger_birthdate_alter_passenger_phone'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tickettemplate',
            unique_together={('vehicle', 'departure_date', 'departure_time')},
        ),
    ]
