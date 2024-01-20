import psycopg2

conn = psycopg2.connect(
    host='localhost',
    database=input('Database: '),
    user=input('Postgres master user: '),
    password=input('Postgres master password: ')
)

cur = conn.cursor()

# Create database role to handle browsing privileges
cur.execute("CREATE USER viewer WITH PASSWORD 'viewer123'")                 # Create new role
cur.execute("GRANT CONNECT ON DATABASE flaskdb TO viewer")                  # Grant connect privilege
cur.execute("GRANT SELECT ON TABLE conference_facilities TO viewer")        # Grant select privilege
cur.execute("GRANT SELECT ON TABLE catering_options TO viewer")

# Create database role to handle login/signup priveleges
cur.execute("CREATE USER log WITH PASSWORD 'log123'")   
cur.execute("GRANT USAGE ON SCHEMA public TO log")
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
cur.execute("GRANT UPDATE (user_name) ON TABLE staff_accounts TO log")
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