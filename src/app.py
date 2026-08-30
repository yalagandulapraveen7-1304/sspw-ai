import os
import sys
import json
import base64
import urllib.request
import urllib.parse
import psycopg2
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_basicauth import BasicAuth # 1. Import the security tool

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['BASIC_AUTH_USERNAME'] = 'santhosh'
app.config['BASIC_AUTH_PASSWORD'] = 'prashanthi'

basic_auth = BasicAuth(app)
CORS(app)
DB_URL = os.environ.get("DATABASE_URL")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
@basic_auth.required
def admin_dashboard():
    all_inquiries = []
    error_message = None
    
    if not DB_URL:
        error_message = "DATABASE_URL is not set. Please add your Supabase/PostgreSQL connection string to your Vercel / Render Environment Variables."
    else:
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(DB_URL)
            cursor = conn.cursor()
            # Ensure table exists so it doesn't fail on fresh databases
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS quotes (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    service TEXT,
                    vehicle TEXT,
                    message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
            
            cursor.execute("""
                SELECT 
                    id, 
                    COALESCE(name, 'N/A'), 
                    COALESCE(phone, 'N/A'), 
                    COALESCE(service, 'General Inquiry'), 
                    COALESCE(vehicle, 'N/A'), 
                    COALESCE(message, '-'), 
                    COALESCE(to_char(created_at, 'DD Mon YYYY, HH:MI AM'), 'Recent')
                FROM quotes 
                ORDER BY id DESC
            """)
            all_inquiries = cursor.fetchall()
        except Exception as e:
            print(f"Database error in admin dashboard: {e}")
            error_message = f"Database Error: {str(e)}"
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        
    return render_template('admin.html', inquiries=all_inquiries, error_message=error_message)

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

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    try:
        image_b64 = None
        if 'image' in request.files:
            file = request.files['image']
            image_b64 = base64.b64encode(file.read()).decode('utf-8')
        elif request.form.get('source'):
            image_b64 = request.form.get('source')
            if ',' in image_b64:
                image_b64 = image_b64.split(',')[1]
        elif request.is_json and request.json.get('source'):
            image_b64 = request.json.get('source')
            if ',' in image_b64:
                image_b64 = image_b64.split(',')[1]

        if not image_b64:
            return jsonify({'success': False, 'error': 'No image provided'}), 400

        data = urllib.parse.urlencode({
            'key': '6d207e02198a847aa98d0a2a901485a5',
            'action': 'upload',
            'source': image_b64,
            'format': 'json'
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://freeimage.host/api/1/upload',
            data=data,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            image_url = res.get('image', {}).get('url')
            if image_url:
                return jsonify({'success': True, 'url': image_url})
            else:
                return jsonify({'success': False, 'error': 'Upload failed'}), 500
    except Exception as e:
        print(f"Server-side image upload error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# This allows local testing but correctly binds for Render in production
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
