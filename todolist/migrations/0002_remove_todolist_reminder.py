# Generated by Django 3.2.9 on 2021-11-14 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='reminder',
        ),
    ]
