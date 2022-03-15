# Generated by Django 4.0.3 on 2022-03-14 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resto', '0003_meal_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='isAvailaible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='latitude',
            field=models.CharField(default='0', max_length=200),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='longitude',
            field=models.CharField(default='0', max_length=200),
        ),
    ]