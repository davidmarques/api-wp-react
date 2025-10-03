import requests
import redis
import json
from app.conf_base import get_config

def get_posts_by_category(cat_name, per_page=None, page=None):
    print(f"Fetching posts for category '{cat_name}' with pagination {per_page} and page {page}")
    config = get_config()
    redis_client = redis.Redis(
        host=config['REDIS_HOST'],
        port=int(config['REDIS_PORT']),
        password=config['REDIS_PASSWORD'] or None,
        decode_responses=True
    )

    app_name = config['APP_NAME']
    cache_exp = config['CACHE_EXPIRATION']
    # Buscar o ID da categoria pelo nome
    cat_url = f"{config['WORDPRESS_API_URL']}/wp/v2/categories"
    cat_resp = requests.get(cat_url, params={"search": cat_name})
    cat_resp.raise_for_status()
    cat_data = cat_resp.json()
    if not cat_data:
        return []
    cat_id = cat_data[0]['id']
    cache_key = f"{app_name}_posts:{cat_name}:{per_page if per_page else 'recent'}:{page if page else 1}"
    print("usando a chave de cache:", cache_key)
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    # Monta URL da API do WP
    base_url = config['WORDPRESS_API_URL']
    params = {
        'categories': cat_id,
        'per_page': 20 if not per_page else int(per_page),
        'orderby': 'date',
        'order': 'desc',
        'page': 1 if not page else int(page)
    }
    url = f"{base_url}/wp/v2/posts"
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    posts = []
    for post in resp.json():
        posts.append({
            'date': post.get('date'),
            'featured_image': post.get('featured_media'),
            'slug': post.get('slug'),
            'title': post.get('title', {}).get('rendered'),
            'excerpt': post.get('excerpt', {}).get('rendered'),
            'content': post.get('content', {}).get('rendered'),
        })
    redis_client.set(cache_key, json.dumps(posts), ex=cache_exp)
    return posts
