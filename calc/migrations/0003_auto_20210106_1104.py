# Generated by Django 3.1.5 on 2021-01-06 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0002_test_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='alliance',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
