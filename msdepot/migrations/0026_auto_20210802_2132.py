# Generated by Django 3.1.6 on 2021-08-02 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msdepot', '0025_auto_20210802_0101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meyvesebzeyeni',
            name='fruit_vegetable_kod_yeni',
            field=models.IntegerField(blank=True, default=None, null=True, unique=True),
        ),
    ]