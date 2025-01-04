#trial workspace
# from flask import Flask, render_template, request, redirect, url_for, flash
# import os

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Needed for session management

# # Configure upload folder and allowed extensions
# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Dummy user data for demonstration
# users = {
#     "user@example.com": "password123"
# }

# # Sample incident data
# incidents = [
#     {
#         'title': 'Incident in Delhi Park',
#         'description': 'A woman reported being harassed by a group of men in a public park in Delhi.',
#         'image': 'https://via.placeholder.com/150',  # Replace with actual image URL
#         'location': 'Delhi, India',
#         'upvotes': 10,
#         'downvotes': 2
#     },
#     # ... other incidents ...
# ]

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/')
# def home():
#     return render_template('welcome.html')  # Render the welcome page first

# @app.route('/sign_in', methods=['GET', 'POST'])
# def sign_in():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
        
#         if email in users and users[email] == password:
#             flash('Sign in successful!', 'success')
#             return redirect(url_for('maps_page'))  # Redirect to maps page on successful sign-in
#         else:
#             flash('Invalid email or password', 'danger')
#             return redirect(url_for('sign_in'))
#     return render_template('sign_in.html')  # Render the sign-in page

# @app.route('/maps')
# def maps_page():
#     return render_template('maps_page.html')  # Render the maps page

# @app.route('/guardian_setup', methods=['GET', 'POST'])
# def guardian_setup():
#     if request.method == 'POST':
#         guardian_name = request.form['guardian_name']
#         phone_number = request.form['phone_number']
#         email_address = request.form['email_address']
#         home_address = request.form['home_address']
        
#         flash('Guardian setup complete!', 'success')
#         return redirect(url_for('maps_page'))  # Redirect back to the maps page after submission
#     return render_template('guardian_setup.html')  # Render the guardian setup page

# @app.route('/profile_setup', methods=['GET', 'POST'])
# def profile_setup():
#     if request.method == 'POST':
#         vehicle_number = request.form['vehicle_number']
#         emergency_contact = request.form['emergency_contact']
#         home_address = request.form['home_address']
#         work_address = request.form['work_address']
        
#         flash('Profile setup complete!', 'success')
#         return redirect(url_for('maps_page'))  # Redirect back to the maps page after submission
#     return render_template('profile_setup.html')  # Render the profile setup page

# @app.route('/community')
# def community():
#     return render_template('community.html', incidents=incidents)  # Render the community page with incidents

# @app.route('/submit_incident', methods=['GET', 'POST'])
# def submit_incident():
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         location = request.form['location']
#         file = request.files['image']

#         if file and allowed_file(file.filename):
#             filename = file.filename
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             image_path = os.path.join('static/uploads', filename)

#             # Add the new incident to the incidents list
#             incidents.append({
#                 'title': title,
#                 'description': description,
#                 'image': image_path,
#                 'location': location,
#                 'upvotes': 0,
#                 'downvotes': 0
#             })

#             flash('Incident submitted successfully!', 'success')
#             return redirect(url_for('community'))  # Redirect to the community page
#     return render_template('submit_incident.html')  # Render the submit incident page

# if __name__ == '__main__':
#     app.run(debug=True)  # Run the Flask app in debug mode
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Dummy user data for demonstration
users = {
    "user@example.com": "password123"
}

# Sample incident data
incidents = [
    {
        'title': 'Incident in Delhi Park',
        'description': 'A woman reported being harassed by a group of men in a public park in Delhi.',
        'image': 'https://via.placeholder.com/150',  # Replace with actual image URL
        'location': 'Delhi, India',
        'upvotes': 10,
        'downvotes': 2
    },
    # ... other incidents ...
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('welcome.html')  # Render the welcome page first

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users and users[email] == password:
            flash('Sign in successful!', 'success')
            return redirect(url_for('maps'))  # Redirect to maps page on successful sign-in
        else:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('sign_in'))
    return render_template('sign_in.html')  # Render the sign-in page

@app.route('/sign_up_1', methods=['GET', 'POST'])
def sign_up_1():
    if request.method == 'POST':
        email = request.form['email']
        dob = request.form['dob']
        gender = request.form['gender']

        # Calculate age based on date of birth
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

        # Store temporary user data in session
        session['temp_user_data'] = {
            'email': email,
            'dob': dob,
            'gender': gender,
            'age': age
        }

        # Redirect to the next step
        return redirect(url_for('sign_up_2'))
    return render_template('sign_up_1.html')
@app.route('/sign_up_2', methods=['GET', 'POST'])
def sign_up_2():
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('sign_up_2'))

        # Retrieve temporary user data from session
        temp_user_data = session.get('temp_user_data', {})

        # Add password to temporary user data
        temp_user_data['password'] = password

        # Redirect based on age
        if temp_user_data['age'] <= 15:
            return redirect(url_for('guardian_setup'))
        else:
            return redirect(url_for('maps'))

    return render_template('sign_up_2.html')

@app.route('/maps')
def maps_page():
    return render_template('maps_page.html')  # Render the maps_page.html template

@app.route('/maps_page')
def maps():
    return render_template('maps_page1.html')  # Render the maps_page1.html template

@app.route('/guardian_setup', methods=['GET', 'POST'])
def guardian_setup():
    if request.method == 'POST':
        guardian_name = request.form['guardian_name']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        home_address = request.form['home_address']
        
        flash('Guardian setup complete!', 'success')
        return redirect(url_for('maps'))  # Redirect back to the maps page after submission
    return render_template('guardian_setup.html')  # Render the guardian setup page

@app.route('/profile_setup', methods=['GET', 'POST'])
def profile_setup():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        emergency_contact = request.form['emergency_contact']
        home_address = request.form['home_address']
        work_address = request.form['work_address']
        
        flash('Profile setup complete!', 'success')
        return redirect(url_for('maps'))  # Redirect back to the maps page after submission
    return render_template('profile_setup.html')  # Render the profile setup page

@app.route('/community')
def community():
    return render_template('community.html', incidents=incidents)  # Render the community page with incidents

@app.route('/submit_incident', methods=['GET', 'POST'])
def submit_incident():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = os.path.join('static/uploads', filename)

            # Add the new incident to the incidents list
            incidents.append({
                'title': title,
                'description': description,
                'image': image_path,
                'location': location,
                'upvotes': 0,
                'downvotes': 0
            })

            flash('Incident submitted successfully!', 'success')
            return redirect(url_for('community'))  # Redirect to the community page
    return render_template('submit_incident.html')  # Render the submit incident page

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode