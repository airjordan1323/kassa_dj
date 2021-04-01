# Generated by Django 3.1.7 on 2021-03-31 11:16

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Кол-во на товар',
                'verbose_name_plural': 'Кол-во на товары',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Наименование')),
                ('price', models.FloatField(verbose_name='Цена')),
                ('count', models.PositiveSmallIntegerField(default=0, verbose_name='Количество')),
                ('percent', models.PositiveSmallIntegerField(verbose_name='Процент наценки')),
                ('min_percent', models.PositiveSmallIntegerField(blank=True, help_text='Минимальный добавочный процент от закупочной стоимости', null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Минимальный Процент наценки')),
                ('description', models.CharField(blank=True, help_text='Краткое описание товара', max_length=600, null=True, verbose_name='Описание')),
                ('image', models.ImageField(blank=True, help_text='Изображение Товара', null=True, upload_to='images/', verbose_name='Изображение')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, help_text='Дата, когда товар был добавлен в базу', verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, verbose_name='Наименование')),
                ('type', models.CharField(choices=[('OUTCOME', 'OUTCOME'), ('INCOME', 'INCOME')], max_length=12, verbose_name='Тип')),
                ('sum', models.PositiveIntegerField(verbose_name='Цена')),
                ('pub_date', models.DateTimeField(auto_now_add=True, help_text='Дата, когда товар был добавлен в базу', verbose_name='Дата публикации')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кассир')),
                ('items', models.ManyToManyField(blank=True, related_name='trans', to='app.Item', verbose_name='цены Товаров')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Наименование')),
                ('phone', models.CharField(max_length=200, verbose_name='Телефон')),
                ('type_dj', models.CharField(choices=[('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('NULL', 'NULL')], default='NULL', max_length=10, verbose_name='Тип')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('last_change', models.DateTimeField(default=datetime.datetime(2021, 3, 31, 11, 16, 12, 126228, tzinfo=utc), verbose_name='Дата изменении')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Кассир')),
                ('items', models.ManyToManyField(related_name='orders', to='app.CountItems', verbose_name='Товары и кол-во')),
            ],
            options={
                'verbose_name': 'Сетка',
                'verbose_name_plural': 'Сетки',
            },
        ),
        migrations.AddField(
            model_name='countitems',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.item', verbose_name='count_item'),
        ),
    ]
