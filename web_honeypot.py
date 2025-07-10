# Import library dependencies.
from flask import Flask, render_template, request, redirect, url_for
import logging
from logging.handlers import RotatingFileHandler
from dashboard_data_parser import * 
from pathlib import Path

# Logging Format
logging_format = logging.Formatter('%(asctime)s %(message)s')

base_dir = base_dir = Path(__file__).parent.parent
http_audits_log_local_file_path = base_dir / 'honeypot' / 'log_files' / 'http_audit.log'

# HTTP Logger
event_logger = logging.getLogger('HTTPLogger')
event_logger.setLevel(logging.INFO)
event_handler = RotatingFileHandler(http_audits_log_local_file_path, maxBytes=2000, backupCount=5)
event_handler.setFormatter(logging_format)
event_logger.addHandler(event_handler)

def baseline_web_honeypot(input_username="admin", input_password="veryhardpassword"):

    app = Flask(__name__)

    @app.route('/')
    
    def index():
        return render_template('wp-admin.html')

    @app.route('/wp-admin-login', methods=['POST'])

    def login():
        username = request.form['username']
        password = request.form['password']

        ip_address = request.remote_addr

        event_logger.info(f'Client with IP Address: {ip_address} entered\n Username: {username}, Password: {password}')

        if username == input_username and password == input_password:
            return 'SUCCESFULLY LOGGED IN!'
        else:
            return "Invalid username or password, please try again."
        
    return app

def run_app(port=5000, input_username="admin", input_password="veryhardpassword"):
     app = baseline_web_honeypot(input_username, input_password)
     app.run(debug=True, port=port, host="0.0.0.0")

     return app

