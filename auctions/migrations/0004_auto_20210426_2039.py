# Generated by Django 3.1.6 on 2021-04-26 15:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20210426_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bids',
            name='date',
            field=models.DateField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listing',
            name='createdDate',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
