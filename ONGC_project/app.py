from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ongc_portal'

# Secret key for session
app.secret_key = os.urandom(24)

# Initialize MySQL
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/employees')
def employees():
    return render_template('employees.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        cpf_number = request.form['cpf_number']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE cpf_number = %s', [cpf_number])
        user = cur.fetchone()
        cur.close()
        
        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]
            session['cpf_number'] = user[1]
            return jsonify({'success': True})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contact_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)',
                    [name, email, subject, message])
        mysql.connection.commit()
        cur.close()
        
        return jsonify({'success': True, 'message': 'Message sent successfully'})

if __name__ == '__main__':
    app.run(debug=True)