# ssh-http-honeypot

A lightweight combined SSH + HTTP honeypot with a real-time dashboard.  
It captures incoming SSH login attempts (credentials & commands) and HTTP requests, then visualizes them via a simple web interface.

---

## 1. Quick Local Run

1. **Clone and install dependencies**  
   ```bash
   git clone https://github.com/KacperKolasa/ssh-http-honeypot.git
   cd ssh-http-honeypot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the honeypots**  
   In one terminal run the following to start the SSH honeypot:  
   ```bash
   python honeypot.py -a 0.0.0.0 -p 22 -s
   ```
   Or the following to start the HTTP honeypot:
   ```bash
   python honeypot.py -a 0.0.0.0 -p 80 -wh
   ```

3. **Launch the dashboard**  
   In another terminal:  
   ```bash
   python web_app.py
   ```  
   Then visit http://localhost:8050/ to see live attack stats.

---

## 2. Hosting on a VPS (e.g. Hostinger)

1. **Push your code** to the VPS (git clone is recommended).  
2. **Open firewall ports**  
   - **Hostinger Cloud Firewall**: add inbound rules for your SSH port and HTTP_PORT.  
   - **Ubuntu UFW** on the VPS:  
     ```bash
     sudo ufw allow 22/tcp    # SSH honeypot port
     sudo ufw allow 80/tcp    # HTTP honeypot port
     sudo ufw allow 8050/tcp    # Dashboard port
     ```

3. **Run services** just like locally:  
   ```bash
   source venv/bin/activate
   python honeypot.py -a 0.0.0.0 -p 22 -s
   python web_app.py
   ```

4. **Browse**  
   - Honeypots: ssh -p 22 attacker@<VPS_IP> and http://<VPS_IP>:80/
   - Dashboard: http://<VPS_IP>:8050/

---

## 3. Sample Findings (2-day Run)

Below is a screenshot of the findings over 2 days:

![Dashboard screenshot](assets/images/dashboard.png)

