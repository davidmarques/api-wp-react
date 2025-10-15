from fastapi import FastAPI, Query, HTTPException
from app.data_posts import get_posts_by_category
from app.data_posgraduacao import get_posgraduacao
from app.conf_base import get_config
import redis

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API FastAPI rodando!"}

@app.get("/posts_by_cat/{cat}")
def posts_by_cat(cat: str, per_page: int = Query(None, alias="per_page"), page: int = Query(None, alias="page")):
    posts = get_posts_by_category(cat, per_page, page)
    return {"posts": posts}

@app.get("/pos-graduacao")
def pos_graduacao(per_page: int = Query(None, alias="per_page"), page: int = Query(None, alias="page")):
    print("Vamos buscar pos-graduacao")
    items = get_posgraduacao(per_page, page)
    return {"pos_graduacao": items}

@app.post("/purge_cache")
def purge_cache(secret: str = Query(..., alias="secret")):
    config = get_config()
    if secret != config.get("REDIS_PASSWORD"):
        raise HTTPException(status_code=403, detail="Unauthorized")
    redis_client = redis.Redis(
        host=config['REDIS_HOST'],
        port=int(config['REDIS_PORT']),
        password=config['REDIS_PASSWORD'] or None,
        decode_responses=True
    )
    prefix = f"{config['APP_NAME']}_posts:"
    keys = redis_client.keys(f"{prefix}*")
    deleted = 0
    for k in keys:
        redis_client.delete(k)
        deleted += 1
    return {"purged_keys": deleted}