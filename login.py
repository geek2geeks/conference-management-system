import psycopg2
import bcrypt
import random

class Portal:       # Define class
    rand = random.randint(100, 999)     # Generate random number for staff user name

    # Method to connect to database
    def __init__(self):     # Pass self
        self.conn = psycopg2.connect(       # Define connection
            host='localhost',      
            database='flaskdb',
            user='log',
            password='log123'
        )
        self.cur = self.conn.cursor()       # Define cursor

    # Method to close connection
    def close_conn(self):       # Pass self
        self.cur.close()        # Close cursor
        self.conn.close()       # Close connection

    # Method to hash password
    def hash(self, table, id, data):        # Pass table, id, password
        if table == 'customer_keys':        # If table is customer_keys query = ...
            query = "INSERT INTO customer_keys (customer_id, key) VALUES (%s, crypt(%s, gen_salt('bf'))::bytea);"  
        else:       # Else query = ...
            query = "INSERT INTO staff_keys (staff_id, key) VALUES (%s, crypt(%s, gen_salt('bf'))::bytea);"
        self.cur.execute(query, (id, data,))        # Execute query w/ placeholders defined

    # Method to check if current block is valid
    def check_curr_block(self):     # Pass current block
        try:        # Try to execute query
            self.cur.execute("SELECT * FROM staff_accounts")        # Query to check if current block is valid            
        except psycopg2.errors.InFailedSqlTransaction as e:     # If query fails
            if isinstance(e, psycopg2.DatabaseError) and "aborted" in str(e):       # If query fails due to aborted transaction
                self.conn.rollback()        
                self.conn.cursor()
            else:       # If query fails due to other reason
                print("Error: ", e)      
        except psycopg2.errors.InterfaceError as e:
            if 'cursor already closed' in str(e):
                self.cur.close()                    # Close cursor
                self.conn = psycopg2.connect(
                    host='localhost',      
                    database='flaskdb',
                    user='log',
                    password='log123'
                )
                self.cur = self.conn.cursor()       # Define new cursor
            else:
                print("Error: ", e)
                

    # Method to authenticate staff credentials
    def auth_staff(self, user, key):      # Pass user name & password
        self.check_curr_block()     # Check if current block is valid   
        ### Error handling for user name ###
        query = "SELECT staff_id FROM staff_accounts WHERE user_name = %s"      # Query to get id for user name
        self.cur.execute(query, (user,))     # Execute query
        id = self.cur.fetchone()[0]     # Define fetched staff id as id
        query = "SELECT role FROM staff_accounts WHERE user_name = %s"      # Query to get role for user name
        self.cur.execute(query, (user,))
        role = self.cur.fetchone()[0]       # Fetch role
        query = "SELECT key FROM staff_keys WHERE staff_id = %s"        # Query to select password with matching id for comparison
        self.cur.execute(query, (id,))       # Execute query
        stored_key = self.cur.fetchone()     # Fetch encrypted password
        stored_key_bytes = stored_key[0].tobytes()      # Convert to bytes for comparison
        if stored_key and bcrypt.checkpw(key.encode('utf-8'), stored_key_bytes):        # If stored password matches key set error as none   
            self.close_conn()       # Close connection
            return(True, id, role)     
        else:       # Else set error as...
            self.close_conn()       # Close connection
        return (False, None, None)       

    # Method to authenticate customer credentials    
    def auth_customer(self, email, key):        # Pass email & password
        exists = self.check_exists(email)        # Check if email exists
        if exists == False:     # If email does not exist return false
            return (False, None, None)
        elif email is None:     # If email is none return false
            return (False, None, None)
        else:
            self.check_curr_block()     # Check if current block is valid 
            query = "SELECT customer_id FROM customer_accounts WHERE email = %s"        # Query to get id for email
            self.cur.execute(query, (email,))       # Execute query
            id = self.cur.fetchone()        # Define fetched customer id as id
            query = "SELECT key FROM customer_keys WHERE customer_id = %s"      # Query to select password with matching id for comparison
            self.cur.execute(query, (id,))      # Execute query
            stored_key = self.cur.fetchone()        # Define fetched encrypted password
            stored_key_bytes = stored_key[0].tobytes()      # Convert to bytes for comparison
            if stored_key and bcrypt.checkpw(key.encode('utf-8'), stored_key_bytes):        # If stored password matches key return true
                self.close_conn()       # Close connection
                return (True, id, 'customer')      
            else:       # Else return false
                self.close_conn()       # Close connection
                return (False, None, None)
        

    # Method to create new staff account and store encrypted password
    def new_staff(self, f_name, l_name, password):      # Pass first name, last name, password
        self.check_curr_block()     # Check if current block is valid
        user_name = f_name + l_name + self.rand        # Define user name as first name + last name + random number
        query = "INSERT INTO staff_accounts (first_name, last_name, user_name) VALUES (%s, %s, %s)"     # SQL query to insert first name, last name and user name into staff_accounts with place holders
        self.cur.execute(query, (f_name, l_name, user_name,))     # Run query w/ placeholders defined
        query_username = ("SELECT staff_id FROM staff_accounts WHERE user_name = %s")       # Query to get id for user name
        self.cur.execute(query_username, (user_name,))      # Execute query
        staff_id = self.cur.fetchone()      # Define fetched staff id as id
        table = 'staff_keys'        # Define table for hash method
        self.hash(table, staff_id, password)        # Call hash method to hash password
        self.conn.commit()      # Commit changes to database
        self.close_conn()       # Close connection

    # Method to create new customer account and store encrypted password
    def new_customer(self, f_name, l_name, email, phone_number, company, password):    # Pass first name, last name, email, phone number, company, password
        self.check_curr_block()     # Check if current block is valid
        query = "INSERT INTO customer_accounts (first_name, last_name, email, phone_number, company) VALUES (%s, %s, %s, %s, %s)"       # SQL query to insert first name, last name, email, phone number, company into customer_accounts with place holders
        self.cur.execute(query, (f_name, l_name, email, phone_number, company,))        # Run query w/ placeholders defined
        query_email = ("SELECT customer_id FROM customer_accounts WHERE email = %s")        # Query to get id for email    
        self.cur.execute(query_email, (email,))     # Execute query
        customer_id = self.cur.fetchone()       # Define fetched customer id as id
        table = 'customer_keys'     # Define table for hash method 
        self.hash(table, customer_id, password)     # Call hash method to hash password
        self.conn.commit()      # Commit changes to database
        self.close_conn()       # Close connection
        return (True, customer_id, 'customer')      # Return true, id and customer
    

    def check_exists(self, email):
        self.check_curr_block()     # Check if current block is valid
        query = "SELECT email FROM customer_accounts WHERE email = %s"
        self.cur.execute(query, (email,))
        email = self.cur.fetchone()
        if email:
            return True
        else:
            return False
