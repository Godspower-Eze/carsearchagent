# Generated by Django 3.1 on 2020-09-06 03:29

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0003_auto_20200906_0325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchedvalue',
            name='mileagerange',
            field=django_mysql.models.ListTextField(models.IntegerField(), size=100),
        ),
        migrations.AlterField(
            model_name='searchedvalue',
            name='pricerange',
            field=django_mysql.models.ListTextField(models.IntegerField(), size=100),
        ),
    ]
