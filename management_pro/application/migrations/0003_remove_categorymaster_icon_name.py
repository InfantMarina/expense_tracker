# Generated by Django 3.1 on 2020-11-30 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20201121_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymaster',
            name='icon_name',
        ),
    ]
