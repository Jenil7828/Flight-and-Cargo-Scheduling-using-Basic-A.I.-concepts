# AI-Based Cargo Allocation System

## 📌 Project Overview
This project implements an **AI-based cargo allocation system** that optimally schedules cargo shipments based on flight availability, cargo priority, and cost-effectiveness. The system utilizes **search algorithms and heuristic functions** to recommend the best flights for cargo transport.

## 🚀 Features
- **AI-Powered Flight Selection**: Uses heuristic-based search to allocate cargo to optimal flights.
- **Cargo Management**: Add, view, and allocate cargo dynamically.
- **Flight Scheduling**: Retrieve flight schedules for cargo transportation.
- **Automated Cost Optimization**: Calculates cost based on distance, cargo priority, and flight base cost.
- **User-Friendly Interface**: Provides an interactive web-based UI for cargo scheduling.

## 🏗️ Technologies Used
- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Database**: SQLite / PostgreSQL
- **AI Techniques**: A* Search, Constraint Satisfaction Problems (CSP), Automated Planning

## 🔧 Installation & Setup
### Prerequisites:
- Python 3.x
- Django Framework
- Virtual Environment (optional but recommended)

### Setup Steps:
1. **Clone the repository**:
   ```sh
   git clone https://github.com/Jenil7828/Flight-and-Cargo-Scheduling-using-Basic-A.I.-concepts.git
   cd airline_expert
   ```
2. **Set up a virtual environment** (optional):
   ```sh
   python -m venv venv
   # On Windows use: venv\Scripts\activate
   # On Mac use: source venv/bin/activate 
   ```
3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Run database migrations**:
   ```sh
   python manage.py migrate
   ```
5. **Start the development server**:
   ```sh
   python manage.py runserver
   ```
6. **Access the application** in your browser:
   ```
   http://127.0.0.1:8000/
   ```

## 📂 Project Structure
```
airline_expert/
│-- airline_expert/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│-- scheduling/
│   ├── migrations/
│   ├── templates/
│   │   ├── add_cargo.html
│   │   ├── base.html
│   │   ├── cargo.html
│   │   ├── flights.html
│   │   ├── home.html
│   │   ├── schedule_cargo.html
│   │   ├── schedule_flight.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│-- db.sqlite3
│-- manage.py
```

## 🔬 AI Concepts Covered
- **Search Algorithms**: Uses A* Search to determine optimal flight routes.
- **Heuristic Functions**: Prioritizes cargo allocation based on urgency, cost, and distance.
- **Constraint Satisfaction Problems (CSP)**: Ensures flights meet cargo constraints.
- **Automated Planning**: Allocates resources efficiently while considering scheduling constraints.

## 🤝 Contributing
Want to contribute? Follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-xyz`).
3. Commit your changes.
4. Push to your branch and create a pull request.

## 📞 Contact
For any queries, reach out to:
- **Email**: jenilrathod478@gmail.com
- **GitHub**: [Jenil Rathod](https://github.com/Jenil7828)
