from django.contrib import admin
from .models import Client, Consumer, Account


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "ssn", "address")
    search_fields = ("name", "ssn")
    ordering = ("name",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "client_reference_no", "balance", "status")
    search_fields = ("client__name", "client_reference_no", "status")
    list_filter = ("status", "client")
    ordering = ("client", "status")
    filter_horizontal = ("consumers",)


admin.site.site_header = "Aktos accounts administration"
