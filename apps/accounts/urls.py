from django.urls import path
from .views import AccountListView, ImportCSVView

urlpatterns = [
    path("accounts/", AccountListView.as_view(), name="accounts-list"),
    path("accounts/import/", ImportCSVView.as_view(), name="import-csv"),
]
