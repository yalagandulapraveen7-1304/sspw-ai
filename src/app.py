import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_URL = "postgresql://postgres:ammulupremnishi1304@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"


from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)



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

# Route to catch the form submission (ONLY ONE EXISTS NOW)@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    # Assuming your frontend sends JSON data. Adjust to request.form if using standard HTML forms.
    data = request.json 
    name = data.get('name')
    phone = data.get('phone')
    service = data.get('service')
    vehicle = data.get('vehicle')
    message = data.get('message')

    try:
        # Connect to Supabase
        conn = psycopg2.connect(DB_URL)
        cursor = conn.cursor()
        
        # INSERT the data using %s placeholders
        cursor.execute('''
            INSERT INTO quotes (name, phone, service, vehicle, message)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, phone, service, vehicle, message))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Quote submitted successfully!'})
        
    except Exception as e:
        print(f"Database error: {e}") # This will log in Vercel so we can debug if it fails
        return jsonify({'success': False, 'error': 'Server error'}), 500
@app.route('/cost-estimator')
def cost_estimator():
    return render_template('cost-estimator.html')

if __name__ == '__main__':
    app.run(debug=True)