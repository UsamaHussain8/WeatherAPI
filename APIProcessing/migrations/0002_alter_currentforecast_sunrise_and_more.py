# Generated by Django 5.1.4 on 2024-12-20 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APIProcessing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentforecast',
            name='sunrise',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='currentforecast',
            name='sunset',
            field=models.TimeField(null=True),
        ),
    ]