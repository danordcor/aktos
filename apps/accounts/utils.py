import csv
import io
import logging
from django.db import transaction
from django.http import JsonResponse
from apps.accounts.models import Account, Consumer, Client

# Configure logging
logger = logging.getLogger(__name__)


class CSVProcessor:
    """
    Handles the processing and import of CSV files containing account and consumer data.
    """

    EXPECTED_HEADERS = [
        "client reference no",
        "balance",
        "status",
        "consumer name",
        "consumer address",
        "ssn",
    ]

    def __init__(self, file):
        """
        Initializes the processor with the given CSV file.
        :param file: File object containing CSV data.
        """
        self.file = file

    def validate_file(self):
        """
        Validates that the uploaded file is a CSV.
        :return: JsonResponse if invalid, None if valid.
        """
        if not self.file.name.endswith(".csv"):
            logger.error("Invalid file format. Only CSV files are allowed.")
            return JsonResponse({"error": "Invalid file format"}, status=400)
        return None

    def decode_csv(self):
        """
        Decodes the uploaded CSV file and returns a CSV reader object.
        :return: csv.reader object if successful, JsonResponse if failed.
        """
        try:
            decoded_file = self.file.read().decode("utf-8")
            csv_reader = csv.reader(io.StringIO(decoded_file))
            return csv_reader
        except Exception as e:
            logger.error(f"Failed to decode CSV file: {e}")
            return JsonResponse({"error": "Unable to read CSV file"}, status=400)

    def validate_headers(self, headers):
        """
        Validates that the CSV headers match the expected structure.
        :param headers: List of column headers from the CSV file.
        :return: JsonResponse if invalid, None if valid.
        """
        if headers != self.EXPECTED_HEADERS:
            logger.error(
                f"Invalid CSV structure. Expected headers: {self.EXPECTED_HEADERS}"
            )
            return JsonResponse({"error": "Invalid CSV structure"}, status=400)
        return None

    def process(self):
        """
        Processes the CSV file and imports data into the database.
        :return: JsonResponse indicating success or failure.
        """
        file_validation = self.validate_file()
        if file_validation:
            return file_validation

        csv_reader = self.decode_csv()
        if isinstance(csv_reader, JsonResponse):
            return csv_reader

        headers = next(csv_reader, None)
        header_validation = self.validate_headers(headers)
        if header_validation:
            return header_validation

        try:
            client, _ = Client.objects.get_or_create(name="Default Client")
            processed_rows = 0

            with transaction.atomic():
                for row in csv_reader:
                    if len(row) != 6:
                        logger.warning(f"Skipping malformed row: {row}")
                        continue

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
                    processed_rows += 1

            logger.info(f"Successfully processed {processed_rows} rows from CSV.")
            return JsonResponse(
                {
                    "message": f"CSV imported successfully, {processed_rows} records added"
                },
                status=201,
            )

        except Exception as e:
            logger.error(f"Unexpected error processing CSV: {e}")
            return JsonResponse({"error": str(e)}, status=500)
