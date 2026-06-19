from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

def setup_database():
    conn = sqlite3.connect('sspw_data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            service_required TEXT,
            vehicle_model TEXT,
            message TEXT,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

db_conn = setup_database()

# Route to serve your website
@app.route('/')
def home():
    return render_template('index.html')

# --- Admin Route ---
@app.route('/admin')
def admin_dashboard():
    cursor = db_conn.cursor()
    # Grab everything, sorted by newest first
    cursor.execute("SELECT * FROM contact_inquiries ORDER BY submitted_at DESC")
    all_inquiries = cursor.fetchall() 
    return render_template('admin.html', inquiries=all_inquiries)

# Route to catch the form submission (ONLY ONE EXISTS NOW)
@app.route('/submit-quote', methods=['POST'])
def handle_quote():
    name = request.form.get('name')
    phone = request.form.get('phone')
    service = request.form.get('service')
    vehicle = request.form.get('vehicle')
    message = request.form.get('message')

    # DIAGNOSTIC: This forces Python to print exactly what the browser sent
    print(f"--- INCOMING DATA: Name: {name}, Phone: {phone} ---")

    if not name or not phone:
        # Returning JSON instead of text prevents JS from crashing
        return jsonify({"status": "error", "message": "Name and Phone are required."}), 400

    cursor = db_conn.cursor()
    cursor.execute('''
        INSERT INTO contact_inquiries (name, phone_number, service_required, vehicle_model, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, phone, service, vehicle, message))
    db_conn.commit()

    return jsonify({"status": "success", "message": "Quote request received successfully!"})
@app.route('/cost-estimator')
def cost_estimator():
    return render_template('cost-estimator.html')

if __name__ == '__main__':
    app.run(debug=True)