import os
import requests
import hashlib
import threading
import webbrowser
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from email_scanner import scan_emails  # Your IMAP email scanning function

# Load environment variables
load_dotenv()

frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(upload_folder, exist_ok=True)

app = Flask(__name__,
            template_folder=os.path.join(frontend_path, 'templates'),
            static_folder=os.path.join(frontend_path, 'static'))

app.secret_key = os.getenv("SECRET_KEY", "your_secret_key")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------- User Model -----------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ----------------- Routes -----------------
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Fetch inbox emails
    inbox_results = scan_emails(max_messages=30)
    
    # Determine which section to show (inbox or file)
    section = request.args.get('section', 'inbox')
    file_scan_message = request.args.get('file_scan_message', None)
    
    return render_template('dashboard.html', results=inbox_results, section=section, file_scan_message=file_scan_message)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash("No file part in request", "danger")
        return redirect(url_for('dashboard'))

    file = request.files['file']
    if file.filename == '':
        flash("No file selected", "warning")
        return redirect(url_for('dashboard'))

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    vt_url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": os.getenv("VT_API_KEY")}
    response = requests.get(vt_url, headers=headers)

    if response.ok and response.json().get("data"):
        scan_msg = "⚠️ File flagged by VirusTotal!"
    else:
        scan_msg = "✅ File appears clean."

    # Redirect to dashboard and show File Scan section automatically
    return redirect(url_for('dashboard', section='file', file_scan_message=scan_msg))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email_input = request.form.get('email')
        password_input = request.form.get('password')
        user = User.query.filter_by(email=email_input).first()
        if user and user.password == password_input:
            login_user(user, remember=True)  # Remember login
            
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email_input = request.form.get('email')
        password_input = request.form.get('password')
        if User.query.filter_by(email=email_input).first():
            flash('Email already registered.', 'warning')
            return redirect(url_for('login'))
        user = User(email=email_input, password=password_input)
        db.session.add(user)
        db.session.commit()
        flash('Signup successful!', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('login'))

# ----------------- Utility -----------------
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

# ----------------- Main -----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    threading.Timer(1.0, open_browser).start()  # Opens browser automatically
    app.run(debug=True)
