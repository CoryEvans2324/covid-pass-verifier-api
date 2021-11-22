import os

class Config:
    TRUSTED_ISSUERS = [
        'did:web:nzcp.covid19.health.nz',
        'did:web:nzcp.identity.health.nz'
    ]

    KEY_REFRESH_INTERVAL = 60 * 60 * 24  # 1 day

    KEY_FILE = 'keys.json'
    CORS_ORIGINS = [
        '*'
    ]
    CORS_ALWAYS_SEND = True

class ProductionConfig(Config):
    CORS_ORIGINS = os.getenv('CORS_ORIGINS').split(',')

class DevelopmentConfig(Config):
    pass