import csv
import io
from django.db import transaction
from django.http import JsonResponse
from .models import Account, Consumer, Client

def process_csv_data(file):
    if not file.name.endswith(".csv"):
        return JsonResponse({"error": "Invalid file format"}, status=400)

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
