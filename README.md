# RouteWise 🚚

RouteWise is a full-stack truck route planning and Electronic Logging Device (ELD) management application built for commercial drivers.

The application helps truck drivers plan trips, calculate routes, estimate driving schedules, and generate compliant daily driving logs based on FMCSA Hours of Service (HOS) regulations.

## 🚀 Live Demo

Backend API:
https://ayinla.pythonanywhere.com/

---

# Features

## 🗺️ Smart Route Planning

- Enter:
  - Current location
  - Pickup location
  - Dropoff location
  - Current HOS cycle hours used

- Generate optimized driving routes using OpenRouteService API.

- Calculates:
  - Route distance
  - Estimated travel duration
  - Required stops

---

## 📋 ELD Log Generation

RouteWise generates driver daily logs based on FMCSA property-carrying driver rules:

- 70 hours / 8 days cycle
- 11-hour driving limit
- 14-hour duty window
- 30-minute break requirements

The system helps drivers visualize their daily activities:

- Driving
- Sleeper berth
- On-duty
- Rest periods

---

## 🔐 Authentication

Implemented using:

- Django REST Framework
- JWT Authentication
- Simple JWT

Features:

- Secure login
- Token-based authentication
- Protected API endpoints

---

# Tech Stack

## Backend

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite (development)
- PostgreSQL ready
- OpenRouteService API


## Deployment

Backend:
- PythonAnywhere

---

# Project Architecture

```
route_backend/

│
├── backend/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── trips/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── routing/
│   ├── services.py
│   ├── views.py
│   └── urls.py
│
├── eld_logs/
│   ├── models.py
│   └── services.py
│
├── manage.py
└── requirements.txt
```

---

# API Endpoints

## Authentication

### Obtain JWT Token

```
POST /api/token/
```

Request:

```json
{
    "username": "driver",
    "password": "password"
}
```

Response:

```json
{
    "access": "jwt_access_token",
    "refresh": "jwt_refresh_token"
}
```

---

## Trips

### Create Trip

```
POST /api/trips/
```

Example:

```json
{
    "current_location": "Dallas, TX",
    "pickup_location": "Fort Worth, TX",
    "dropoff_location": "Houston, TX",
    "current_cycle_used": 18
}
```

---

## Generate Route

```
GET /api/routing/<trip_id>/
```

Returns:

- Route information
- Distance
- Duration
- Driving schedule
- ELD log information

---

# Installation Guide

## Clone Repository

```bash
git clone https://github.com/Olukoyataiwohammed/route_backend.git

cd route_backend
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

Windows:

```bash
venv\Scripts\activate
```



---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key

ORS_API_KEY=your_openrouteservice_api_key
```

---

## Run Database Migration

```bash
python manage.py migrate
```

---

## Create Admin User

```bash
python manage.py createsuperuser
```

---

## Start Development Server

```bash
python manage.py runserver
```

Backend runs at:

```
http://127.0.0.1:8000/
```

---

# Future Improvements

- Real truck-specific routing
- Interactive map visualization
- PDF ELD log export
- Driver profiles
- Fuel stop optimization
- PostgreSQL production database
- Real-time weather and traffic integration

---

# Author

**Taiwo Olukoya**

Full Stack Developer

GitHub:
https://github.com/Olukoyataiwohammed
