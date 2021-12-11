# Generated by Django 3.2.9 on 2021-11-22 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_remove_todolist_reminder'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='Tree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='todolist.todolist'),
        ),
    ]