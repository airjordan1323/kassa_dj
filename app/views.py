from .serializers import *
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from datetime import datetime

# class BigListPagination(PageNumberPagination):
#     page_size = 20
#     page_size_query_param = 'page_size'
#     max_page_size = 40

class ItemView(generics.CreateAPIView):
    serializer_class = ItemUpSerializer


class ItemGetView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'price', 'name']


class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer


class TransPostView(generics.CreateAPIView):
    trans = Transaction.objects.all()
    serializer_class = TransactionSerializer


class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer


class TransGetView(APIView):
    # queryset = Transaction.objects.all
    # serializer = TransactionViewSerializer

    def get(self, request):
        transaction = Transaction.objects.all()
        serializer = TransactionViewSerializer(transaction, many=True)
        item = Item.objects.all()
        products = ItemSerializer(item, many=True)
        typing = TypeIn.objects.all()
        type = TypeSerializer(typing, many=True)
        return Response({'queryset': serializer.data,
                         'item': products.data,
                         'typing': type.data})


# class InComeView(APIView):
#
#     def post(self, request, pk):
#         income = Income.objects.all()
#         ser = InComeSerializer(income)
#         item = Item.objects.all()
#         serializer = ItemSerializer(item)
#         return Response({'ser:': ser.data, 'serializer': serializer.data})


