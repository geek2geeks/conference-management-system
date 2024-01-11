import psycopg2

#connect to postgreSQL DB
conn = psycopg2.connect(
    host="localhost",
    database="flaskdb",     
    user=input("Postgres master user: "),        		#prompt for postgreSQL master user-name
    password=input("Postgres master password: "))     	#prompt for postgreSQL master password

cur = conn.cursor() #create cursor, allowing python to execute postgreSQL commands

#INSERT data into TABLE catering_options
cur.execute("INSERT INTO catering_options (name, description, capacity, price_per_day, cuisine, type) VALUES ('Gourmet Delights', 'Exquisite gourmet cuisine for upscale events', 100, 800, 'French', 'buffet'),"
  "('Finger Foods Galore', 'A variety of finger foods perfect for casual gatherings', 80, 500, 'International', 'buffet'),"
  "('Grand Feast Platter', 'A large platter with diverse dishes suitable for any event', 120, 700, 'Various', 'platter'),"
  "('Mediterranean Buffet', 'Healthy and flavorful Mediterranean dishes', 90, 600, 'Mediterranean', 'buffet'),"
  "('Sushi Sensation', 'Freshly made sushi platter for sushi enthusiasts', 60, 900, 'Japanese', 'platter'),"
  "('Tropical Buffet', 'Tropical flavors with a mix of fruits and exotic dishes', 70, 650, 'Tropical', 'buffet'),"
  "('Cheese Platter Extravaganza', 'Assorted cheeses from around the world', 50, 450, 'International', 'platter'),"
  "('BBQ Bonanza', 'A barbecue platter with a variety of grilled meats', 80, 750, 'American', 'platter'),"
  "('Vegan Delight', 'Delicious vegan options suitable for all dietary needs', 85, 550, 'Vegetarian', 'buffet'),"
  "('Seafood Galore', 'An assortment of seafood dishes from the ocean', 55, 850, 'Seafood', 'platter');")

#INSERT data into TABLE conference_facilities
cur.execute("INSERT INTO conference_facilities (name, description, capacity, price_per_day, location, address) VALUES ('Elegant Events Center', 'Perfect venue for corporate conferences and seminars', 150, 1200, 'Westminster', '123 Westminster St, SW1A 1AA'),"
  "('Riverside Suites', 'Scenic view conference rooms by the Thames', 80, 900, 'South Bank', '456 Riverside Ave, SE1 7PB'),"
  "('City Hub Conference Hall', 'Modern facility in the heart of the financial district', 200, 1500, 'City of London', '789 Financial St, EC2R 8AH'),"
  "('Mayfair Meeting Place', 'Luxurious venue in the affluent district', 100, 2000, 'Mayfair', '101 Mayfair Rd, W1K 1AB'),"
  "('Tech Central', 'State-of-the-art facilities for tech-related events', 120, 1100, 'Shoreditch', '202 Tech St, E1 6GY'),"
  "('Greenwich Conventions', 'Historic venue with a blend of modern amenities', 90, 1000, 'Greenwich', '303 Historic Ave, SE10 8JA'),"
  "('Bloomsbury Ballrooms', 'Stunning ballrooms for elegant conferences', 180, 1800, 'Bloomsbury', '404 Bloomsbury Way, WC1A 1AA'),"
  "('Theatreland Conventions', 'Convenient venue amidst London's vibrant theater scene', 70, 950, 'Covent Garden', '505 Theatre St, WC2H 9HZ'),"
  "('Kensington Forum', 'Versatile space in the upscale Kensington district', 130, 1300, 'Kensington', '606 Kensington Blvd, SW7 2SA'),"
  "('Regents Park Pavilion', 'Scenic location with views of Regents Park', 50, 800, 'Regents Park', '707 Regents Park Rd, NW1 4RY'),"
  "('London Heights', 'Spacious hall for conferences and seminars', 200, 1500, 'Westminster', '1 Westminster Street, SW1A 0AA'),"
  "('Thames View Hub', 'Conference space overlooking the Thames', 120, 1000, 'South Bank', '15 South Bank Lane, SE1 9TG'),"
  "('City Central Conference Center', 'Modern conference facility in the heart of the city', 300, 2000, 'The City', '25 City Central Road, EC2V 8BG'),"
  "('Regents Park Venue', 'Elegant venue amidst Regents Park', 150, 1200, 'Regents Park', '8 Regents Park Place, NW1 4RG'),"
  "('Docklands Convention Center', 'State-of-the-art facilities in Docklands', 250, 1800, 'Canary Wharf', '10 Docklands Avenue, E14 5AB'),"
  "('London Central Conference Center', 'State-of-the-art facility in the heart of London', 200, 1500, 'Central London', '123 Main Street, WC1X 0AA'),"
  "('West End Events Hub', 'Versatile venue in the vibrant West End', 150, 1200, 'West End', '456 High Street, W1A 1AA'),"
  "('City Skyline Conventions', 'Panoramic views of the city for your event', 100, 1800, 'City of London', '789 Skyline Avenue, EC2A 2BB'),"
  "('South Bank Summit Space', 'Riverside venue with modern amenities', 180, 1400, 'South Bank', '101 Riverwalk, SE1 7PB'),"
  "('East London Expo Hall', 'Spacious hall for exhibitions and conferences', 250, 2000, 'East London', '222 Expo Street, E1 8CC'),"
  "('Northside Conference Plaza', 'Convenient location in North London', 120, 1000, 'North London', '333 Plaza Road, N1 9DD'),"
  "('Regents Park Convention Center', 'Surrounded by nature in Regents Park', 300, 2500, 'Regents Park', '444 Green Lane, NW1 4AA'),"
  "('Canary Wharf Conference Oasis', 'Business district venue with modern facilities', 180, 1600, 'Canary Wharf', '555 Financial Road, E14 5AA'),"
  "('Hampstead Heath Hall', 'Scenic location near Hampstead Heath', 80, 900, 'Hampstead', '666 Heath Street, NW3 6AA'),"
  "('Camden Creative Space', 'Artsy and dynamic venue in Camden', 120, 1100, 'Camden', '777 Artistic Avenue, NW1 0AA'),"
  "('Greenwich Grand Conventions', 'Historic venue in the heart of Greenwich', 150, 1300, 'Greenwich', '888 Time Square, SE10 9BB'),"
  "('Wembley Events Arena', 'Iconic venue near Wembley Stadium', 200, 1800, 'Wembley', '999 Stadium Road, HA9 0AA'),"
  "('Kensington Gardens Pavilion', 'Elegant venue overlooking Kensington Gardens', 120, 1100, 'Kensington', '777 Serene Street, W8 4AA');")

conn.commit()       #commit changes to databse

cur.close()         #close cursor

conn.close()        #close DB connection