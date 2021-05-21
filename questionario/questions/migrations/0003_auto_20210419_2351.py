# Generated by Django 3.1.7 on 2021-04-20 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20210419_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('RADIO', 'radio'), ('SELECT', 'select'), ('CHECKBOX', 'dropbox'), ('TEXT', 'text'), ('RANK', 'rank'), ('RANK_2', 'rank_2')], default='RANK', max_length=30),
        ),
    ]
