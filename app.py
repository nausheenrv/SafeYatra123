from flask import Flask, render_template, request, redirect, url_for, flash
import os

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
    return render_template('sign_in.html')

@app.route('/sign_in', methods=['POST'])
def sign_in():
    email = request.form['email']
    password = request.form['password']
    
    if email in users and users[email] == password:
        flash('Sign in successful!', 'success')
        return redirect(url_for('maps_page'))  # Redirect to maps page on successful sign-in
    else:
        flash('Invalid email or password', 'danger')
        return redirect(url_for('home'))

@app.route('/maps')
def maps_page():
    return render_template('maps_page.html')  # Render the maps page

@app.route('/guardian_setup', methods=['GET', 'POST'])
def guardian_setup():
    if request.method == 'POST':
        guardian_name = request.form['guardian_name']
        phone_number = request.form['phone_number']
        email_address = request.form['email_address']
        home_address = request.form['home_address']
        
        flash('Guardian setup complete!', 'success')
        return redirect(url_for('maps_page'))  # Redirect back to the maps page after submission

    return render_template('guardian_setup.html')  # Render the guardian setup page

@app.route('/profile_setup', methods=['GET', 'POST'])
def profile_setup():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        emergency_contact = request.form['emergency_contact']
        home_address = request.form['home_address']
        work_address = request.form['work_address']
        
        flash('Profile setup complete!', 'success')
        return redirect(url_for('maps_page'))  # Redirect back to the maps page after submission

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

    return render_template('submit_incident.html')  # Render the incident submission page

if __name__ == '__main__':
    app.run(debug=True)