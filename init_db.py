import psycopg2

pg_user = input("Postgres master user: ")
pg_key =input("Postgres master password: ")
# Connect to the database
conn = psycopg2.connect(
    host="localhost",
    database='postgres',        # Prompt for postgreSQL database
    user=pg_user,        		# Prompt for postgreSQL master user-name
    password=pg_key)     	    # Prompt for postgreSQL master password

conn.autocommit = True
cur = conn.cursor()     # Create a cursor for executing queries

cur.execute("CREATE DATABASE flaskdb")
conn.commit()
conn.close()

conn = psycopg2.connect(
    host='localhost',
    database='flaskdb',
    user=pg_user,
    password=pg_key
)

cur = conn.cursor()

cur.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto;")     # Create extension for encryption
cur.execute("CREATE DOMAIN meal VARCHAR(8) CHECK(VALUE IN ('buffet', 'platter'));")     # Create domain for meal type
cur.execute("CREATE DOMAIN payment_method VARCHAR(16) CHECK(VALUE IN ('visa', 'mastercard', 'american express'));")     # Create domain for payment methods
cur.execute("CREATE DOMAIN status VARCHAR(9) CHECK(VALUE IN ('booked', 'past', 'cancelled'));")     # Create domain for booking status

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
            "key BYTEA NOT NULL);")

# Create table for staff accounts
cur.execute("CREATE TABLE staff_accounts ("
            "staff_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "first_name VARCHAR(25) NOT NULL,"
            "last_name VARCHAR(45) NOT NULL,"
            "user_name VARCHAR(50));")

# Create table for staff keys
cur.execute("CREATE TABLE staff_keys ("
            "staff_id INTEGER PRIMARY KEY NOT NULL REFERENCES staff_accounts (staff_id) ON DELETE CASCADE,"
            "key BYTEA NOT NULL);")

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

# Commit the transaction to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()