from datetime import timezone
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from .serializers import *
from rest_framework import filters, generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10000
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ItemView(generics.CreateAPIView):
    serializer_class = ItemUpSerializer
    permission_classes = [permissions.IsAdminUser]


class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name', 'description', ]
    ordering_fields = ['id', 'price', 'name', 'pub_date', ]

    def get_queryset(self):
        date_from = self.request.query_params.get('from')
        date_to = self.request.query_params.get('to')
        if date_from and date_to:
            return Item.objects.filter(pub_date__range=[date_from, date_to])
        else:
            return Item.objects.all()


class ItemDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        item = Item.objects.get(id=pk)
        serializer = ItemDetailSerializer(item, context={'request': request})
        return Response({'item': serializer.data})


class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer
    permission_classes = [permissions.IsAdminUser]


class TransListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'author', 'name', 'pub_date']
    filterset_fields = ['type']

    def get_queryset(self):
        date_from = self.request.query_params.get('from')
        date_to = self.request.query_params.get('to')
        if date_from and date_to:
            return Transaction.objects.filter(pub_date__range=[date_from, date_to])
        else:
            return Transaction.objects.all()


class TransPostView(generics.CreateAPIView):
    serializer_class = TransactionPostSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def get_author(self, serializer):
        return serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.get_author(serializer)
        return Response(TransactionSerializer(instance).data)


class TransDeleteView(generics.DestroyAPIView):
    queryset = Transaction.objects.filter(type="OUTCOME")
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAdminUser]


class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer
    permission_classes = [permissions.IsAdminUser]


class BuyView(APIView):
    parser_classes = [JSONParser]

    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
            :param request:
            :return:
        """
        final = 0
        freq = {}
        for i in request.data['items']:
            final += i['price']
            if i['id'] in freq:
                freq[i['id']] += 1
            else:
                freq[i['id']] = 1

        try:
            transaction = Transaction.objects.create(author=request.user, type="INCOME", sum=final)
            for item_id, count in freq.items():
                item = Item.objects.get(id=item_id)
                item.count -= count
                item.save()
                transaction.items.add(item_id)
            return Response({"status": "added"}, status=201)
        except Exception as e:
            return Response({"status": e}, status=500)


class TransInDeleteView(generics.DestroyAPIView):
    queryset = Transaction.objects.filter(type="INCOME")
    serializer_class = TransactionSerializer


class AuthorView(APIView):
    def get(self, request):
        user = Account.objects.get(id=request.user.id)
        serializer = AccountsSerializer(user)
        return Response(serializer.data)

# class OrderListView(generics.ListAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#
#
# class OrderNullView(APIView):
#     parser_classes = [JSONParser]
#
#     def post(self, request):
#         freq = {}
#         for i in request.data['items']:
#             if i['id'] in freq:
#                 freq[i['id']] += 1
#             else:
#                 freq[i['id']] = 1
#
#         try:
#             order = Order.objects.create(type_dj="NULL", author=request.user, name=request.data['name'],
#                                          phone=request.data['phone'],)
#             for item_id, count in freq.items():
#                 item = Item.objects.get(id=item_id)
#                 item.count -= count
#                 item.save()
#                 count_item = CountItems.objects.create(item=item, count=count)
#                 order.items.add(count_item)
#             return Response({"status": "added"}, status=201)
#         except Exception as e:
#             return Response({"status": str(e)}, status=500)
#
#
# class OrderUpdateView(APIView):
#     def get(self, request, pk, action):
#         order = Order.objects.get(id=pk)
#         if action == "accept":
#             order.type_dj = "ACCEPTED"
#             order.save()
#             trans = Transaction(author=request.user, type="INCOME", sum=0)
#             final = 0
#             count_items = []
#             for item in order.items.all():
#                 final += item.item.count * item.item.price
#                 count_items.append(item.item.id)
#             trans.sum = final
#             trans.save()
#             for id in count_items:
#                 trans.items.add(id)
#             return Response(TransactionSerializer(trans).data)
#         elif action == "reject":
#             pass
#         else:
#             return Response({'error': "Unknown action, try using accept or reject"})
