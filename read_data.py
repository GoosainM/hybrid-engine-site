import sqlite3

# Connect to our local database
conn = sqlite3.connect("fitness.db")
cursor = conn.cursor()

try:
    # Fetch all records from our registrations table
    cursor.execute("SELECT * FROM registrations")
    rows = cursor.fetchall()
    
    print("\n--- SECURE DATABASE ENTRIES ---")
    if not rows:
        print("The database is currently empty. Go submit a form on your webpage first!")
    for row in rows:
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Goal: {row[3]} | Date: {row[4]}")
    print("--------------------------------\n")

except sqlite3.OperationalError:
    print("Could not read table. Make sure you have submitted at least one form entry on the website!")

conn.close()