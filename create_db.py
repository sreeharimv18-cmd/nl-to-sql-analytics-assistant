import sqlite3

# 1. Connect to (or create) a database file named placement.db
connection = sqlite3.connect("placement.db")
cursor = connection.cursor()

# 2. Create a simple 'students' table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    branch TEXT,
    cgpa REAL,
    package_lpa REAL
)
""")

# 3. Add 5 sample student records
sample_students = [
    (1, "Arjun Nair", "CSE", 8.6, 12.5),
    (2, "Meera Krishnan", "ECE", 8.2, 9.0),
    (3, "Rahul Menon", "CSE", 7.4, 7.5),
    (4, "Sneha Varma", "IT", 9.1, 16.0),
    (5, "Devika Pillai", "CSE", 8.9, 14.0)
]

cursor.executemany("INSERT OR IGNORE INTO students VALUES (?, ?, ?, ?, ?)", sample_students)

# 4. Save changes and close the connection
connection.commit()
connection.close()

print("Success! placement.db has been created with 5 student records.")