from typing import Optional
from get_price import getPrice
from fastapi import FastAPI

app = FastAPI()

# TODO Make function generalized
@app.get("/gdr-wkub")
def get_gdr_wkub_pair():
    return getPrice(chain="BKC", factory="TukTuk", pair="WKUB/GDR")
