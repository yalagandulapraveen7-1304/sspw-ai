import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_URL = "postgresql://postgres:9lkVPMXKCm9Mvvgp@db.xqtetjnwycdyyxlbbyko.supabase.co:5432/postgres"


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

# Route to catch the form submission (ONLY ONE EXISTS NOW)@app.route('/submit-quote', methods=['PO# Route to catch the form submission
# Leave this exactly as it is
@app.route('/submit-quote', methods=['POST'])
def submit_quote():
    # Delete the request.json line entirely.
    # Use request.form so Flask can read the standard frontend FormData
    name = request.form.get('name')
    phone = request.form.get('phone')
    service = request.form.get('service')
    vehicle = request.form.get('vehicle')
    message = request.form.get('message')
    
    # ... the rest of your Supabase database code stays exactly the same ...
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