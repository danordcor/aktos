from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from apps.accounts.utils import CSVProcessor

from apps.accounts.models import Account
from apps.accounts.serializers import AccountSerializer


class AccountPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class AccountListView(generics.ListAPIView):
    serializer_class = AccountSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["balance", "status"]
    pagination_class = AccountPagination

    def get_queryset(self):
        queryset = Account.objects.all()

        min_balance = self.request.query_params.get("min_balance", None)
        max_balance = self.request.query_params.get("max_balance", None)
        consumer_name = self.request.query_params.get("consumer_name", None)
        status = self.request.query_params.get("status", None)

        if min_balance is not None:
            queryset = queryset.filter(balance__gte=min_balance)

        if max_balance is not None:
            queryset = queryset.filter(balance__lte=max_balance)

        if status is not None:
            queryset = queryset.filter(status=status.lower())

        if consumer_name is not None:
            queryset = queryset.filter(consumers__name__icontains=consumer_name)

        return queryset


class ImportCSVView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"error": "No file provided"}, status=400)

        return CSVProcessor(file).process()
