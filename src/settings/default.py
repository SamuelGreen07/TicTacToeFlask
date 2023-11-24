import os


locales = ['en_EN', 'en']


DATABASE_CONFIG = {
    'DEFAULT': {
        'ENGINE': 'asyncpg',
        'NAME': os.getenv('PG_DB', 'TicTacToe'),
        'USER': os.getenv('PG_USER', 'aurora'),
        'PASSWORD': os.getenv('PG_PASSWORD', 'aurorapass'),
        'HOST': os.getenv('PG_HOST', 'localhost'),
        'PORT': os.getenv('PG_PORT', 5431),
        'MAX_POOL': os.getenv('MAX_POOL', 10),
        'MIN_POOL': os.getenv('MIN_POOL', 1),
        'MIGRATIONS': {
            'ENGINE': 'postgresql'
        }
    }
}