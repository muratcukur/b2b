# Generated by Django 3.1.6 on 2021-06-12 13:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ms_a101_bolges', '0003_auto_20210612_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depotorders',
            name='user_name',
        ),
    ]
