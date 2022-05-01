import os
from get_price import getPrice
from fastapi import FastAPI
from fastapi import FastAPI, Request, Response
from fastapi_redis_cache import FastApiRedisCache, cache
from dotenv import load_dotenv
load_dotenv()

PYTHON_ENV = os.getenv("PYTHON_ENV", "development")

app = FastAPI(title="FastAPI Swap Token Pair Price",
              docs_url="/docs"if PYTHON_ENV != "production"else None,
              redoc_url="/redoc"if PYTHON_ENV != "production"else None)


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", "redis://redis:6379"),
        prefix="Pair-Price",
        response_header="X-Redis-Cache",
        ignore_arg_types=[Request, Response]
    )

# TODO: Make function generalized


@app.get("/gdr-wkub")
@cache(expire=60)
def get_gdr_wkub_pair_cache():
    return getPrice(chain="BKC", factory="TukTuk", pair="WKUB/GDR")

@app.get("/health-check")
def health_check():
    return { "status": "OK", "app_revision": os.environ.get("APP_REVISION", "") }
