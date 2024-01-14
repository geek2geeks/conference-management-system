import psycopg2

# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database=input("Database: "),                       # Prompt for postgreSQL database
    user=input("Postgres master user: "),        		# Prompt for postgreSQL master user-name
    password=input("Postgres master password: "))     	# Prompt for postgreSQL master password

# Create a cursor for executing queries
cur = conn.cursor()

# Create extension for encryption
cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")
# Create domain for meal type
cur.execute("CREATE DOMAIN meal VARCHAR(8) CHECK(VALUE IN ('buffet', 'platter'));")

# Create domain for payment methods
cur.execute("CREATE DOMAIN payment_method VARCHAR(16) CHECK(VALUE IN ('visa', 'mastercard', 'american express'));")

# Create domain for booking status
cur.execute("CREATE DOMAIN status VARCHAR(9) CHECK(VALUE IN ('booked', 'past', 'cancelled'));")

# Create table for customer accounts
cur.execute("CREATE TABLE customer_accounts ("
            "customer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "first_name VARCHAR(25) NOT NULL,"
            "last_name VARCHAR(45) NOT NULL,"
            "email VARCHAR(50) NOT NULL,"
            "phone_number INTEGER,"
            "company VARCHAR(50));")

# Create table for customer keys
cur.execute("CREATE TABLE customer_keys ("
            "customer_id INTEGER PRIMARY KEY NOT NULL REFERENCES customer_accounts (customer_id) ON DELETE CASCADE,"
            "key VARCHAR(16) NOT NULL);")

# Create table for staff accounts
cur.execute("CREATE TABLE staff_accounts ("
            "staff_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "first_name VARCHAR(25) NOT NULL,"
            "last_name VARCHAR(45) NOT NULL,"
            "user_name VARCHAR(50));")

# Create table for staff keys
cur.execute("CREATE TABLE staff_keys ("
            "staff_id INTEGER PRIMARY KEY NOT NULL REFERENCES staff_accounts (staff_id) ON DELETE CASCADE,"
            "key VARCHAR(16) NOT NULL);")

# Create table for conference facilities
cur.execute("CREATE TABLE conference_facilities ("
            "conference_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "name VARCHAR(50),"
            "description TEXT,"
            "capacity INTEGER,"
            "price_per_day INTEGER,"
            "location VARCHAR(25),"
            "address TEXT,"
            "photo_int TEXT,"
            "photo_ext TEXT);")

# Create table for catering options
cur.execute("CREATE TABLE catering_options ("
            "catering_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "name VARCHAR(50),"
            "description TEXT,"
            "capacity INTEGER,"
            "price_per_day DECIMAL,"
            "type meal NOT NULL,"
            "cuisine VARCHAR(25),"
            "address TEXT);")

# Create table for payment methods
cur.execute("CREATE TABLE payment_methods ("
            "payment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "customer_id_foreign INTEGER NOT NULL REFERENCES customer_accounts (customer_id),"
            "bank VARCHAR(25) NOT NULL,"
            "payment_type payment_method NOT NULL,"
            "account_number INTEGER NOT NULL,"
            "expiry_date DATE NOT NULL);")

# Create table for bookings
cur.execute("CREATE TABLE bookings ("
            "booking_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "customer_id_foreign INTEGER REFERENCES customer_accounts (customer_id),"
            "event_date DATE,"
            "conference_id_foreign INTEGER REFERENCES conference_facilities (conference_id),"
            "catering_id_foreign INTEGER REFERENCES catering_options (catering_id),"
            "created TIMESTAMPTZ NOT NULL,"
            "modified TIMESTAMPTZ,"
            "booking_status status NOT NULL,"
            "cancel_reason TEXT,"
            "payment_id_foreign INTEGER REFERENCES payment_methods (payment_id),"
            "price DECIMAL);")

# Create database role to handle browsing privileges
cur.execute("CREATE USER viewer WITH PASSWORD 'viewer123'")                 # Create new role
cur.execute("GRANT CONNECT ON DATABASE flaskdb TO viewer")                  # Grant connect privilege
cur.execute("GRANT SELECT ON TABLE conference_facilities TO viewer")        # Grant select privilege
cur.execute("GRANT SELECT ON TABLE catering_options TO viewer")

# Create database role to handle login/signup priveleges
cur.execute("CREATE USER log WITH PASSWORD 'log123'")                       # Create new role
cur.execute("GRANT CONNECT ON DATABASE flaskdb TO log")                     # Grant connect privilege
cur.execute("GRANT SELECT ON TABLE staff_accounts TO log")
cur.execute("GRANT SELECT ON TABLE customer_accounts TO log")
cur.execute("GRANT SELECT ON TABLE staff_keys TO log")
cur.execute("GRANT SELECT ON TABLE customer_keys TO log")
cur.execute("GRANT INSERT ON TABLE staff_accounts TO log")                  # Grant insert privilege
cur.execute("GRANT INSERT ON TABLE customer_accounts TO log")
cur.execute("GRANT INSERT ON TABLE staff_keys TO log")
cur.execute("GRANT INSERT ON TABLE customer_keys TO log")
cur.execute("GRANT UPDATE ON TABLE staff_keys TO log")                      # Grant update privilege
cur.execute("GRANT UPDATE (user_name) ON TABLE staff_accounuts")
cur.execute("GRANT UPDATE ON TABLE customer_keys TO log")

# Create database role to handle client privileges
cur.execute("CREATE USER client WITH PASSWORD 'client123'")                 # Create new role
cur.execute("GRANT CONNECT ON DATABASE flaskdb TO client")                  # Grant connect privilege
cur.execute("GRANT SELECT ON TABLE conference_facilities TO client")        # Grant select privilege 
cur.execute("GRANT SELECT ON TABLE catering_options TO client")
cur.execute("GRANT SELECT ON TABLE bookings TO client")
cur.execute("GRANT SELECT ON TABLE payment_methods TO client")
cur.execute("GRANT INSERT ON TABLE bookings TO client")                     # Grant insert privilege
cur.execute("GRANT INSERT ON TABLE payment_methods TO client")
cur.execute("GRANT UPDATE (key) ON TABLE customer_keys TO client")          # Grant update privilege
cur.execute("GRANT UPDATE ON TABLE bookings TO  client")

# Create database role to handle staff privileges
cur.execute("CREATE USER staff WITH PASSWORD 'staff123'")                   # Create new role
cur.execute("GRANT CONNECT ON DATABASE flaskdb TO staff")                   # Grant connect privilege
cur.execute("GRANT SELECT ON TABLE conference_facilities TO staff")         # Grant select privilege
cur.execute("GRANT SELECT ON TABLE catering_options TO staff")
cur.execute("GRANT SELECT ON TABLE bookings TO staff")
cur.execute("GRANT SELECT ON TABLE payment_methods TO staff")
cur.execute("GRANT SELECT ON TABLE customer_accounts TO staff")
cur.execute("GRANT INSERT ON TABLE bookings TO staff")                      # Grant insert privilege
cur.execute("GRANT INSERT ON TABLE payment_methods TO staff")
cur.execute("GRANT INSERT ON TABLE customer_accounts To staff")
cur.execute("GRANT UPDATE ON TABLE bookings TO staff")                      # Grant update privilege

# Create database role to handle admin privileges
cur.execute("CREATE USER staff_admin WITH PASSWORD 'staff_admin123'")       # Create new role
cur.execute("GRANT CONNECT ON DATABASE flaskdb TO staff_admin")             # Grant connect privilege
cur.execute("GRANT SELECT ON TABLE conference_facilities TO staff_admin")   # Grant select privilege
cur.execute("GRANT SELECT ON TABLE catering_options TO staff_admin")
cur.execute("GRANT SELECT ON TABLE bookings TO staff_admin")
cur.execute("GRANT SELECT ON TABLE payment_methods TO staff_admin")
cur.execute("GRANT SELECT ON TABLE customer_accounts TO staff_admin")
cur.execute("GRANT INSERT ON TABLE bookings TO staff_admin")                # Grant insert privilege
cur.execute("GRANT INSERT ON TABLE payment_methods TO staff_admin")
cur.execute("GRANT INSERT ON TABLE customer_accounts To staff_admin")
cur.execute("GRANT INSERT ON TABLE conference_facilities To staff_admin")
cur.execute("GRANT INSERT ON TABLE catering_options To staff_admin")
cur.execute("GRANT UPDATE ON TABLE bookings TO staff_admin")                # Grant update privilege
cur.execute("GRANT UPDATE ON TABLE conference_facilities To staff_admin")
cur.execute("GRANT UPDATE ON TABLE catering_options To staff_admin")

# Commit the transaction to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
