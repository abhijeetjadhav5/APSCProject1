import sqlite3

# Connect to database
conn = sqlite3.connect("registration.db")

# Create table
conn.execute("""
CREATE TABLE IF NOT EXISTS registrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT,
    aadhar TEXT,
    name TEXT,
    validate TEXT,
    gender TEXT,
    contact TEXT,
    address TEXT,
    dob TEXT
)
""")

# Save changes
conn.commit()

# Close database
conn.close()

print("Table created successfully!")
