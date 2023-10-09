# Generated by Django 4.2.5 on 2023-10-07 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookingDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('phone', models.CharField(max_length=10)),
                ('pickupdate', models.DateField()),
                ('pickuptime', models.TimeField()),
                ('pickup', models.TextField()),
                ('dropoff', models.TextField()),
                ('ride', models.CharField(choices=[('MI', 'MINI'), ('SE', 'SEDAN'), ('MU', 'MUV'), ('MP', 'MUV PRIME'), ('SV', 'SUV'), ('TP', 'TEMPO')], default='MI', max_length=2)),
                ('twoway', models.BooleanField(default=False)),
                ('bookingdate', models.DateField(auto_now_add=True)),
            ],
        ),
    ]