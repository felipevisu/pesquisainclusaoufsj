# Generated by Django 3.1.7 on 2021-04-20 02:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20210419_2156'),
        ('answers', '0002_response_session'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('response', 'question')},
        ),
    ]