# Name - [Aayush Jindal]
# Airline Information System
# Features: Add, Search, Book, Cancel, Modify, Delete flights and generate fare reports

# Password protection
import getpass
while True:
    password = getpass.getpass('Enter Your Password: ')
    rewrite_pass = getpass.getpass('Rewrite Your Password: ')
    if rewrite_pass == password:
        print("Password Matched.")
        break
    else:
        print("Password Does Not Match. Try again.\n")
        
# Dictionary For Flights

flights = [
    {'no': 'SD-101', 'src': 'Delhi', 'dest': 'Mumbai', 'seats': 120, 'fare': 4500},
    {'no': 'SD-202', 'src': 'Pune', 'dest': 'Bengaluru', 'seats': 60, 'fare': 5200}
]

# Function to add a new flight record
def add_flight():
    print("\n--- Add Flight ---")
    no = input("Enter Flight Number: ").strip()
    src = input("Enter Source: ").title()
    dest = input("Enter Destination: ").title()
    try:
        seats = int(input("Enter Available Seats: "))
        fare = float(input("Enter Fare: "))
        if seats<0 or fare<0:
            print("Enter Valid Input. /n")
            return
    except ValueError:
        print("Invalid input. Seats and fare should be numeric.\n")
        return

    flights.append({'no': no, 'src': src, 'dest': dest, 'seats': seats, 'fare': fare})
    print(f"Flight {no} added successfully!\n")

# Function to search for flights by source and destination
def search_flights():
    print("\n--- Search Flights ---")
    src = input("From: ").strip().title()
    dest = input("To: ").strip().title()
    found = False
    for f in flights:
        if f['src'] == src and f['dest'] == dest:
            print(f"Match: {f['no']} | Seats: {f['seats']} | Fare: ₹{f['fare']}")
            found = True
    if not found:
        print("No matching flights.\n")

# Function to book tickets for a selected flight
def book_flight():
    print("\n--- Book Flight ---")
    src = input("From: ").strip().title()
    dest = input("To: ").strip().title()
    try:
        p = int(input("Passengers: "))
    except ValueError:
        print("Invalid number of passengers.")
        return

    for f in flights:
        if f['src'] == src and f['dest'] == dest:
            if p <= f['seats']:
                total = p * f['fare']
                f['seats'] -= p
                print(f"Booking Confirmed for Flight {f['no']}")
                print(f"Total Fare = ₹{total}")
                print(f"Seats Remaining = {f['seats']}\n")
            else:
                print("Not enough seats available.\n")
            return
    print("Flight not found.\n")

# Function to cancel booked seats
def cancel_booking():
    print("\n--- Cancel Booking ---")
    no = input("Enter Flight Number: ").strip()
    try:
        p = int(input("Passengers to Cancel: "))
    except ValueError:
        print("Invalid input.\n")
        return
    for f in flights:
        if f['no'] == no:
            f['seats'] += p
            print(f"Cancelled {p} seats on {no}. Seats now available: {f['seats']}\n")
            return
    print("Flight not found.\n")

# Function to modify existing flight details
def modify_flight():
    print("\n--- Modify Flight ---")
    no = input("Enter Flight Number: ").strip()
    for f in flights:
        if f['no'] == no:
            print("Leave blank to keep old value.")
            src = input(f"New Source ({f['src']}): ").strip()
            dest = input(f"New Destination ({f['dest']}): ").strip()
            seats = input(f"New Seats ({f['seats']}): ").strip()
            fare = input(f"New Fare ({f['fare']}): ").strip()
            if src:
                f['src'] = src.title()
            if dest:
                f['dest'] = dest.title()
            if seats.isdigit():
                f['seats'] = int(seats)
            if fare.replace('.', '', 1).isdigit():
                f['fare'] = float(fare)
            print("Flight details updated.\n")
            return
    print("Flight not found.\n")

# Function to delete a flight record
def delete_flight():
    print("\n--- Delete Flight ---")
    no = input("Enter Flight Number: ").strip()
    for f in flights:
        if f['no'] == no:
            flights.remove(f)
            print(f"Flight {no} deleted.\n")
            return
    print("Flight not found.\n")

# Function to display the lowest fare for a given route
def lowest_fare():
    print("\n--- Lowest Fare Report ---")
    src = input("From: ").strip().title()
    dest = input("To: ").strip().title()
    fares = [f['fare'] for f in flights if f['src'] == src and f['dest'] == dest]
    if fares:
        print(f"Lowest Fare {src} → {dest}: ₹{min(fares)}\n")
    else:
        print("No flights found.\n")

# Function to display the average fare for a given route
def average_fare():
    print("\n--- Average Fare Report ---")
    src = input("From: ").strip().title()
    dest = input("To: ").strip().title()
    fares = [f['fare'] for f in flights if f['src'] == src and f['dest'] == dest]
    if fares:
        avg = sum(fares) / len(fares)
        print(f"Average Fare {src} → {dest}: ₹{avg:.2f}\n")
    else:
        print("No flights found.\n")

# Main program loop
while True:
    print("====== Airline Information System ======")
    print("1. Add Flight")
    print("2. Search Flights")
    print("3. Book Flight")
    print("4. Cancel Booking")
    print("5. Modify Flight")
    print("6. Delete Flight")
    print("7. Lowest Fare")
    print("8. Average Fare")
    print("9. Exit")

    ch = input("Enter your choice: ").strip()

    if ch == '1':
        add_flight()
    elif ch == '2':
        search_flights()
    elif ch == '3':
        book_flight()
    elif ch == '4':
        cancel_booking()
    elif ch == '5':
        modify_flight()
    elif ch == '6':
        delete_flight()
    elif ch == '7':
        lowest_fare()
    elif ch == '8':
        average_fare()
    elif ch == '9':
        print("Exiting Have a nice day!")
        break
    else:
        print("Invalid choice! Please try again.\n")
