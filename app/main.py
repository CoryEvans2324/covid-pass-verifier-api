import os
import json
import time

from functools import wraps

from flask import (
    Flask,
    jsonify,
    request
)

from flask_cors import CORS

from app import verify, keys, settings

app = Flask(__name__)
if os.getenv('FLASK_ENV', 'production') == 'development':
    app.config.from_object(settings.DevelopmentConfig)
else:
    app.config.from_object(settings.ProductionConfig)

cors = CORS(app)

if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

def refresh_keys():
    jwks = []
    for issuer in app.config['TRUSTED_ISSUERS']:
        did_json = keys.get_did(issuer)
        jwks += keys.parse_did(did_json)
    
    with open(os.path.join(app.instance_path, app.config['KEY_FILE']), 'w') as f:
        json.dump(jwks, f)

def ensure_keys_exist(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key_file_path = os.path.join(app.instance_path, app.config['KEY_FILE'])
        if not os.path.exists(key_file_path):
            refresh_keys()

        elif os.path.getmtime(key_file_path) < time.time() - app.config['KEY_REFRESH_INTERVAL']:
            refresh_keys()
        
        return func(*args, **kwargs)
    return wrapper

@app.route('/verify', methods=['POST'])
@ensure_keys_exist
def verify_token():
    uri = request.json.get('uri')
    if not uri.startswith('NZCP:/'):
        return make_resonse(None, 'Invalid QR Code')

    uri = uri[6:]
    version, b32data = uri.split('/')

    with open(os.path.join(app.instance_path, app.config['KEY_FILE'])) as f:
        key_list = json.load(f)

    claims, error_msg = verify.verify_and_decode(b32data, key_list)
    if error_msg:
        return make_resonse(None, error_msg)

    # translate the claims
    claims = {
        verify.CLAIM_KEYS.get(k, str(k)): v
        for k, v in claims.items()
    }

    if claims['iss'] not in app.config['TRUSTED_ISSUERS']:
        return make_resonse(claims, 'Issuer not in trusted list')

    return make_resonse(claims)

def make_resonse(claims, error_msg=None):
    if not claims:
        return jsonify({
            'success': False,
            'error': error_msg
        }), 401

    if error_msg:
        return jsonify({
            'success': False,
            'error': error_msg,
            'claims': claims['vc']
        }), 401

    return jsonify({
        'success': True,
        'claims': claims['vc']
    })