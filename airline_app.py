import sqlite3
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Airline Information System Pro",
    page_icon="✈️",
    layout="wide"
)

# ---------------- DATABASE CONFIGURATION & INITIALIZATION ----------------

def get_connection():
    return sqlite3.connect("airline.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    # FLIGHTS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        flight_no TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        destination TEXT NOT NULL,
        total_seats INTEGER NOT NULL,
        available_seats INTEGER NOT NULL,
        fare REAL NOT NULL
    )
    """)

    # BOOKINGS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_no TEXT NOT NULL,
        passenger_name TEXT NOT NULL,
        seats_booked INTEGER NOT NULL,
        FOREIGN KEY (flight_no) REFERENCES flights(flight_no) ON DELETE CASCADE
    )
    """)

    # Default Seed Data Setup
    cursor.execute("""
    INSERT OR IGNORE INTO flights VALUES ('SD-101','Delhi','Mumbai',120,100,4500)
    """)

    cursor.execute("""
    INSERT OR IGNORE INTO flights VALUES ('SD-202','Pune','Bengaluru',60,39,5200)
    """)
    cursor.execute("""
    INSERT OR IGNORE INTO flights VALUES ('SD-304','Patial','Delhi',80,60,4200)
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- SYSTEM BACKEND FUNCTIONS ----------------

def execute_query(query, params=(), fetch=False, commit=False):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    try:
        cursor.execute(query, params)
        if commit:
            conn.commit()
        if fetch:
            return cursor.fetchall()
    except Exception as e:
        conn.close()
        raise e
    conn.close()


st.title("✈️ Airline Information System")

# Sidebar Menu Router
menu = st.sidebar.selectbox(
    "Operations Management",
    [
        "Dashboard", 
        "Add Flight", 
        "Search Flights", 
        "Book Ticket", 
        "Cancel Booking", 
        "Modify / Delete Flight",
        "Reports"
    ]
)

# 1. Dashboard
if menu == "Dashboard":
    st.header("📋 Current Flight Schedules")
    
    rows = execute_query("SELECT flight_no, source, destination, total_seats, available_seats, fare FROM flights", fetch=True)
    
    if rows:
        df = pd.DataFrame(rows, columns=["Flight No", "Source", "Destination", "Total Seats", "Available Seats", "Fare (₹)"])
        # Format currency mapping to whole number followed by symbol
        df["Fare (₹)"] = df["Fare (₹)"].map("{:.0f}₹".format)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("The hangar is empty. No flights scheduled at the moment.")

# 2. ADD FLIGHT
elif menu == "Add Flight":
    st.header("New Flight")
    
    col1, col2 = st.columns(2)
    with col1:
        no = st.text_input("Flight Number (e.g., AI-204)").strip().upper()
        src = st.text_input("Origin Source City").strip().title()
        dest = st.text_input("Destination City").strip().title()
    with col2:
        total_seats = st.number_input("Total Seat Capacity", min_value=1, step=1, value=180)
        fare = st.number_input("Base Ticket Fare (₹)", min_value=0.0, step=100.0, value=5000.0)

    if st.button("Commit Route to Database", use_container_width=True):
        if not no or not src or not dest:
            st.warning("All spatial parameters must be provided.")
        elif src == dest:
            st.error("Invalid Vector: Origin and Destination cannot match.")
        else:
            try:
                execute_query(
                    "INSERT INTO flights VALUES (?, ?, ?, ?, ?, ?)",
                    (no, src, dest, total_seats, total_seats, fare),
                    commit=True
                )
                st.success(f"Flight Route {no} safely indexed.")
                st.balloons()
            except sqlite3.IntegrityError:
                st.error(f"Collision Error: Flight Number '{no}' is already assigned.")

# 3. SEARCH FLIGHTS
elif menu == "Search Flights":
    st.header("Search")
    
    search_by = st.radio("Filter Metric", ["Route Vectors (Source/Destination)", "Exact Flight ID"], horizontal=True)
    
    if search_by == "Route Vectors (Source/Destination)":
        s_src = st.text_input("Match Source").strip().title()
        s_dest = st.text_input("Match Destination").strip().title()
        
        if st.button("Filter Schedules"):
            query = "SELECT * FROM flights WHERE source LIKE ? AND destination LIKE ?"
            results = execute_query(query, (f"%{s_src}%", f"%{s_dest}%"), fetch=True)
            if results:
                df_res = pd.DataFrame(results, columns=["Flight No", "Source", "Destination", "Total Seats", "Available Seats", "Fare (₹)"])
                df_res["Fare (₹)"] = df_res["Fare (₹)"].map("{:.0f}₹".format)
                st.write(df_res)
            else:
                st.error("No active flights match those geographic coordinates.")
                
    else:
        s_no = st.text_input("Target Flight Number").strip().upper()
        if st.button("Isolate Target"):
            results = execute_query("SELECT * FROM flights WHERE flight_no = ?", (s_no,), fetch=True)
            if results:
                df_res = pd.DataFrame(results, columns=["Flight No", "Source", "Destination", "Total Seats", "Available Seats", "Fare (₹)"])
                df_res["Fare (₹)"] = df_res["Fare (₹)"].map("{:.0f}₹".format)
                st.write(df_res)
            else:
                st.error("Flight Identity Not Found.")

# 4. BOOK TICKET
elif menu == "Book Ticket":
    st.header("Book Ticket")
    
    flights = execute_query("SELECT flight_no, source, destination, available_seats, fare FROM flights WHERE available_seats > 0", fetch=True)
    
    if not flights:
        st.info("No bookings can be transacted. All scheduled flights are at maximum capacity.")
    else:
        flight_options = [f"{f[0]} ({f[1]} ➔ {f[2]}) | Available: {f[3]} | Price: {f[4]:.0f}₹" for f in flights]
        selected_index = st.selectbox("Select Flight Manifest", range(len(flight_options)), format_func=lambda x: flight_options[x])
        
        chosen_flight = flights[selected_index]
        flight_no = chosen_flight[0]
        max_available = chosen_flight[3]
        ticket_price = chosen_flight[4]
        
        p_name = st.text_input("Primary Passenger Name").strip().title()
        seats_to_book = st.number_input("Tickets Requested", min_value=1, max_value=max_available, step=1)
        
        total_cost = seats_to_book * ticket_price
        st.metric(label="Total Transaction Volume", value=f"{total_cost:.0f}₹")
        
        if st.button("Process Secure Transaction", use_container_width=True):
            if not p_name:
                st.warning("Passenger naming constraints require a valid manifest identity.")
            else:
                conn = get_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO bookings (flight_no, passenger_name, seats_booked) VALUES (?, ?, ?)", 
                                   (flight_no, p_name, seats_to_book))
                    cursor.execute("UPDATE flights SET available_seats = available_seats - ? WHERE flight_no = ?", 
                                   (seats_to_book, flight_no))
                    conn.commit()
                    st.success(f"Transaction Clear. Manifest Booked. Booking Reference ID generated.")
                except Exception as e:
                    conn.rollback()
                    st.error(f"Transaction aborted: {e}")
                finally:
                    conn.close()

# 5. CANCEL BOOKING
elif menu == "Cancel Booking":
    st.header("Cancel Booking")
    
    b_id = st.number_input("Enter Transaction Booking ID Reference", min_value=1, step=1)
    
    if st.button("Look up and Revoke Booking", use_container_width=True):
        booking_data = execute_query("SELECT flight_no, seats_booked FROM bookings WHERE booking_id = ?", (b_id,), fetch=True)
        
        if not booking_data:
            st.error("No transactional logs found matching this Booking ID Reference.")
        else:
            f_no, returned_seats = booking_data[0]
            
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (b_id,))
                cursor.execute("UPDATE flights SET available_seats = available_seats + ? WHERE flight_no = ?", (returned_seats, f_no))
                conn.commit()
                st.success(f"Booking Reference ID {b_id} successfully wiped. {returned_seats} seats re-allocated to inventory.")
            except Exception as e:
                conn.rollback()
                st.error(f"Revocation workflow dropped: {e}")
            finally:
                conn.close()

# 6. MODIFY / DELETE FLIGHT
elif menu == "Modify / Delete Flight":
    st.header("Modify Flight")
    
    all_flights = execute_query("SELECT flight_no FROM flights", fetch=True)
    if not all_flights:
        st.info("No structural parameters available to modify.")
    else:
        flight_list = [f[0] for f in all_flights]
        target_flight = st.selectbox("Target Core Flight Element", flight_list)
        
        current_data = execute_query("SELECT * FROM flights WHERE flight_no = ?", (target_flight,), fetch=True)[0]
        
        tab1, tab2 = st.tabs(["Modify Attributes", "System Purge (Delete)"])
        
        with tab1:
            m_src = st.text_input("Alter Source", value=current_data[1]).strip().title()
            m_dest = st.text_input("Alter Destination", value=current_data[2]).strip().title()
            m_fare = st.number_input("Re-evaluate Base Fare (₹)", value=current_data[5], min_value=0.0)
            
            if st.button("Apply Parameters"):
                execute_query(
                    "UPDATE flights SET source = ?, destination = ?, fare = ? WHERE flight_no = ?",
                    (m_src, m_dest, m_fare, target_flight),
                    commit=True
                )
                st.success(f"Flight {target_flight} telemetry altered safely.")
                st.rerun()
                
        with tab2:
            st.warning(f"Purging '{target_flight}' will cascade delete all linked active booking records.")
            if st.button(f"Confirm Destructive Deletion of {target_flight}"):
                execute_query("DELETE FROM flights WHERE flight_no = ?", (target_flight,), commit=True)
                st.success(f"Flight {target_flight} has been completely dropped from the index.")
                st.rerun()

# 7. Reports
elif menu == "Reports":
    st.header("Reports")
    
    report_query = """
        SELECT 
            f.flight_no,
            f.source,
            f.destination,
            COUNT(b.booking_id) as total_booking_transactions,
            TOTAL(b.seats_booked) as aggregate_seats_sold,
            TOTAL(b.seats_booked) * f.fare as gross_revenue_yield
        FROM flights f
        LEFT JOIN bookings b ON f.flight_no = b.flight_no
        GROUP BY f.flight_no
    """
    
    report_rows = execute_query(report_query, fetch=True)
    
    if report_rows:
        df_report = pd.DataFrame(report_rows, columns=[
            "Flight No", "Source", "Destination", "Transaction Count", "Seats Settled", "Gross Revenue (₹)"
        ])
        
        total_revenue = df_report["Gross Revenue (₹)"].sum()
        total_tickets = df_report["Seats Settled"].fillna(0).sum()
        
        m_col1, m_col2 = st.columns(2)
        m_col1.metric("System Gross Revenue Yield", f"{total_revenue:.0f}₹")
        m_col2.metric("Total Passengers Logged", int(total_tickets))
        
        st.subheader("Flight Revenue Yield Breakdown")
        df_display = df_report.copy()
        df_display["Gross Revenue (₹)"] = df_display["Gross Revenue (₹)"].map("{:.0f}₹".format)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.subheader("Revenue Generation Map by Flight Route")
        st.bar_chart(data=df_report, x="Flight No", y="Gross Revenue (₹)", use_container_width=True)
        
    else:
        st.info("Insufficient data layers compiled to produce executive analytics.")