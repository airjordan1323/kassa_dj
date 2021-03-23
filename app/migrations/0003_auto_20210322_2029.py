# Generated by Django 3.1.7 on 2021-03-22 15:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210322_1819'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TypeIn',
        ),
        migrations.AddField(
            model_name='transaction',
            name='last_change',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Дата, когда товар был редактирован', verbose_name='Дата изменении'),
            preserve_default=False,
        ),
    ]