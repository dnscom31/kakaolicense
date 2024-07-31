from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

LICENSE_KEY_PREFIX = "MYAPP"
LICENSE_KEY_SECRET = "your_secret_here"
licenses = {}


def generate_license_key(user_id):
    combined_string = f"{LICENSE_KEY_PREFIX}{user_id}{LICENSE_KEY_SECRET}"
    return hashlib.sha256(combined_string.encode()).hexdigest()


@app.route('/register', methods=['POST'])
def register_license():
    data = request.json
    user_id = data['user_id']
    mac_address = data['mac_address']
    license_key = data['license_key']

    expected_license_key = generate_license_key(user_id)
    if expected_license_key != license_key:
        return jsonify({'status': 'invalid license key'}), 400

    licenses[user_id] = {'license_key': license_key, 'mac_address': mac_address}
    return jsonify({'status': 'success'})


@app.route('/verify', methods=['POST'])
def verify_license():
    data = request.json
    user_id = data['user_id']
    mac_address = data['mac_address']
    license_key = data['license_key']

    if user_id in licenses:
        stored_license = licenses[user_id]
        if stored_license['license_key'] == license_key and stored_license['mac_address'] == mac_address:
            return jsonify({'status': 'valid'})
    return jsonify({'status': 'invalid'}), 400


if __name__ == '__main__':
    app.run(debug=True)
