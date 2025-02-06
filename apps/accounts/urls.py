from django.urls import path
from .views import AccountListView, ImportCSVView

urlpatterns = [
    path("", AccountListView.as_view(), name="accounts-list"),
    path("import/", ImportCSVView.as_view(), name="import-csv"),
]
