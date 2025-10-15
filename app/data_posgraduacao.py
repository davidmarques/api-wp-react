import requests
import redis
import json
from app.conf_base import get_config

def get_posgraduacao(per_page=None, page=None):
    
    config = get_config()
    redis_client = redis.Redis(
        host=config['REDIS_HOST'],
        port=int(config['REDIS_PORT']),
        password=config['REDIS_PASSWORD'] or None,
        decode_responses=True
    )
    app_name = config['APP_NAME']
    cache_exp = config['CACHE_EXPIRATION']
    cache_key = f"{app_name}_posgraduacao:{per_page if per_page else 'recent'}:{page if page else 1}"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    base_url = config['WORDPRESS_API_URL']
    params = {
        'per_page': 20 if not per_page else int(per_page),
        'orderby': 'date',
        'order': 'desc',
        'page': 1 if not page else int(page)
    }
    url = f"{base_url}/wp/v2/pos-graduacao"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    items = []
    for item in resp.json():
        items.append(item)
    redis_client.set(cache_key, json.dumps(items), ex=cache_exp)
    return items
