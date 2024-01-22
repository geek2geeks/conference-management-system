from flask import Flask, render_template, request, redirect, url_for, session
from login import Portal, Client, Staff, Admin

app = Flask(__name__)
app.secret_key = 'secret_key'

log = Portal()
client = Client()
staff = Staff()
admin = Admin()

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])       # Define login route
def login():        # Define login method
    error = None        # Define error variable
    if request.method == 'POST':        # If request is POST
        email = request.form['email']       # Get email
        password = request.form['password']     # Get password
        validate = log.auth_customer(email, password)       # Call auth_customer method from login.py
        if validate[0] == True:        # If first variable in validate is true print = login successful
            print("login successful")
            session['logged_in'] = validate[0]     # Set session logged in status
            session['user_id'] = validate[1]       # Set session user id
            session['user_type'] = validate[2]     # Set session user type
            return redirect(url_for('dashboard'))            
        else:       # Else print = invalid credentials
            error = 'Invalid credentials. Please try again...'
            print(error)
    return render_template('login.html', error=error)

@app.route('/admin_login', methods=['GET', 'POST'])       # Define admin login route
def admin_login(): 
    error = None
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        validate = log.auth_staff(user_name, password)     # Call auth_staff method from login.py
        if validate[0] == True:
            session['logged_in'] = validate[0]     # Set session logged in status
            session['user_id'] = validate[1]       # Set session user id
            session['user_type'] = validate[2]     # Set session user type
            return redirect(url_for('admin_panel'))
        else:
            error = 'Invalid credentials. Please try again...'
            print(error)
    return render_template('admin_login.html', error=error)

@app.route('/reset_password')
def reset_password():
    # Logic for resetting password
    return render_template('reset_password.html')


# Route for handling user registration, supports both GET and POST methods
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        contact_number = request.form['contact_number']
        company = request.form['company']
        password = request.form['password']
        password_confirm = request.form['password_confirm']
        if password != password_confirm:
            error = 'Passwords do not match.'
        else:
            exists = log.check_exists(email)            # Check whether email alread exists within table and handle error
            if exists == True:
                error = 'Email already exists.'
                #return render_template('signUp.html', error=error)
            else:
                validate = log.new_customer(first_name, last_name, email, contact_number, company, password)       # Call new_customer method from login.py
                print("Sign up successful")
                session['logged_in'] = validate[0]     # Set session logged in status
                session['user_id'] = validate[1]       # Set session user id
                session['user_type'] = validate[2]     # Set session user type
                return redirect(url_for('dashboard'))
    return render_template('signUp.html', error=error)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/manage_bookings')
def manage_bookings():
    # Logic to retrieve and display user's bookings
    return render_template('manage_bookings.html')


@app.route('/admin_panel', methods=['GET', 'POST'])
def admin_panel():
    results = None
    if request.method == 'POST':
        menu1 = request.form.get('menu1')
        menu2 = request.form.get('menu2')
        menu3 = request.form.get('menu3')
        input_box = request.form.get('input_box')
        if menu1 is not None and menu2 is not None:
            if menu3 is None:
                query = 'SELECT %s FROM %s' % (menu1, menu2)
            else:
                query = 'SELECT %s FROM %s WHERE %s = %s' % (menu1, menu2, menu3, input_box)
            staff.cur.execute(query)
            results = staff.cur.fetchall()
    if session.get('logged_in') == True:       # Get session logged in status
        return render_template('admin_panel.html', results=results)       
    else:
        return redirect(url_for('admin_login'))      # Redirect to login page



@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Handle booking logic
        pass
    return render_template('book.html')


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in') == True:        # Get session logged in status
        log.check_curr_block()
        query = 'SELECT * FROM customer_accounts WHERE customer_id = %s'
        log.cur.execute(query, (session['user_id'],))
        profile = log.cur.fetchall()
        user_id = profile[0][0]
        first_name = profile[0][1]
        last_name = profile[0][2]
        email = profile[0][3]
        phone_number = profile[0][4]
        company = profile[0][5]
        client.check_curr_block()
        query_bookings = ("SELECT bookings.event_date, conference_facilities.name, conference_facilities.location FROM bookings JOIN conference_facilities ON bookings.conference_id_foreign = conference_facilities.conference_id WHERE customer_id_foreign = %s AND booking_status != 'cancelled' ORDER BY event_date DESC")
        client.cur.execute(query_bookings, (session['user_id'],))
        bookings = client.cur.fetchall()
        query_pay = 'SELECT bank, payment_type, expiry_date FROM payment_methods WHERE customer_id_foreign = %s'
        client.cur.execute(query_pay, (session['user_id'],))
        payment_methods = client.cur.fetchall()
        bank=payment_methods[0][0]

        return render_template('dashboard.html', user_id=user_id, first_name=first_name, last_name=last_name, email=email, 
                               phone_number=phone_number, company=company, bank=bank, payment_methods=payment_methods, bookings=bookings)
    else:
        print("not logged in")
        return redirect(url_for('login'))      # Redirect to login page


@app.route('/about')
def about():
    return render_template('about.html')

# Route for handling user logout
@app.route('/logout')
def logout():
    session['logged_in'] = False        # Set session logged in status
    session['user_id'] = None           # Set session user id
    session['user_type'] = None         # Set session user type
    return redirect(url_for('home'))


# Include your routes here

if __name__ == '__main__':
    app.run(debug=True)
