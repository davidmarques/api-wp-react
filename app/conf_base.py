import os
from dotenv import load_dotenv
from pathlib import Path

def get_config():
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    return {
        'WORDPRESS_API_URL': os.getenv('WORDPRESS_API_URL'),
        'WORDPRESS_API_USER': os.getenv('WORDPRESS_API_USER'),
        'WORDPRESS_API_PASSWORD': os.getenv('WORDPRESS_API_PASSWORD'),
        'REDIS_HOST': os.getenv('REDIS_HOST'),
        'REDIS_PORT': os.getenv('REDIS_PORT'),
        'REDIS_DB': os.getenv('REDIS_DB'),
        'REDIS_PASSWORD': os.getenv('REDIS_PASSWORD'),
        'APP_NAME': os.getenv('APP_NAME'),
        'CACHE_EXPIRATION': int(os.getenv('CACHE_EXPIRATION', '3600')),
    }
