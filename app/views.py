from datetime import timezone
from rest_framework.pagination import LimitOffsetPagination
from .serializers import *
from rest_framework import filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class ItemView(generics.CreateAPIView):
    serializer_class = ItemUpSerializer
    # permission_classes = [permissions.IsAdminUser]


class ItemListView(generics.ListAPIView):
    serializer_class = ItemListSerializer
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name', 'description']
    ordering_fields = ['id', 'price', 'name', 'pub_date']

    def get_queryset(self):
        date_from = self.request.query_params.get('from')
        date_to = self.request.query_params.get('to')
        return Item.objects.filter(pub_date__range=[date_from, date_to])


class ItemDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        item = Item.objects.get(id=pk)
        serializer = ItemDetailSerializer(item, context={'request': request})
        return Response({'item': serializer.data})


class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer
    # permission_classes = [permissions.IsAdminUser]


class TransOUTListView(generics.ListAPIView):
    queryset = Transaction.objects.filter(type="OUTCOME")
    serializer_class = TransactionSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['id', 'author', 'name', 'pub_date']


class TransINListView(generics.ListAPIView):
    queryset = Transaction.objects.filter(type="INCOME")
    serializer_class = TransactionSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'author', 'name', 'pub_date']


class TransGetView(APIView):

    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        trans = Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(trans)
        return Response({'transaction': serializer.data})


class TransPostView(generics.CreateAPIView):
    serializer_class = TransactionPostSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    # permission_classes = [permissions.IsAdminUser]


class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer
    # permission_classes = [permissions.IsAuthenticated]


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
