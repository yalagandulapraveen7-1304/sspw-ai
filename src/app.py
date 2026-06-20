import os
import psycopg2
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This is the ONLY initialization you need

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_URL = os.environ.get("DATABASE_URL")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    # 1. Open a fresh connection for this specific page load
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    
    try:
        # 2. Query the CORRECT table and sort by the CORRECT column
        cursor.execute("SELECT * FROM quotes ORDER BY id DESC")
        all_inquiries = cursor.fetchall()
    finally:
        # 3. CRITICAL: Always close the doors you open to prevent server crashes
        cursor.close()
        conn.close()
        
    return render_template('admin.html', inquiries=all_inquiries)

@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    # Use request.form so Flask can read the standard frontend FormData
    name = request.form.get('name')
    phone = request.form.get('phone')
    service = request.form.get('service')
    vehicle = request.form.get('vehicle')
    message = request.form.get('message')
    
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
    except Exception as e:
        print(f"Database error: {e}") 
        return jsonify({'success': False, 'error': 'Server error'}), 500
    finally:
        # Ensure we always close connections, even if it crashes
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            
    return jsonify({'success': True, 'message': 'Quote submitted successfully!'})

@app.route('/cost-estimator')
def cost_estimator():
    return render_template('cost-estimator.html')

# This allows local testing but correctly binds for Render in production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)