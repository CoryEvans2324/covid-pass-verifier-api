import cwt
import json
import base64

CLAIM_KEYS = {
    1: 'iss',
    2: 'sub',
    3: 'aud',
    4: 'exp',
    5: 'nbf',
    6: 'iat',
    7: 'cti'
}

def decode_base32(data):
    missing_padding = len(data) % 8

    char = '='
    if isinstance(data, bytes):
        char = b'='

    if missing_padding != 0:
        data += char * (8 - missing_padding)
    return base64.b32decode(data)

def decode_base64(data):
    return base64.urlsafe_b64decode(data + '=' * (4 - len(data) % 4))



def verify_and_decode(b32data: str, public_keys_jwk: list):
    pub_keys = [cwt.COSEKey.from_jwk(k) for k in public_keys_jwk]

    raw = decode_base32(b32data)
    try:
        claims = cwt.decode(raw, keys=pub_keys)
    except Exception as e:
        return None, str(e)
    

    # Check claims
    return claims, None
