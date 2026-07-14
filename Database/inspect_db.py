import sqlite3

# connect to your DB
conn = sqlite3.connect("taskdatabase.db")
cursor = conn.cursor()

# list tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# show all tasks
cursor.execute("SELECT * FROM task;")
rows = cursor.fetchall()
print("\nAll tasks:")
for row in rows:
    print(row)

conn.close()