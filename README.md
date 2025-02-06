# Aktos System

Welcome!

## Local Setup

Follow these steps to set up the project locally using Docker Compose.

1. Clone the repository:

   ```bash
   git clone https://github.com/danordcor/aktos
   cd aktos
   ```

2. Build the Docker images:

   ```bash
   docker-compose build
   ```

3. Run migrations to set up the database:

   ```bash
   docker-compose run web python manage.py migrate
   ```
4. Create a superuser account for admin access:

   ```bash
   docker-compose run web python manage.py createsuperuser
   ```

5. Create initial data, for roles and examples:

   ```bash
   docker-compose run web python populate_data.py
   ```

6. Run the development server using Docker Compose:

   ```bash
   docker-compose up
   ```

## Running Tests

Follow these steps to run tests within the Docker environment.

1. Run tests:

   ```bash
   docker-compose run web python manage.py test
   ```
