# Generated by Django 3.1 on 2020-09-06 03:25

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0002_auto_20200906_0321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchedvalue',
            name='mileagerange',
            field=django_mysql.models.ListTextField(models.CharField(max_length=100), size=100),
        ),
        migrations.AlterField(
            model_name='searchedvalue',
            name='pricerange',
            field=django_mysql.models.ListTextField(models.CharField(max_length=100), size=100),
        ),
        migrations.AlterField(
            model_name='searchedvalue',
            name='searchlist',
            field=django_mysql.models.ListTextField(models.CharField(max_length=100), size=100),
        ),
    ]
