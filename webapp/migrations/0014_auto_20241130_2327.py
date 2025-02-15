# Generated by Django 3.1.3 on 2024-11-30 14:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20241128_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy_list',
            name='pay_method',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='buy_list',
            name='buy_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='uploaded_product',
            name='created_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='uploaded_product',
            name='updated_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
