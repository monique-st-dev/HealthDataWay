# HealthDataWay

**HealthDataWay** is a modern Django web platform for tracking health indicators. It allows doctors and patients to connect, manage appointments, and view health data in a clean and professional interface. The project supports internal notifications and a clear role-based access system.

---

## Key Features

- Registration and login with role selection (patient or doctor)
- Doctors can send connection requests to patients
- Patients can accept or reject connection requests
- Patients can create appointment requests
- Doctors can approve or reject appointments
- Patients can record health data (blood sugar, blood pressure, pulse)
- Internal notifications (no emails)
- Dockerized setup with PostgreSQL, Redis and Celery
- Basic testing with `pytest`

---

## Project Structure


```
HealthDataWay/
├── src/
│ ├── accounts/ 
│ ├── appointments/ 
│ ├── charts/ 
│ ├── common/ 
│ ├── config/ 
│ ├── connections/ 
│ ├── dashboards/ 
│ ├── notifications/ 
│ ├── records/ 
│ └── tests/ 
│
├── templates/ 
├── static/ 
├── media/ 
├── manage.py
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```


---

## Technologies Used

- **Python 3.12**
- **Django 5.2**
- **PostgreSQL 15** 
- **Celery + Redis** 
- **Bootstrap 5**, 
- **Docker Compose** 
- **pytest** 

---

## Getting Started (Locally)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/HealthDataWay.git
   cd HealthDataWay


2. **Create your environment file:**
    ```bash
    cp .env.example .env
   
3. **Start the project with Docker:**
    ```bash
    docker-compose up --build

4. **Run migrations and create superuser:**
    ```bash
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser

5. **Start the Celery worker:**
    ```bash
    docker-compose exec web celery -A config worker -l info


Author
Created by Monik 
Final project for the Django Advanced Course – SoftUni 2025
