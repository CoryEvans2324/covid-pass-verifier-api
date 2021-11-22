import os

class Config:
    TRUSTED_ISSUERS = [
        'did:web:nzcp.covid19.health.nz',
        'did:web:nzcp.identity.health.nz'
    ]

    REFRESH_TOKEN = os.getenv('REFRESH_TOKEN')

    KEY_FILE = 'keys.json'
    CORS_ORIGINS = [
        '*'
    ]
    CORS_ALWAYS_SEND = True

class ProductionConfig(Config):
    CORS_ORIGINS = os.getenv('CORS_ORIGINS').split(',')

class DevelopmentConfig(Config):
    pass