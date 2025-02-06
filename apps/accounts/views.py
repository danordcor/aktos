import csv
import io

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter
from rest_framework.views import APIView

from django.db.models import Q
from django.db import transaction
from django.http import JsonResponse
from .models import Account, Client, Consumer
from .serializers import AccountSerializer


class AccountListView(generics.ListAPIView):
    serializer_class = AccountSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["balance", "status"]

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

        if not file.name.endswith(".csv"):
            return JsonResponse(
                {"error": "Invalid file format. Please upload a CSV file."}, status=400
            )

        try:
            decoded_file = file.read().decode("utf-8")
            csv_reader = csv.reader(io.StringIO(decoded_file))
            headers = next(csv_reader, None)

            expected_headers = [
                "client reference no",
                "balance",
                "status",
                "consumer name",
                "consumer address",
                "ssn",
            ]
            if headers != expected_headers:
                return JsonResponse({"error": "Invalid CSV structure."}, status=400)

            client, _ = Client.objects.get_or_create(name="Default Client")

            with transaction.atomic():
                for row in csv_reader:
                    if len(row) != 6:
                        return JsonResponse({"error": "Malformed CSV row."}, status=400)

                    (
                        client_reference_no,
                        balance,
                        status,
                        consumer_name,
                        consumer_address,
                        ssn,
                    ) = row

                    consumer, _ = Consumer.objects.get_or_create(
                        name=consumer_name.strip(),
                        address=consumer_address.strip(),
                        ssn=ssn.strip(),
                    )

                    account, created = Account.objects.get_or_create(
                        client=client,
                        client_reference_no=client_reference_no.strip(),
                        defaults={
                            "balance": balance,
                            "status": status.lower(),
                        },
                    )
                    account.consumers.add(consumer)

            return JsonResponse({"message": "CSV imported successfully"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
