# Generated by Django 3.2 on 2021-06-03 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('answers', '0006_remove_response_interview_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='body',
            field=models.TextField(blank=True, null=True, verbose_name='resposta'),
        ),
    ]
