# Airline Information System Pro

A modern airline management application built with **Python, Streamlit, SQLite, and Pandas**. The system provides an interactive web interface for managing flights, handling passenger bookings, generating reports, and maintaining airline records efficiently.

[Live Demo](https://airline-information-system-5ggdxjv7ma7lskt4ctpp8g.streamlit.app/)
---

## Overview

Airline Information System Pro is designed to simulate core airline operations through a user-friendly dashboard. It enables administrators to manage flight schedules, process ticket bookings, cancel reservations, modify flight information, and analyze revenue data.

The application uses **SQLite** for persistent data storage and **Streamlit** for the frontend interface, creating a lightweight yet powerful management system.
---

## Features

### Flight Management

* Add new flights with validation.
* Prevent duplicate flight numbers.
* Modify existing flight information.
* Delete flights with automatic booking cleanup.
* View all available flight schedules.

### Flight Search

* Search by:

  * Flight Number
  * Source and Destination Route
* Instant filtering and display of matching flights.

### Ticket Booking

* Book seats on available flights.
* Automatic seat availability updates.
* Fare calculation based on number of tickets.
* Booking records stored permanently.

### Booking Cancellation

* Cancel reservations using Booking ID.
* Automatically restore cancelled seats to flight inventory.

### Reports & Analytics

* Total revenue generated.
* Total passengers booked.
* Booking transaction statistics.
* Revenue breakdown by flight.
* Interactive revenue charts.

### Database Support

* SQLite database integration.
* Persistent storage of flights and bookings.
* Foreign key constraints for data integrity.

---

## 🛠️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python 3   | Core Programming Language |
| Streamlit  | Web Interface             |
| SQLite     | Database Storage          |
| Pandas     | Data Analysis & Tables    |

---

## 📂 Project Structure

```text
Airline-Information-System/
│
├── airline_app.py      # Main Streamlit Application
├── airline.db          # SQLite Database (auto-generated)
├── README.md
│
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/airline-information-system.git
cd airline-information-system
```

### 2. Create a Virtual Environment (Optional)

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install streamlit pandas
```

---

## ▶️ How to Run

Start the Streamlit application:

```bash
streamlit run airline_app.py
```

After execution, Streamlit will automatically open the application in your browser.

If it does not open automatically, visit:

```text
http://localhost:8501
```

---

## 📘 How to Use

### Dashboard

* Open the application.
* Select **Dashboard** from the sidebar.
* View all available flights and current seat availability.

### Add Flight

* Choose **Add Flight**.
* Enter:

  * Flight Number
  * Source City
  * Destination City
  * Total Seats
  * Fare
* Click **Commit Route to Database**.

### Search Flights

* Choose **Search Flights**.
* Search using:

  * Flight Number
  * Source/Destination Route
* View matching records instantly.

### Book Ticket

* Select **Book Ticket**.
* Choose an available flight.
* Enter passenger name.
* Specify number of seats.
* Click **Process Secure Transaction**.

### Cancel Booking

* Select **Cancel Booking**.
* Enter the Booking ID.
* Confirm cancellation.
* Seats are automatically restored.

### Modify Flight

* Select **Modify / Delete Flight**.
* Choose a flight.
* Update route information or fare.
* Save changes.

### Delete Flight

* Open **Modify / Delete Flight**.
* Navigate to the Delete tab.
* Confirm deletion.
* Related bookings are automatically removed.

### Generate Reports

* Open **Reports**.
* View:

  * Revenue generated
  * Passenger statistics
  * Flight-wise earnings
  * Revenue charts

---

## 🗄️ Database Schema

### Flights Table

| Column          | Type      |
| --------------- | --------- |
| flight_no       | TEXT (PK) |
| source          | TEXT      |
| destination     | TEXT      |
| total_seats     | INTEGER   |
| available_seats | INTEGER   |
| fare            | REAL      |

### Bookings Table

| Column         | Type         |
| -------------- | ------------ |
| booking_id     | INTEGER (PK) |
| flight_no      | TEXT (FK)    |
| passenger_name | TEXT         |
| seats_booked   | INTEGER      |

---

## 🎯 Learning Outcomes

This project demonstrates:

* Database Design with SQLite
* CRUD Operations
* Data Validation
* Streamlit UI Development
* Data Visualization
* Relational Database Concepts
* Python Application Architecture

---

## 📸 Sample Functionalities

✅ Add Flights

✅ Search Flights

✅ Book Tickets

✅ Cancel Reservations

✅ Modify Flight Records

✅ Revenue Analytics

✅ SQLite Database Integration

---

## 👨‍💻 Author

**Aayush Jindal**

GitHub: https://github.com/AayushCode24-7

---

## 📄 License

This project is intended for educational and portfolio purposes.
