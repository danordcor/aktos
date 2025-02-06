import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.accounts.utils import process_csv_data

def import_consumers_balance():
    file_path = os.path.join(os.getcwd(), "consumers_balances.csv")

    if not os.path.exists(file_path):
        print("Error: The file 'consumers_balance.csv' was not found in the project root.")
        return

    try:
        with open(file_path, "rb") as file:
            response = process_csv_data(file)
            print(response.content.decode("utf-8"))

    except Exception as e:
        print(f"Error processing the file: {str(e)}")


if __name__ == "__main__":
    import_consumers_balance()