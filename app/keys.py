import json
import requests

def get_did(issuer: str):
    issuer_domain = issuer.split(':')[2]

    resp = requests.get(
        f'https://{issuer_domain}/.well-known/did.json'
    )

    if resp.status_code != 200:
        return None
    
    return resp.json()

def parse_did(did: dict = None) -> list:

    if not did:
        return []

    keys = []
    for key in did['verificationMethod']:
        issuer, kid = key['id'].split('#')
        key['publicKeyJwk']['key_ops'] = ['verify']
        key['publicKeyJwk']['kid'] = kid

        keys.append(key['publicKeyJwk'])

    return keys
