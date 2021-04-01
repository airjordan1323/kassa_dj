from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime
from user.models import Account


class Item(models.Model):
    name = models.CharField("Наименование", max_length=250)
    price = models.FloatField("Цена")
    count = models.PositiveSmallIntegerField(
        "Количество",
        default=0
    )
    percent = models.PositiveSmallIntegerField("Процент наценки")
    min_percent = models.PositiveSmallIntegerField(
        "Минимальный Процент наценки",
        validators=[
            MinValueValidator(0)
        ],
        blank=True, null=True,
        help_text="Минимальный добавочный процент от закупочной стоимости",
    )
    description = models.CharField('Описание', blank=True, null=True, max_length=600,
                                   help_text="Краткое описание товара")
    image = models.ImageField("Изображение", upload_to='images/', null=True, blank=True,
                              help_text="Изображение Товара")
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
    author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Кассир", blank=True, null=True)
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

    def save(self, *args, **kwargs):
        if self.type == "INCOME":
            self.name = "INCOME"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"

# class CountItems(models.Model):
#     item = models.ForeignKey(Item, verbose_name='count_item', on_delete=models.CASCADE)
#     count = models.PositiveSmallIntegerField()
#
#     class Meta:
#         verbose_name = "Кол-во на товар"
#         verbose_name_plural = "Кол-во на товары"


# class Order(models.Model):
#     author = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Кассир", blank=True, null=True)
#     name = models.CharField("Наименование", max_length=200)
#     phone = models.CharField("Телефон", max_length=200)
#     items = models.ManyToManyField(CountItems, verbose_name="Товары и кол-во", related_name="orders")
#     TYPE_CHOICE = (
#         ('ACCEPTED', 'ACCEPTED'),
#         ('REJECTED', 'REJECTED'),
#         ('NULL', 'NULL')
#     )
#     type_dj = models.CharField("Тип", choices=TYPE_CHOICE, default="NULL", max_length=10)
#     pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
#     last_change = models.DateTimeField("Дата изменении", default=timezone.now())
#
#     def save(self, *args, **kwargs):
#         self.last_change = timezone.now()
#         super().save(*args, **kwargs)
#
#     class Meta:
#         verbose_name = "Сетка"
#         verbose_name_plural = "Сетки"
