# Generated by Django 3.1 on 2020-12-01 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20201201_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymaster',
            name='parent_category',
            field=models.CharField(max_length=20),
        ),
    ]