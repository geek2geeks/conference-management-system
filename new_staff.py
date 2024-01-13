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

# Insert new user first name, last name into table --- Change to allow for code to be used for new customer by allowing input for table
f_name = "Beta"     # Change to accept input
l_name = "Bot"      # Change to accept input
query_insert = "INSERT INTO staff_accounts (first_name, last_name) VALUES (%s, %s)"     # SQL query to insert first name, last name into staff_accounts with place holders
cur.execute(query_insert, (f_name, l_name))     # Run query w/ placeholders defined

# Identify row
query_select = "SELECT staff_id FROM staff_accounts WHERE first_name = %s AND last_name = %s"       # SQL query to fetch primary key (staff_id) for row inserted
cur.execute(query_select, (f_name, l_name))     # Run query w/ placeholders defined
staff_id = cur.fetchone()       # Get staff_id 
print(staff_id)     # Testing purposes only --- REMOVE

# Create user name for new user
query_username = "UPDATE staff_accounts SET user_name = CONCAT(first_name, last_name, floor(random() * 1000 + 1)) WHERE staff_id = %s"      # SQL query to create user_name via concatination of first name, last name & random int
cur.execute(query_username, (staff_id,))        # Execute query w/ placeholder defined
query_select = "SELECT * FROM staff_accounts WHERE staff_id = %s"       # SQL query to get row of data inserted and updated with user name
cur.execute(query_select, (staff_id,))      # Execute query w/ placeholder defined
new_acc = cur.fetchall()        # Get row
print(new_acc)      # Testing purposes only --- REMOVE

# Create default password for new user & insert into staff_keys table using identified id
new_key = "defaultKey-123"      # Define default key --- Change to accept input or random generation???
query_new_key = "INSERT INTO staff_keys (staff_id_foreign, key) VALUES (%s, %s)"        # SQL query to insert staff id and default key
cur.execute(query_new_key, (staff_id, new_key))     # Execute query w/ placeholders
query_select = "SELECT * FROM staff_keys WHERE staff_id_foreign = %s"       # SQL query to select inserted data
cur.execute(query_select, (staff_id,))      # Execute query w/ placeholders
key = cur.fetchall()        # Get row
print(key)      # Testing purposes only --- REMOVE

#conn.commit() --- Commented out whilst testing

cur.close()     # Close cursor

conn.close()    # Close connection