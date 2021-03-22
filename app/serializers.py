from rest_framework import serializers
from .models import *


class ItemSerializer(serializers.ModelSerializer):
    sell_price = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    mid_price = serializers.SerializerMethodField()
    quantity_percent = serializers.SerializerMethodField()
    quantity_self = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    def get_sell_price(self, obj):
        try:
            new_price = obj.price + ((obj.percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

    def get_income(self, obj):
        try:
            new_price = (obj.price + ((obj.percent * obj.price) / 100))
            income = new_price - obj.price
        except:
            income = 0
        return "{:,} сум".format(int(income))

    def get_min_price(self, obj):
        try:
            new_price = obj.price + ((obj.min_percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

    def get_mid_price(self, obj):
        try:
            new_percent = (obj.min_percent + obj.percent) / 2
            new_price = obj.price + ((new_percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

    def get_quantity_percent(self, obj):
        try:
            total = (obj.price + ((obj.percent * obj.price) / 100)) * obj.count
        except:
            total = 0
        return "{:,} сум".format(int(total))

    def get_quantity_self(self, obj):
        try:
            total = obj.price * obj.count
        except:
            total = 0
        return "{:,} сум".format(int(total))


class ItemUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = "pub_date",


class ItemListSerializer(serializers.ModelSerializer):
    sell_price = serializers.SerializerMethodField()
    class Meta:
        model = Item
        fields = ("id", "name", "sell_price",)

    def get_sell_price(self, obj):
        try:
            new_price = obj.price + ((obj.percent * obj.price) / 100)
        except:
            new_price = 0
        return "{:,} сум".format(int(new_price))

class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeIn
        fields = 'name'


class TransactionSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField('get_summary')

    class Meta:
        model = Transaction
        fields = "id", "name", "item", "type_in", "sum", "pub_date"

    def get_summary(self, obj):
        return str(obj.item.name)

class TransactionViewSerializer(serializers.ModelSerializer):
    # item = ItemListSerializer()
    # type_in = TypeSerializer()

    class Meta:
        model = Transaction
        fields = "id", "name", "item", "type_in", "sum", "pub_date"
