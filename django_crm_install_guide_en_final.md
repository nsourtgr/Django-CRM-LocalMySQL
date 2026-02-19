# Django-CRM-LocalMySQL Installation Guide (English)

This guide explains how to install **Django-CRM-LocalMySQL** on a new PC with **local MySQL** and Docker. Note: The database contains only the schema, no data.

---

## 1️⃣ Prerequisites

1. Docker & Docker Compose
2. Git
3. Local MySQL (database contains only the schema)

---

## 2️⃣ Clone repository

```bash
git clone https://github.com/nsourtgr/Django-CRM-LocalMySQL.git
cd Django-CRM-LocalMySQL
```

---

## 3️⃣ Create .env

Create a `.env` file with the same credentials as on the first PC:

```
DB_NAME=dcrm_db
DB_USER=dcrm_user
DB_PASSWORD=password123
DB_HOST=host.docker.internal
DB_PORT=3306
SECRET_KEY=<same secret key>
DEBUG=True
```

---

## 4️⃣ Run Docker container

```bash
docker-compose up --build
```
- Django will run at `http://127.0.0.1:8001/`
- The container_name in docker-compose.yml is `dcrm_web`

---

## 5️⃣ Run migrations

Since the database contains only the schema, you need to run migrations to create the tables:

```bash
docker exec -it dcrm_web bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6️⃣ Create superuser (optional)

```bash
docker exec -it dcrm_web bash
python manage.py createsuperuser
```

---

## 7️⃣ Access the site

- Site: `http://127.0.0.1:8001/`
- Admin: `http://127.0.0.1:8001/admin/`

---

## 8️⃣ Important Notes

1. Python is not needed on the host; the container includes all dependencies.
2. MySQL is outside Docker.
3. The `.env` file must have the same credentials and secret key.