# Generated by Django 3.1.7 on 2021-04-01 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='author',
        ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.DeleteModel(
            name='CountItems',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]