import os
import sys
import json
import base64
import urllib.request
import urllib.parse
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

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
        print(f"Image upload error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
