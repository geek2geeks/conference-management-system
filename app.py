from flask import Flask, render_template, request, redirect, url_for
from login import Portal

app = Flask(__name__)

log = Portal()

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
        if validate == True:        # If validate is true print = login successful
            print("login successful")
            return render_template('dashboard.html')            
        else:       # Else print = invalid credentials
            error = 'Invalid credentials. Please try again...'
            print(error)
    return render_template('login.html', error=error)


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
            # Check whether email alread exists within table and handle error
            log.new_customer(first_name, last_name, email, contact_number, company, password)       # Call new_customer method from login.py
            print("Sign up successful")
            return render_template('dashboard.html')
    return render_template('signUp.html', error=error)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/logout')
def logout():
    # Here, you'll handle the logic to log the user out
    # For example, if using Flask-Login, you can use logout_user()
    # redirect the user to the home page after logging out
    return redirect(url_for('home'))

@app.route('/manage_bookings')
def manage_bookings():
    # Logic to retrieve and display user's bookings
    return render_template('manage_bookings.html')


@app.route('/admin')
def admin():
    # Ensure user is an admin
    # Logic to manage users, bookings, facilities, etc.
    return render_template('admin_panel.html')



@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Handle booking logic
        pass
    return render_template('book.html')


@app.route('/dashboard')
def dashboard():
    
    # Ensure user is logged in
    return render_template('dashboard.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Include your routes here

if __name__ == '__main__':
    app.run(debug=True)
