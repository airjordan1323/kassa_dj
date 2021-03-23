from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from user.models import Account


class Item(models.Model):
    name = models.CharField("Наименование", max_length=250)
    price = models.FloatField("Цена")
    count = models.PositiveSmallIntegerField(
        "Количество",
        default=0
    )
    percent = models.PositiveSmallIntegerField(
        "Процент наценки",
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        help_text="Добавочный процент от закупочной стоимости"
    )
    min_percent = models.PositiveSmallIntegerField(
        "Минимальный Процент наценки",
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0)
        ],
        blank=True, null=True,
        help_text="Минимальный добавочный процент от закупочной стоимости",
    )
    description = models.CharField('Описание', blank=True, null=True, max_length=600,
                                   help_text="Краткое описание товара")
    image = models.ImageField("Изображение", upload_to='images')
    pub_date = models.DateTimeField("Дата добавления", default=datetime.now,
                                    help_text="Дата, когда товар был добавлен в базу")

    def save(self, *args, **kwargs):
        if self.min_percent is None:
            self.min_percent = self.percent
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Transaction(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Кассир")
    name = models.CharField("Наименование", max_length=250, blank=True)
    items = models.ManyToManyField(Item, verbose_name="цены Товаров", related_name="trans", blank=True)
    TYPE_CHOICE = (
        ('OUTCOME', 'OUTCOME'),
        ('INCOME', 'INCOME')
    )
    type = models.CharField("Тип", max_length=12, choices=TYPE_CHOICE)
    sum = models.PositiveIntegerField("Цена")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True,
                                    help_text="Дата, когда товар был добавлен в базу")
    last_change = models.DateTimeField("Дата изменении", auto_now_add=True,
                                       help_text="Дата, когда товар был редактирован")

    def save(self, *args, **kwargs):
        if self.type == "INCOME":
            self.name = "INCOME"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
