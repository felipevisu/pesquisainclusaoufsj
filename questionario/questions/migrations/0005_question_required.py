# Generated by Django 3.1.7 on 2021-04-20 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20210420_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='required',
            field=models.BooleanField(default=True),
        ),
    ]
