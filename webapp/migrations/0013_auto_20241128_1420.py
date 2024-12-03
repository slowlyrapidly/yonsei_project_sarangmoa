# Generated by Django 3.1.3 on 2024-11-28 05:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20241128_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy_list',
            name='buy_date',
            field=models.DateField(default=datetime.datetime(2024, 11, 28, 5, 20, 10, 763827, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='uploaded_product',
            name='created_date',
            field=models.DateField(default=datetime.datetime(2024, 11, 28, 5, 20, 10, 763827, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='uploaded_product',
            name='updated_date',
            field=models.DateField(default=datetime.datetime(2024, 11, 28, 5, 20, 10, 763827, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
