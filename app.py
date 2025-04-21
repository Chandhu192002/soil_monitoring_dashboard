# Updated app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import threading
from notification_alert import check_and_notify # type: ignore

app = Flask(__name__, template_folder='templates')
CORS(app)

latest_data = {
    'moisture': 0,
    'distance': 0
}

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/data', methods=['POST'])
def receive_data():
    global latest_data
    data = request.get_json()
    print("Received data:", data)
    latest_data = {
        'moisture': data.get('moisture', 0),
        'distance': data.get('distance', 0)
    }

    # Run notifications in background
    threading.Thread(target=check_and_notify, args=(latest_data['moisture'], latest_data['distance'])).start()
    return jsonify({'status': 'success'}), 200

@app.route('/api/latest-data', methods=['GET'])
def get_latest_data():
    return jsonify(latest_data)

if __name__ == '__main__':
    app.run(host='192.168.12.109', port=5500, debug=True)
