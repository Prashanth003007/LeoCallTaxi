# Generated by Django 4.2.5 on 2023-10-10 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_bookingdetails_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='joindetail',
            name='modelname',
        ),
    ]