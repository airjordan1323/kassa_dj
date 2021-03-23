from .serializers import *
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class ItemView(generics.CreateAPIView):
    serializer_class = ItemUpSerializer


class ItemListView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['id', 'name', 'description']
    ordering_fields = ['id', 'price', 'name', 'pub_date']


class ItemDetailView(APIView):

    def get(self, request, pk):
        item = Item.objects.get(id=pk)
        serializer = ItemDetailSerializer(item, context={'request': request})
        # transaction = Transaction.objects.filter()
        # serial = TransactionSerializer(transaction)
        return Response({'item': serializer.data})



class ItemDeleteView(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer


class TransPostView(APIView):
    def get(self, request, pk):
        trans = Transaction.objects.get(id=pk)
        serializer = TransactionSerializer(trans)
        return Response({'transaction': serializer.data})


class ItemUpdateView(generics.UpdateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemUpSerializer


class BuyView(APIView):
    parser_classes = [JSONParser]

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
            transaction = Transaction.objects.create(type="INCOME", sum=final)
            for item_id, count in freq.items():
                item = Item.objects.get(id=item_id)
                item.count -= count
                item.save()
                transaction.items.add(item_id)
            return Response({"status": "added"}, status=201)
        except Exception as e:
            return Response({"status": e}, status=500)
