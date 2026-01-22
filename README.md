# Hospital Management System API

A comprehensive REST API built with FastAPI for managing hospital operations, including patient records, doctor information, admin authentication, and insurance premium prediction using machine learning.

## Features

- **Patient Management**: Complete CRUD operations for patient records
- **Doctor Management**: Manage doctor profiles and specialties
- **Admin Authentication**: Secure JWT-based authentication for admin users
- **Insurance Premium Prediction**: ML-powered insurance premium category prediction based on user demographics and lifestyle factors
- **PostgreSQL Database**: Robust database management with SQLAlchemy ORM
- **RESTful API**: Well-structured API endpoints following REST principles
- **Streamlit Frontend**: User-friendly web interface for all operations

## Frontend Features

The Streamlit frontend provides an intuitive interface for:

- **Dashboard**: Overview and quick access to all features
- **Patient Management**: 
  - Create, view, update, and delete patient records
  - View list of all patients with pagination
- **Doctor Management**:
  - Create, view, update, and delete doctor profiles
  - Manage doctor specialties
- **Insurance Premium Prediction**:
  - Interactive form for user input
  - Real-time BMI and risk calculations
  - Visual probability distribution
  - Model health status
- **Settings**: Configure API URL and manage session

## Tech Stack

- **Backend Framework**: FastAPI 0.126.0
- **Frontend Framework**: Streamlit 1.39.0
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0.45
- **Authentication**: JWT (python-jose), bcrypt
- **Machine Learning**: scikit-learn, pandas, numpy
- **Server**: Uvicorn
- **HTTP Client**: requests

## Prerequisites

- Python 3.11+
- PostgreSQL database
- pip (Python package manager)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On Linux/Mac:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

1. **Install PostgreSQL** and ensure it's running on your system

2. **Create a database**:
   ```sql
   CREATE DATABASE hospital_management;
   ```

3. **Update database connection** in `database.py`:
   ```python
   SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost:5432/hospital_management"
   ```
   Replace `username` and `password` with your PostgreSQL credentials.

4. **Database tables** will be created automatically when you run the application (via `schemas.Base.metadata.create_all(bind=engine)` in `main.py`)

## Running the Application

### Backend (FastAPI)

1. **Start the FastAPI server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Interactive API Documentation (Swagger UI): `http://localhost:8000/docs`
   - Alternative API Documentation (ReDoc): `http://localhost:8000/redoc`

### Frontend (Streamlit)

1. **Make sure the FastAPI server is running** (see above)

2. **Start the Streamlit application**:
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Access the frontend**:
   - The Streamlit app will open automatically in your browser at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in the terminal

4. **Login**:
   - If you don't have an admin account, create one using the "Create New Admin Account" form on the login page
   - Then login with your credentials to access the dashboard

## API Endpoints

### Health Check
- `GET /` - Welcome message
- `GET /check-connection` - Database connection status

### Admin Authentication
- `POST /admin/add` - Create a new admin user
- `POST /admin/token` - Login and get JWT access token

### Patient Management
- `POST /patients/patient/` - Create a new patient
- `GET /patients/patient/{patient_id}` - Get patient by ID
- `GET /patients/patients_list/{limit}` - Get list of patients (with limit)
- `PUT /patients/patient_id/{id}` - Update patient information
- `DELETE /patients/patient_id/{id}` - Delete a patient

### Doctor Management
- `POST /doctors/doctor/` - Create a new doctor
- `GET /doctors/doctor/{doctor_id}` - Get doctor by ID
- `PUT /doctors/doctor_id/{id}` - Update doctor information
- `DELETE /doctors/doctor_id/{id}` - Delete a doctor

### Insurance Premium Prediction
- `GET /insurance_premium/` - API information
- `GET /insurance_premium/health` - Health check with model version
- `POST /insurance_premium/predict` - Predict insurance premium category

## Usage Examples

### 1. Create an Admin User
```bash
curl -X POST "http://localhost:8000/admin/add" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "securepassword123"
  }'
```

### 2. Login and Get Token
```bash
curl -X POST "http://localhost:8000/admin/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=securepassword123"
```

### 3. Create a Patient
```bash
curl -X POST "http://localhost:8000/patients/patient/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 35,
    "weight": 75.5,
    "height": 1.75
  }'
```

### 4. Create a Doctor
```bash
curl -X POST "http://localhost:8000/doctors/doctor/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Jane Smith",
    "specialty": "Cardiology"
  }'
```

### 5. Predict Insurance Premium
```bash
curl -X POST "http://localhost:8000/insurance_premium/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "weight": 75.5,
    "height": 1.75,
    "income_lpa": 12.5,
    "smoker": false,
    "city": "Mumbai",
    "occupation": "Engineer"
  }'
```

## Insurance Premium Prediction Model

The insurance premium prediction endpoint uses a machine learning model to predict premium categories (Low, Medium, High) based on:

- **Age**: User's age (0-120)
- **Weight**: Weight in kg
- **Height**: Height in meters (0-2.5)
- **Income**: Annual income in LPA (Lakhs Per Annum)
- **Smoker**: Boolean indicating smoking status
- **City**: City name (automatically categorized into tier 1, 2, or 3)
- **Occupation**: One of: Engineer, Driver, Teacher, Banker, Sales Manager, Businessman, Factory Worker

The model automatically calculates:
- **BMI**: Body Mass Index
- **Lifestyle Risk**: Low, Medium, or High based on smoking and BMI
- **Age Group**: young, adult, middle_aged, or senior
- **City Tier**: 1, 2, or 3 based on city classification

## Project Structure

```
FastAPI/
├── main.py                 # FastAPI application entry point
├── streamlit_app.py        # Streamlit frontend application
├── database.py            # Database connection and configuration
├── database_models.py      # Database models (legacy)
├── schemas.py             # Pydantic models and SQLAlchemy models
├── requirements.txt       # Python dependencies
├── router/
│   ├── auth.py           # Admin authentication routes
│   ├── patients.py       # Patient management routes
│   ├── doctors.py        # Doctor management routes
│   └── insurance.py      # Insurance premium prediction routes
└── model/
    ├── model1.pkl        # Trained ML model
    └── predict.py        # Prediction logic
```

## Security Notes

- **JWT Secret Key**: The current secret key in `router/auth.py` should be changed in production. Use a secure, randomly generated key.
- **Password Hashing**: Passwords are hashed using bcrypt before storage.
- **Token Expiration**: Access tokens expire after 20 minutes (configurable).

## Development

- The API uses automatic database table creation on startup
- CORS middleware is commented out but available for frontend integration
- The application runs in development mode with auto-reload enabled

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available for use.

## Support

For issues and questions, please open an issue in the repository.
