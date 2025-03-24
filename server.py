from flask import Flask, send_from_directory, render_template_string
import os

app = Flask(__name__, static_folder='public', template_folder='templates')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/public/<path:filename>')
def serve_static(filename):
    return send_from_directory('public', filename)

if __name__ == '__main__':
    os.makedirs('public', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)