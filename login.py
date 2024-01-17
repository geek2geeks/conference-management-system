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

    def hash(self, table, id, data):
        if table == 'customer_keys':
            query = "INSERT INTO customer_keys (customer_id, key) VALUES (%s, crypt(%s, gen_salt('bf'))::bytea);"  # Insert encrypted password(user_key) using bf algorithm as binary(bytea) data type
        else:
            query = "INSERT INTO staff_keys (staff_id, key) VALUES (%s, crypt(%s, gen_salt('bf'))::bytea);"
        self.cur.execute(query, (id, data,))

    def check_curr_block(self):
        try:
            self.cur.execute("SELECT * FROM staff_accounts")
            self.conn.commit()
        except psycopg2.errors.InFailedSqlTransaction as e:
            if isinstance(e, psycopg2.DatabaseError) and "aborted" in str(e):
                self.conn.rollback()
            else:
                None

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
        self.close_conn()

    def new_customer(self, f_name, l_name, email, phone_number, company, password):    # Pass first name, last name, email, phone number, company, password
        self.check_curr_block()     # Check if current block is valid
        query = "INSERT INTO customer_accounts (first_name, last_name, email, phone_number, company) VALUES (%s, %s, %s, %s, %s)"       # SQL query to insert first name, last name, email, phone number, company into customer_accounts with place holders
        self.cur.execute(query, (f_name, l_name, email, phone_number, company,))        # Run query w/ placeholders defined
        query_email = ("SELECT customer_id FROM customer_accounts WHERE email = %s")#??? dirty-read
        self.cur.execute(query_email, (email,))     # Execute query
        customer_id = self.cur.fetchone()       # Define fetched customer id as id
        table = 'customer_keys'     # Define table for hash method 
        self.hash(table, customer_id, password)     # Call hash method to hash password
        self.conn.commit()      # Commit changes to database
        self.close_conn()       # Close connection
