# Generated by Django 4.2.5 on 2023-10-13 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_cars_base_d'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cars',
            name='base_d',
        ),
        migrations.AddField(
            model_name='cars',
            name='base_d_i',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cars',
            name='base_d_o',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cars',
            name='add_charge_i',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='add_charge_o',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='basefare_i',
            field=models.SmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='cars',
            name='basefare_o',
            field=models.SmallIntegerField(),
        ),
    ]