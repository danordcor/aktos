# **Aktos System** 🚀

Welcome to **Aktos System**, a Django-based application designed for **managing accounts, debts, and consumers**. This system provides **RESTful API endpoints** to interact with the data and supports **PostgreSQL and Docker Compose** for an easy setup.

---

## **📌 Local Setup**

Follow these steps to **set up the project locally using Docker Compose**.

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/danordcor/aktos
cd aktos
```

### **2️⃣ Build the Docker Images**
```bash
docker-compose build
```

### **3️⃣ Run Migrations to Set Up the Database**
```bash
docker-compose run web python manage.py migrate
```

### **4️⃣ Create a Superuser for Admin Access**
```bash
docker-compose run web python manage.py createsuperuser
```

### **5️⃣ Populate Initial Data (Roles, Examples)**
```bash
docker-compose run web python populate_data.py
```

### **6️⃣ Start the Development Server**
```bash
docker-compose up
```
- The app will be available at: **[http://localhost:8080](http://localhost:8080)**
- Admin panel: **[http://localhost:8080/admin](http://localhost:8080/admin)**

---

## **📌 Running Tests**
To run the **Django test suite** inside Docker:
```bash
docker-compose run web python manage.py test
```

---

## **📌 API Documentation**

### **Base URL**
For local development, use:
```
http://localhost:8080/api/v1/
```

### **1️⃣ Accounts Endpoint**
#### **GET /accounts/**
Retrieve all accounts, with optional filters.

#### **Query Parameters:**
| Parameter       | Type     | Description                                        |
|---------------|---------|------------------------------------------------|
| `min_balance` | float   | Filter accounts with a balance greater than or equal to this value. |
| `max_balance` | float   | Filter accounts with a balance less than or equal to this value. |
| `consumer_name` | string | Filter accounts by consumer name. |
| `status`      | string  | Filter accounts by status (`in_collection`, `paid_in_full`, etc.). |

#### **Example Requests:**
```bash
curl "http://localhost:8080/api/v1/accounts?min_balance=100&max_balance=1000"
```

---

### **2️⃣ Import CSV Data**
#### **POST /accounts/import/**
Allows **bulk importing of accounts** from a CSV file.

#### **Expected CSV Format**
```
client reference no,balance,status,consumer name,consumer address,ssn
ffeb5d88-e5af-45f0-9637-16ea469c58c0,59638.99,INACTIVE,Jessica Williams,"0233 Edwards Glens",018-79-4253
```

#### **Example Request**
```bash
curl -X POST http://localhost:8080/api/v1/accounts/import/ \
     -H "Content-Type: multipart/form-data" \
     -F "file=@data.csv"
```

---

## **📌 Environment Variables**
Ensure your `.env` file contains:
```
DEBUG=True
SECRET_KEY=mysecretkey
DB_NAME=dbname
DB_USER=dbuser
DB_PASSWORD=dbpassword
DB_HOST=db
DB_PORT=5432
POSTGRES_PASSWORD=dbpassword
```

---

## **🚀 Summary**
✅ **Easy local setup using Docker Compose**
✅ **API endpoints for managing accounts and consumers**
✅ **CSV file import support**

Now you're **ready to use Aktos System!** 🎉🚀
If you have any issues, feel free to open a GitHub issue! 😊
