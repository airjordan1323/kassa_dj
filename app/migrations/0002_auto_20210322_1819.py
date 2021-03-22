# Generated by Django 3.1.7 on 2021-03-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='item',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='type_in',
        ),
        migrations.AddField(
            model_name='transaction',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, related_name='trans', to='app.Item', verbose_name='цены Товаров'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('OUTCOME', 'OUTCOME'), ('INCOME', 'INCOME')], default='INCOME', max_length=12, verbose_name='Тип'),
            preserve_default=False,
        ),
    ]