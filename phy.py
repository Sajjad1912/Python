import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ====== DATABASE SETUP ======
conn = sqlite3.connect("pharmacy.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS medicines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    quantity INTEGER NOT NULL,
    mfg_date TEXT NOT NULL,
    exp_date TEXT NOT NULL
)
''')
conn.commit()

# ====== FUNCTIONS ======
def add_medicine():
    name = name_var.get()
    price = price_var.get()
    quantity = quantity_var.get()
    mfg_date = mfg_var.get()
    exp_date = exp_var.get()

    if name == "" or price == "" or quantity == "" or mfg_date == "" or exp_date == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    cursor.execute("INSERT INTO medicines (name, price, quantity, mfg_date, exp_date) VALUES (?, ?, ?, ?, ?)", 
                   (name, float(price), int(quantity), mfg_date, exp_date))
    conn.commit()
    messagebox.showinfo("Success", "Medicine added successfully!")
    view_medicines()
    clear_fields()

def view_medicines():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM medicines")
    for medicine in cursor.fetchall():
        tree.insert("", tk.END, values=medicine)

def delete_medicine():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a medicine to delete!")
        return
    medicine_id = tree.item(selected_item)["values"][0]
    cursor.execute("DELETE FROM medicines WHERE id = ?", (medicine_id,))
    conn.commit()
    messagebox.showinfo("Success", "Medicine deleted successfully!")
    view_medicines()

def update_medicine():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select a medicine to update!")
        return

    medicine_id = tree.item(selected_item)["values"][0]
    name = name_var.get()
    price = price_var.get()
    quantity = quantity_var.get()
    mfg_date = mfg_var.get()
    exp_date = exp_var.get()

    if name == "" or price == "" or quantity == "" or mfg_date == "" or exp_date == "":
        messagebox.showerror("Error", "All fields are required!")
        return

    cursor.execute("UPDATE medicines SET name = ?, price = ?, quantity = ?, mfg_date = ?, exp_date = ? WHERE id = ?", 
                   (name, float(price), int(quantity), mfg_date, exp_date, medicine_id))
    conn.commit()
    messagebox.showinfo("Success", "Medicine updated successfully!")
    view_medicines()
    clear_fields()

def clear_fields():
    name_var.set("")
    price_var.set("")
    quantity_var.set("")
    mfg_var.set("")
    exp_var.set("")

# ====== GUI ======
root = tk.Tk()
root.title("Pharmacy Management System")
root.geometry("1200x500")

# Input fields
name_var = tk.StringVar()
price_var = tk.StringVar()
quantity_var = tk.StringVar()
mfg_var = tk.StringVar()
exp_var = tk.StringVar()

tk.Label(root, text="Medicine Name").grid(row=0, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Price").grid(row=1, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=price_var).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Quantity").grid(row=2, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=quantity_var).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Manufacturing Date (YYYY-MM-DD)").grid(row=3, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=mfg_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Expiry Date (YYYY-MM-DD)").grid(row=4, column=0, padx=10, pady=5)
tk.Entry(root, textvariable=exp_var).grid(row=4, column=1, padx=10, pady=5)

# Buttons
tk.Button(root, text="Add Medicine", command=add_medicine).grid(row=0, column=2, padx=10)
tk.Button(root, text="Update Medicine", command=update_medicine).grid(row=1, column=2, padx=10)
tk.Button(root, text="Delete Medicine", command=delete_medicine).grid(row=2, column=2, padx=10)

# Table
tree = ttk.Treeview(root, columns=("ID", "Name", "Price", "Quantity", "Mfg Date", "Exp Date"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.heading("Quantity", text="Quantity")
tree.heading("Mfg Date", text="Mfg Date")
tree.heading("Exp Date", text="Exp Date")
tree.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

view_medicines()

root.mainloop()
