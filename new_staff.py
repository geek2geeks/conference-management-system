import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",
    # user=input("PostgreSQL master user: "),
    user=("postgres"),
    # password=input("PostgreSQL master password: ")
    password=("darTesw")
)

# Cursor for executing queries
cur = conn.cursor()

# Data to be inserted into table (first name, last name) --- Change to allow for code to be used for new customer by allowing input for table
f_name = "Beta"     # Change to accept input
l_name = "Bot"      # Change to accept input
query_insert = "INSERT INTO staff_accounts (first_name, last_name) VALUES (%s, %s)"     # SQL query to insert first name, last name into staff_accounts with place holders
cur.execute(query_insert, (f_name, l_name))     # Run query w/ placeholders defined

query_select = "SELECT staff_id FROM staff_accounts WHERE first_name = %s AND last_name = %s"       # SQL query to fetch primary key (staff_id) for row inserted
cur.execute(query_select, (f_name, l_name))     # Run query w/ placeholders defined
staff_id = cur.fetchall()       # Get staff_id 
print(staff_id)     # Testing purposes only --- REMOVE

query_username = "UPDATE staff_accounts SET user_name = CONCAT(first_name, last_name, floor(random() * 1000 + 1)) WHERE staff_id = %s"      # SQL query to create user_name via concatination of first name, last name & random int
cur.execute(query_username, (staff_id,))        # Execute query w/ placeholder defined
query_select_all = "SELECT * FROM staff_accounts WHERE staff_id = %s"       # SQL query to get row of data inserted and updated with user name --- ERROR comparing int to int array
cur.execute(query_select_all, (staff_id,))      # Execute query w/ placeholder defined
new_acc = cur.fetchall()        # Get row
print(new_acc)      # Print row

#conn.commit()

cur.close()     # Close cursor

conn.close()    # Close connection