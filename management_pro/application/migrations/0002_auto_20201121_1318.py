# Generated by Django 3.1 on 2020-11-21 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=35)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('balance', models.IntegerField()),
                ('account_holder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_mprouser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=20)),
                ('category_description', models.CharField(max_length=20)),
                ('is_child', models.BooleanField()),
                ('parent_category', models.CharField(max_length=20)),
                ('color', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon_name', models.CharField(max_length=20)),
                ('path', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=15)),
                ('amount', models.IntegerField()),
                ('description', models.CharField(max_length=20)),
                ('payee', models.CharField(max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_account', to='application.account')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transaction_mprouser', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_categorymaster', to='application.categorymaster')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=20)),
                ('previous_value', models.IntegerField()),
                ('current_value', models.IntegerField()),
                ('modified_date', models.DateTimeField()),
                ('modified_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactionhistory_mprouser', to=settings.AUTH_USER_MODEL)),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_transaction', to='application.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='LoginHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('login_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loginhistory_mprouser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='categorymaster',
            name='icon_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_icon', to='application.icon'),
        ),
    ]
