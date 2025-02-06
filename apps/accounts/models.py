from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Consumer(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    ssn = models.CharField(max_length=11, unique=True)  # Social Security Number

    def __str__(self):
        return self.name


class Account(models.Model):
    STATUS_CHOICES = [
        ("inactive", "Inactive"),
        ("in_collection", "In Collection"),
        ("paid_in_full", "Paid in Full"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_reference_no = models.UUIDField(unique=True)
    consumers = models.ManyToManyField(Consumer, related_name="accounts")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.client_reference_no} - {self.status}"
