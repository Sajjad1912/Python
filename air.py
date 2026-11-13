import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ====== DATABASE SETUP ======
conn = sqlite3.connect("airline.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    flight_no TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    seats INTEGER NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    passenger_name TEXT NOT NULL,
    flight_id INTEGER NOT NULL,
    FOREIGN KEY(flight_id) REFERENCES flights(id)
)
""")
conn.commit()

# ====== FUNCTIONS ======
def add_flight():
    if not flight_no_var.get() or not origin_var.get() or not destination_var.get() or not seats_var.get():
        messagebox.showerror("Error", "All flight fields are required")
        return
    try:
        seats = int(seats_var.get())
    except ValueError:
        messagebox.showerror("Error", "Seats must be a number")
        return
    cursor.execute("INSERT INTO flights (flight_no, origin, destination, seats) VALUES (?, ?, ?, ?)",
                   (flight_no_var.get(), origin_var.get(), destination_var.get(), seats))
    conn.commit()
    messagebox.showinfo("Success", "Flight added successfully")
    view_flights()
    clear_flight_fields()

def view_flights():
    for row in flight_table.get_children():
        flight_table.delete(row)
    cursor.execute("SELECT * FROM flights")
    for row in cursor.fetchall():
        flight_table.insert("", tk.END, values=row)

def book_flight():
    if not passenger_name_var.get() or not booking_flight_id_var.get():
        messagebox.showerror("Error", "Passenger name and flight ID are required")
        return
    try:
        flight_id = int(booking_flight_id_var.get())
    except ValueError:
        messagebox.showerror("Error", "Flight ID must be a number")
        return

    cursor.execute("SELECT seats FROM flights WHERE id = ?", (flight_id,))
    result = cursor.fetchone()
    if not result:
        messagebox.showerror("Error", "Flight not found")
        return
    if result[0] <= 0:
        messagebox.showerror("Error", "No seats available")
        return

    cursor.execute("INSERT INTO bookings (passenger_name, flight_id) VALUES (?, ?)",
                   (passenger_name_var.get(), flight_id))
    cursor.execute("UPDATE flights SET seats = seats - 1 WHERE id = ?", (flight_id,))
    conn.commit()
    messagebox.showinfo("Success", "Booking successful")
    view_bookings()
    view_flights()
    clear_booking_fields()

def view_bookings():
    for row in booking_table.get_children():
        booking_table.delete(row)
        cursor.execute("""
        SELECT bookings.id, passenger_name, flights.flight_no, flights.origin, flights.destination
        FROM bookings
        JOIN flights ON bookings.flight_id = flights.id
         """)
    for row in cursor.fetchall():
        booking_table.insert("", tk.END, values=row)

def cancel_booking():
    selected = booking_table.selection()
    if not selected:
        messagebox.showerror("Error", "Select a booking to cancel")
        return
    booking_id = booking_table.item(selected[0])['values'][0]
    flight_no = booking_table.item(selected[0])['values'][2]

    # Get flight ID
    cursor.execute("SELECT id FROM flights WHERE flight_no = ?", (flight_no,))
    flight = cursor.fetchone()
    if not flight:
        messagebox.showerror("Error", "Flight not found for this booking")
        return

    # Delete booking & increase seat count
    cursor.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
    cursor.execute("UPDATE flights SET seats = seats + 1 WHERE id = ?", (flight[0],))
    conn.commit()
    messagebox.showinfo("Success", "Booking cancelled")
    view_bookings()
    view_flights()

def clear_flight_fields():
    flight_no_var.set("")
    origin_var.set("")
    destination_var.set("")
    seats_var.set("")

def clear_booking_fields():
    passenger_name_var.set("")
    booking_flight_id_var.set("")

# ====== GUI ======
root = tk.Tk()
root.title("Simple Airline Reservation System")
root.geometry("800x500")

# ====== FLIGHT MANAGEMENT ======
tk.Label(root, text="--- Add Flight ---", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
tk.Label(root, text="Flight No").grid(row=1, column=0, sticky="e")
tk.Label(root, text="Origin").grid(row=2, column=0, sticky="e")
tk.Label(root, text="Destination").grid(row=3, column=0, sticky="e")
tk.Label(root, text="Seats").grid(row=4, column=0, sticky="e")

flight_no_var = tk.StringVar()
origin_var = tk.StringVar()
destination_var = tk.StringVar()
seats_var = tk.StringVar()

tk.Entry(root, textvariable=flight_no_var).grid(row=1, column=1)
tk.Entry(root, textvariable=origin_var).grid(row=2, column=1)
tk.Entry(root, textvariable=destination_var).grid(row=3, column=1)
tk.Entry(root, textvariable=seats_var).grid(row=4, column=1)

tk.Button(root, text="Add Flight", command=add_flight).grid(row=5, column=0, columnspan=2, pady=5)

flight_table = ttk.Treeview(root, columns=("ID", "Flight No", "Origin", "Destination", "Seats"), show="headings")
for col in ("ID", "Flight No", "Origin", "Destination", "Seats"):
    flight_table.heading(col, text=col)
flight_table.grid(row=0, column=3, rowspan=6, padx=10, pady=5)

# ====== BOOKING MANAGEMENT ======
tk.Label(root, text="--- Book Flight ---", font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=5)
tk.Label(root, text="Passenger Name").grid(row=7, column=0, sticky="e")
tk.Label(root, text="Flight ID").grid(row=8, column=0, sticky="e")

passenger_name_var = tk.StringVar()
booking_flight_id_var = tk.StringVar()

tk.Entry(root, textvariable=passenger_name_var).grid(row=7, column=1)
tk.Entry(root, textvariable=booking_flight_id_var).grid(row=8, column=1)

tk.Button(root, text="Book Flight", command=book_flight).grid(row=9, column=0, columnspan=2, pady=5)

booking_table = ttk.Treeview(root, columns=("ID", "Passenger", "Flight No", "Origin", "Destination"), show="headings")
for col in ("ID", "Passenger", "Flight No", "Origin", "Destination"):
    booking_table.heading(col, text=col)
booking_table.grid(row=6, column=3, rowspan=4, padx=10, pady=5)

tk.Button(root, text="Cancel Booking", command=cancel_booking).grid(row=10, column=3, pady=5)

view_flights()
view_bookings()
root.mainloop()
