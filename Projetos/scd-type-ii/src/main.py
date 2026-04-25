from extract import *
from load import *
from aux_functions import *
import os

from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5433/project_scd_ii")
coin_api_key = os.getenv("coin-api-key")
name_coin = 'bitcoin'

with engine.begin() as conn:
    coin_price = get_coin_price(name_coin, coin_api_key)
    print(coin_price)

    curr_price = get_current_price(conn, name_coin)
    print(curr_price)

    apply_scd2(conn, coin_price, curr_price)


    


