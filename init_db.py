import os
import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",
    user='postgres',        #user=os.environ["DB_USERNAME"], TRIGGERS KEY-ERROR
    password='darTesw')     #password=os.environ["DB_PASSWORD"]) TRIGGERS KEY-ERROR

cur = conn.cursor()

cur.execute("CREATE DOMAIN meal VARCHAR(8) CHECK(VALUE IN ('buffet', 'platter'));")

cur.execute("CREATE DOMAIN payment_method VARCHAR(16) CHECK(VALUE IN ('visa', 'mastercard', 'american express'));")

cur.execute("CREATE DOMAIN status VARCHAR(9) CHECK(VALUE IN ('booked', 'past', 'cancelled'));")

cur.execute("CREATE TABLE customer_accounts (customer_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
	"first_name VARCHAR(25) NOT NULL,"
	"last_name VARCHAR(50) NOT NULL,"
	"email VARCHAR(50) NOT NULL,"
	"phone_number INTEGER,"
	"company VARCHAR(50));")

cur.execute("CREATE TABLE customer_keys (customer_id_foreign INTEGER PRIMARY KEY NOT NULL REFERENCES customer_accounts (customer_id) ON DELETE CASCADE,"
	"key VARCHAR(16) NOT NULL);")

cur.execute("CREATE TABLE staff_accounts (staff_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
	"first_name VARCHAR(25) NOT NULL,"
	"last_name VARCHAR(50) NOT NULL);")

cur.execute("CREATE TABLE staff_keys (staff_id_foreign INTEGER PRIMARY KEY NOT NULL REFERENCES staff_accounts (staff_id) ON DELETE CASCADE,"
	"key VARCHAR(16) NOT NULL);")

cur.execute("CREATE TABLE conference_facilities (conference_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
	"name VARCHAR(50),"
	"description TEXT,"
	"capacity INTEGER,"
	"price_per_day INTEGER,"
	"location VARCHAR(25),"
	"address TEXT,"
	"photo_int TEXT,"
	"photo_ext TEXT);")

cur.execute("CREATE TABLE catering_options (catering_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
	"name VARCHAR(50),"
	"description TEXT,"
	"capacity INTEGER,"
	"price_per_day DECIMAL,"
	"type meal NOT NULL,"
	"cuisine VARCHAR(25),"
	"address TEXT);")

cur.execute("CREATE TABLE payment_methods (payment_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
	"customer_id_foreign INTEGER NOT NULL REFERENCES customer_accounts (customer_id),"
	"payment_type payment_method,"
	"account_number INTEGER NOT NULL,"
	"expiry_date DATE NOT NULL);")

cur.execute("CREATE TABLE bookings (booking_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
	"customer_id_foreign INTEGER REFERENCES customer_accounts (customer_id),"
	"event_date DATE,"
	"conference_id_foreign INTEGER REFERENCES conference_facilities (conference_id),"
	"catering_id_foreign INTEGER REFERENCES catering_options (catering_id),"
	"booking_status status NOT NULL,"
	"payment_id_foreign INTEGER REFERENCES payment_methods (payment_id),"
	"price DECIMAL);")

conn.commit()

cur.close()

conn.close()