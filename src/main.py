import os
from typing import Optional
from get_price import getPrice
from fastapi import FastAPI
from fastapi import FastAPI, Request, Response
from fastapi_redis_cache import FastApiRedisCache, cache

LOCAL_REDIS_URL = "redis://redis:6379"

app = FastAPI(title="FastAPI Swap Token Pair Price")


@app.on_event("startup")
def startup():
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url=os.environ.get("REDIS_URL", LOCAL_REDIS_URL),
        prefix="Pair-Price",
        response_header="X-Redis-Cache",
        ignore_arg_types=[Request, Response]
    )

# TODO Make function generalized
@app.get("/gdr-wkub")
@cache(expire=60)
def get_gdr_wkub_pair_cache():
    return getPrice(chain="BKC", factory="TukTuk", pair="WKUB/GDR")
