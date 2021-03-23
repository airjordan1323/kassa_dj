from django.contrib import admin
from django.utils.safestring import mark_safe
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
from .models import *

admin.site.site_title = "KASSA"
admin.site.site_header = "KASSA"


@admin.register(Transaction)
class CostsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sum", "pub_date")
    list_display_links = ("id", "name")
    list_filter = (
        ('pub_date', DateRangeFilter),
        ('last_change', DateTimeRangeFilter),
    )
    search_fields = ('id', 'name')
    readonly_fields = ('id', 'pub_date')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_image_thumb", "description", "sell_price", "count")
    list_display_links = ("id", "name", "get_image_thumb")
    save_on_top = True
    save_as = True
    search_fields = ('id', 'name', 'description')
    readonly_fields = ('pub_date', 'id', 'sell_price', 'income', 'min_price', 'mid_price', 'quantity_self',
                       'quantity_percent', 'get_image',)

    def sell_price(self, obj):
        try:
            new_price = obj.price + ((obj.percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

    def income(self, obj):
        try:
            new_price = (obj.price + ((obj.percent * obj.price) / 100))
            income = new_price - obj.price
        except:
            income = 0
        return "{:,} сум".format(int(income))

    def min_price(self, obj):
        try:
            new_price = obj.price + ((obj.min_percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

    def mid_price(self, obj):
        try:
            new_percent = (obj.min_percent + obj.percent) / 2
            new_price = obj.price + ((new_percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

    def quantity_percent(self, obj):
        try:
            total = (obj.price + ((obj.percent * obj.price) / 100)) * obj.count
        except:
            total = 0
        return "{:,} сум".format(int(total))

    def quantity_self(self, obj):
        try:
            total = obj.price * obj.count
        except:
            total = 0
        return "{:,} сум".format(int(total))

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100%" height="100%">')

    def get_image_thumb(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="160" height="160">')
