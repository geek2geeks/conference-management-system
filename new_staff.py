import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",
    #user=input("PostgreSQL master user: "),
    user=("postgres"),
    #password=input("PostgreSQL master password: ")
    password=("darTesw")
)

cur = conn.cursor()

f_name = "Beta"
l_name = "Bot"
query_insert = "INSERT INTO staff_accounts (first_name, last_name) VALUES (%s, %s)"
cur.execute(query_insert, (f_name, l_name))

query_select = "SELECT * FROM staff_accounts WHERE first_name = %s AND last_name = %s"
cur.execute(query_select, (f_name, l_name))
row = cur.fetchall()
print(row)

#cur.execute("UPDATE staff_accounts WHERE staff_id = {row} SET user_name = CONCAT(first_name, last_name, floor(random() * 1000 + 1))")

#conn.commit()

cur.close()

conn.close()