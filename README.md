# 🛡️  Email Security Analyzer

A web-based email security dashboard that allows users to scan their inbox for suspicious emails and upload files for malware/virus scanning. Built using Flask, Python, HTML, CSS, JavaScript, and Bootstrap.

---

# ✨ Features

# 📧 Inbox Scan

* Connects to your email account via IMAP.
* Fetches the latest emails and checks for possible phishing attempts using keyword detection.
* Displays emails in a clean, interactive table with From, Subject, Date, and Status.

# 🗂️ File Scan

* Upload files to scan for potential malware using VirusTotal API.
* Displays scan results instantly on the dashboard.
* Full-screen, interactive file upload section.

# 🔐 User Authentication

* Sign up and login functionality.
* Keeps the user logged in until manually logged out.
* Passwords stored securely in SQLite database.

# 🖥️ Dashboard UI

* Sidebar menu to switch between Inbox Scan and File Scan.
* Clean, modern design using Bootstrap 5.
* Floating bubbles for subtle interactive background.

---

# 🛠️ Technologies Used

* Backend: Python, Flask, Flask-Login, SQLite
* Frontend: HTML, CSS, JavaScript, Bootstrap 5
* Email scanning: IMAP via `imaplib`
* File scanning: VirusTotal API
* Environment management: dotenv (`.env` file)

---

# 📂 Project Structure & File Descriptions

```
email-security-analyzer/
│
├── backend/                   # Flask backend
│   ├── app.py                 # Main Flask app with routes, authentication, file scanning
│   ├── email_scanner.py       # Email fetching & phishing detection via IMAP
│   ├── database.db            # SQLite database storing user info
│   ├── uploads/               # Folder for storing uploaded files temporarily
│   └── .env                   # Environment variables: email credentials, API keys, secret key
│
├── frontend/                  # Frontend files
│   ├── templates/             # HTML templates
│   │   ├── dashboard.html     # Main dashboard UI for inbox and file scan
│   │   ├── login.html         # Login page template
│   │   └── signup.html        # Signup page template
│   └── static/                # Static assets
│       ├── css/               # Custom CSS files
│       └── js/                # Custom JavaScript files
│
└── README.md                  # Project overview, setup, usage, and instructions
```

---

# ⚙️ Installation & Setup

# 1. Clone the repository

```bash
git clone https://github.com/anjeeta-rwt25/email-security-analyzer.git
cd email-security-analyzer/backend
```

# 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

# 3. Install dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, install manually:

```bash
pip install flask flask_sqlalchemy flask_login python-dotenv requests
```

# 4. Setup environment variables

Create a `.env` file in the backend folder:

```env
SECRET_KEY=your_secret_key
IMAP_HOST=imap.gmail.com
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_password
VT_API_KEY=your_virustotal_api_key
```

 # Important: For Gmail, you need to enable App Passwords if 2FA is on. Regular passwords may not work due to Google security policies.

# 5. Run the application

```bash
python3 app.py
```

* The app will automatically open in your browser at `http://127.0.0.1:5000`.
* Sign up, log in, and start scanning your inbox or files.

---

# 🚀 Usage

1. 📧 Inbox Scan

   * Click on Inbox Scan in the sidebar.
   * View latest emails and check their phishing status.

2. 🗂️ File Scan

   * Click on File Scan in the sidebar.
   * Upload any file and view VirusTotal scan results instantly.

3. 🔐 Logout

   * Click Logout in the sidebar to end the session.

---

# 📦 Dependencies

* Flask
* Flask-Login
* Flask-SQLAlchemy
* requests
* python-dotenv
* imaplib (built-in)
* email (built-in)
* hashlib (built-in)

---



## **📝 License**

This project is licensed under the **MIT License**. See `LICENSE` file for details.

---


