from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from collections import OrderedDict
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/blog')
def blog():
    posts = [
        {'title': 'Life Cycle', 'content': 'Life is like riding a bicycle. To keep your balance, you must keep moving.'},
        {'title': 'Radfahren', 'content': 'Lebe deinen Traum auf zwei Räder.'},
        {'title': 'Programming', 'content': 'Keep it simple.'}
    ]
    return render_template('blog.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = users.get(username)
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        
        if new_username in users:
            flash('Username already exists', 'danger')
        else:
            hashed_password = generate_password_hash(new_password)
            users[new_username] = {'username': new_username, 'password': hashed_password}
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('login.html')



@app.route('/resume')
def resume():
    return send_from_directory('.', 'static/images/Resume-ENG.pdf')


# @app.route('/api/personal-info', methods=['GET'])
# def personal_info():
#     personal_data = OrderedDict({
#         'name': 'Alireza Etezad',
#         'profession': 'IT Engineer',
#         'skills': ['Python', 'Flask', 'SQL', 'HTML', 'CSS'],
#         'hobbies': ['Cycling', 'Reading', 'Hiking'],
#         'contact': {
#             'address': 'Marzdaran St, Tehran, Iran',
#             'phone': '+98-901-3841134',
#             'email': 'ar_etezad@yahoo.com'
#         }
#     })
#     return jsonify(personal_data)


@app.route('/api/personal-info', methods=['GET'])
def personal_info():
    personal_data = OrderedDict([
        ('name', 'Alireza Etezad'),
        ('profession', 'IT Engineer'),
        ('skills', ['Python', 'Flask', 'SQL', 'HTML', 'CSS']),
        ('hobbies', ['Cycling', 'Reading', 'Hiking']),
        ('contact', OrderedDict([
            ('phone', '+98-901-3841134'),
            ('email', 'ar_etezad@yahoo.com'),
            ('address', 'Marzdaran St, Tehran, Iran')
        ]))
    ])
    
    # Use json.dumps to manually create the JSON with correct ordering
    response = Response(json.dumps(personal_data), mimetype='application/json')
    return response

# if __name__ == '__main__':
#    # app.run(debug=True)
#     ...