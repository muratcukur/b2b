# Generated by Django 3.1.6 on 2021-07-02 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ms_a101_bolges', '0010_auto_20210702_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='depotorder',
            name='unit',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
