# Generated by Django 2.1.7 on 2019-03-03 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20190303_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.CharField(default='DEFAULT VALUE', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='mobno',
            field=models.CharField(default='DEFAULT VALUE', max_length=20),
        ),
    ]
