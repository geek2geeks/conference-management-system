import psycopg2
import bcrypt
import random

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
        self.cur.execute(query, (table, column, data, id,))

# Method to authenticate staff credentials
    def auth_staff(self, user, key):      # Pass user name & password
        query = "SELECT staff_id FROM staff_accounts WHERE user_name = %s"      # Query to get id for user name
        self.cur.execute(query, (user,))     # Execute query
        id = self.cur.fetchone()     # Define fetched staff id as id
        query = "SELECT key FROM staff_keys WHERE staff_id = %s"        # Query to select password with matching id for comparison
        self.cur.execute(query, (id,))       # Execute query
        stored_key = self.cur.fetchone()     # Define fetched encrypted password
        stored_key_bytes = stored_key[0].tobytes()      # Convert to bytes for comparison
        if stored_key and bcrypt.checkpw(key.encode('utf-8'), stored_key_bytes):         
            error = "None"     # If stored password matches key return true
        else:
            error = "Invalid credentials. Please try again..."
        return error
        
    def auth_customer(self, email, key):
        query = "SELECT customer_id FROM customer_accounts WHERE email = %s"
        self.cur.execute(query, (email,))
        id = self.cur.fetchone()
        query = "SELECT key FROM customers_keys WHERE customer_id = %s"
        self.cur.execute(query, (id,))
        stored_key = self.cur.fetchone()
        stored_key_bytes = stored_key[0].tobytes()
        if stored_key and bcrypt.checkpw(key.encode('utf-8'), stored_key_bytes):
            return True
        else:
            return False
        
    def new_staff(self, f_name, l_name, password):
        user_name = f_name + l_name + self.rand
        query = "INSERT INTO staff_accounts (first_name, last_name, user_name) VALUES (%s, %s, %s)"     # SQL query to insert first name, last name into staff_accounts with place holders
        self.cur.execute(query, (f_name, l_name, user_name,))     # Run query w/ placeholders defined
        self.conn.commit()

    def new_customer(self, f_name, l_name, email, phone_number, company, password):
        query = "INSERT INTO customer_accounts (first_name, last_name, email, phone_number, company) VALUES (%s, %s, %s, %s, %s)"
        self.cur.execute(query, (f_name, l_name, email, phone_number, company,))
        query_email = ("SELECT customer_id FROM customer_accounts WHERE email = %s")#??? dirty-read
        self.cur.execute(query_email, (email,))
        customer_id = self.cur.fetchone() 
        self.hash('customer_keys', 'key', customer_id, password)
        self.conn.commit()

close_conn()