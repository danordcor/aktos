from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Client, Consumer, Account
import uuid
import io
import csv


class TestAccountListView(APITestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(name="Test Client")

        for i in range(15):
            consumer = Consumer.objects.create(
                name=f"User {i}",
                address=f"Address {i}",
                ssn=f"123-45-{6789 + i}",
            )
            account = Account.objects.create(
                client=self.client_obj,
                client_reference_no=uuid.uuid4(),
                balance=100 * (i + 1),
                status="in_collection",
            )
            account.consumers.add(consumer)

    def test_get_paginated_accounts(self):
        url = reverse("accounts-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())
        self.assertEqual(len(response.json()["results"]), 10)

    def test_get_second_page_accounts(self):
        url = reverse("accounts-list") + "?page=2"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())
        self.assertEqual(len(response.json()["results"]), 5)

    def test_filter_accounts_by_min_balance(self):
        url = reverse("accounts-list") + "?min_balance=1000"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())
        self.assertTrue(
            all(float(acc["balance"]) >= 1000 for acc in response.json()["results"])
        )

    def test_filter_accounts_by_max_balance(self):
        url = reverse("accounts-list") + "?max_balance=500"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())
        self.assertTrue(
            all(float(acc["balance"]) <= 500 for acc in response.json()["results"])
        )

    def test_filter_accounts_by_status(self):
        url = reverse("accounts-list") + "?status=in_collection"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())
        self.assertEqual(len(response.json()["results"]), 10)

    def test_filter_accounts_by_consumer_name(self):
        url = reverse("accounts-list") + "?consumer_name=User 1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.json())
        self.assertTrue(
            all("User 1" in acc["consumers"][0]["name"] for acc in response.json()["results"])
        )


class TestImportCSVView(APITestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(name="Test Client")

    def test_import_csv_success(self):
        csv_data = io.StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(
            [
                "client reference no",
                "balance",
                "status",
                "consumer name",
                "consumer address",
                "ssn",
            ]
        )
        csv_writer.writerow(
            [
                str(uuid.uuid4()),
                "1200.75",
                "in_collection",
                "Jane Smith",
                "456 Test Avenue",
                "987-65-4321",
            ]
        )

        csv_data.seek(0)
        csv_file = SimpleUploadedFile(
            "test_accounts.csv",
            csv_data.getvalue().encode("utf-8"),
            content_type="text/csv",
        )
        url = reverse("import-csv")
        response = self.client.post(url, {"file": csv_file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(Consumer.objects.count(), 1)

    def test_import_csv_no_file(self):
        url = reverse("import-csv")
        response = self.client.post(url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No file provided", response.json()["error"])

    def test_import_csv_invalid_format(self):
        csv_file = SimpleUploadedFile(
            "test_invalid.txt", b"invalid content", content_type="text/plain"
        )

        url = reverse("import-csv")
        response = self.client.post(url, {"file": csv_file}, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)