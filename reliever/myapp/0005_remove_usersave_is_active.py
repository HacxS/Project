# Generated by Django 2.0.1 on 2019-03-06 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_usersave_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersave',
            name='is_active',
        ),
    ]