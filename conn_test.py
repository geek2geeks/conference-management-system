import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",
    user=input("PostgreSQL master user: "),
    password=input("PostgreSQL master password: ")
)

cur = conn.cursor()

cur.execute("SELECT name FROM catering_options WHERE catering_id = 9")
row = cur.fetchall()
print(row)

conn.commit()

cur.close()

conn.close()