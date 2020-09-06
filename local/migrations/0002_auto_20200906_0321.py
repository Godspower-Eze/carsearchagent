# Generated by Django 3.1 on 2020-09-06 03:21

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('local', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SearchedValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('searchlist', django_mysql.models.ListTextField(models.IntegerField(), size=100)),
                ('mileagerange', django_mysql.models.ListTextField(models.IntegerField(), size=100)),
                ('pricerange', django_mysql.models.ListTextField(models.IntegerField(), size=100)),
            ],
        ),
        migrations.DeleteModel(
            name='SearchedValues',
        ),
    ]