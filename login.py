import psycopg2
import bcrypt
import random

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",
    # user=input("PostgreSQL master user: "),
    user=("log"),
    # password=input("PostgreSQL master password: ")
    password=("log123")
)

# Cursor for executing queries
cur = conn.cursor()

class Portal:
    rand = random.randint(100, 999)

    def __init__(self):
        self.conn = psycopg2.connect(
            host='localhost',
            database='flaskdb',
            user='log',
            password='log123'
        )
        self.cur = self.conn.cursor()

    def close_conn(self):
        self.cur.close()
        self.conn.close()

    def hash(self, table, column, id, data):
        query = "INSERT INTO %s (%s) VALUES (crypt(%s, gen_salt('bf'))::bytea) WHERE customer_id = %s;"  # Insert encrypted password(user_key) using bf algorithm as binary(bytea) data type
        cur.execute(query, (table, column, data, id,))

# Method to authenticate staff credentials
    def auth_staff(self, user, key):      # Pass user name & password
        query = "SELECT staff_id FROM staff_accounts WHERE user_name = %s"      # Query to get id for user name
        cur.execute(query, (user,))     # Execute query
        id = cur.fetchone()     # Define fetched staff id as id
        query = "SELECT key FROM staff_keys WHERE staff_id = %s"        # Query to select password with matching id for comparison
        cur.execute(query, (id,))       # Execute query
        stored_key = cur.fetchone()     # Define fetched encrypted password
        stored_key_bytes = stored_key[0].tobytes()      # Convert to bytes for comparison
        if stored_key and bcrypt.checkpw(key.encode('utf-8'), stored_key_bytes):         
            error = "None"     # If stored password matches key return true
        else:
            error = "Invalid credentials. Please try again..."
        return error
        
    def auth_customer(self, email, key):
        query = "SELECT customer_id FROM customer_accounts WHERE email = %s"
        cur.execute(query, (email,))
        id = cur.fetchone()
        query = "SELECT key FROM customers_keys WHERE customer_id = %s"
        cur.execute(query, (id,))
        stored_key = cur.fetchone()
        stored_key_bytes = stored_key[0].tobytes()
        if stored_key and bcrypt.checkpw(key.encode('utf-8'), stored_key_bytes):
            return True
        else:
            return False
        
    def new_staff(self, f_name, l_name, password):
        user_name = f_name + l_name + self.rand
        query = "INSERT INTO staff_accounts (first_name, last_name, user_name) VALUES (%s, %s, %s)"     # SQL query to insert first name, last name into staff_accounts with place holders
        cur.execute(query, (f_name, l_name, user_name,))     # Run query w/ placeholders defined

    def new_customer(self, f_name, l_name, email, phone_number, company, password):
        query = "INSERT INTO customer_accounts (first_name, last_name, email, phone_number, company) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (f_name, l_name, email, phone_number, company,))
        query_email = ("SELECT customer_id FROM customer_accounts WHERE email = %s")#??? dirty-read
        cur.execute(query_email, (email,))
        customer_id = cur.fetchone() 
        self.hash('customer_keys', 'key', customer_id, password)

conn.commit()

cur.close()
conn.close()