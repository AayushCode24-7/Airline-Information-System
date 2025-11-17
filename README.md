# ✈️ Airline Information System (Python Project)

## 📌 Overview
The Airline Information System is a **Python-based console application** designed to manage flight records.  
It allows users to add, display, book, cancel, delete, and modify flights, as well as generate fare reports.  
This project demonstrates **file handling, input validation, modular design, and robust error handling** in Python.

---

## 🚀 Features
- **Add Flight** → Create new flight records with validation.
- **Duplicate Check** → Prevents adding flights with the same flight number.
- **Display Flights** → Shows all available flights with details.
- **Book Flight** → Reduces available seats after booking.
- **Cancel Booking** → Increases available seats after cancellation.
- **Delete Flight** → Removes a flight record completely.
- **Modify Flight** → Update source, destination, seats, or fare.
- **Fare Report** → Generates the lowest and average fare for a route.
- **Validation** → Ensures seats and fares are positive numbers, prevents invalid inputs.

---

## 🛠️ Technologies Used
- **Python 3.x**
- Concepts:
  - File Handling (`open`, `readlines`, `write`)
  - Exception Handling (`try-except`)
  - Input Validation (`isdigit`, `.replace('.', '', 1).isdigit()`)
  - Modular Functions
  - Loops & Conditionals

---

## 📂 Project Structure
AirlineSystem/
│
├── main.py        # Full Airline Information System code
├── README.md      # Documentation
