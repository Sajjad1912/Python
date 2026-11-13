import sqlite3

# -------------------------------
# Connect to SQLite Database
# -------------------------------
conn = sqlite3.connect("university.db")
cursor = conn.cursor()

# -------------------------------
# 1. Create Tables
# -------------------------------

# Student Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Student (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    department TEXT
);
""")

# Instructor Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Instructor (
    instructor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    instructor_name TEXT,
    email TEXT
);
""")

# Course Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_name TEXT,
    credit INT,
    instructor_id INT,
    FOREIGN KEY (instructor_id) REFERENCES Instructor(instructor_id)
);
""")

# Registration Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS Registration (
    reg_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INT,
    course_id INT,
    semester TEXT,
    grade TEXT,
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);
""")

# Students Table for Insert/Update/Delete example
cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    cgpa REAL
);
""")

# Customers & Orders Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    email TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INT,
    order_date TEXT,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
""")

# -------------------------------
# 2. Insert / Update / Delete on Students
# -------------------------------

# Insert
cursor.execute("INSERT OR REPLACE INTO Students (student_id, name, department, cgpa) VALUES (2301, 'Sanjida', 'CSE', 3.65)")

# Update
cursor.execute("UPDATE Students SET cgpa = 3.85 WHERE student_id = 2301")

# Delete
cursor.execute("DELETE FROM Students WHERE student_id = 2301")

# -------------------------------
# 3. Insert Dummy Data for Join Example
# -------------------------------
cursor.execute("INSERT INTO Customers (customer_name, email) VALUES ('Rahim', 'rahim@example.com')")
cursor.execute("INSERT INTO Customers (customer_name, email) VALUES ('Karim', 'karim@example.com')")

cursor.execute("INSERT INTO Orders (customer_id, order_date) VALUES (1, '2025-09-08')")
cursor.execute("INSERT INTO Orders (customer_id, order_date) VALUES (2, '2025-09-09')")

# -------------------------------
# 4. Run JOIN Query
# -------------------------------
print("\nAll Orders with Customer Details:\n")
cursor.execute("""
SELECT Orders.order_id, Orders.order_date, Customers.customer_name, Customers.email
FROM Orders
JOIN Customers ON Orders.customer_id = Customers.customer_id;
""")

for row in cursor.fetchall():
    print(row)

# -------------------------------
# Commit and Close
# -------------------------------
conn.commit()
conn.close()