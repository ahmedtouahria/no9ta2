# Generated by Django 4.0.3 on 2022-03-30 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resto', '0005_remove_restaurant_email_remove_restaurant_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='position',
            field=models.CharField(max_length=220, null=True),
        ),
    ]