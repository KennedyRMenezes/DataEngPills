from sqlalchemy import create_engine, text
from datetime import datetime


def apply_scd2(conn, new_price, current_price):
    now = datetime.now()

    # First insertion
    if current_price is None:
        conn.execute(text("""
            INSERT INTO coin_price_scd(coin, price, start_date, end_date, current_flag)
            VALUES ('bitcoin', :price, :start, NULL, TRUE)
        """), {"price": new_price, "start": now})
    
    if new_price == current_price:
        return
    
    # New insertion (already exisits one in database)
    conn.execute(text("""
        UPDATE coin_price_scd
        SET end_date = :now,
            current_flag = FALSE
        WHERE coin = 'bitcoin'
        AND current_flag = TRUE
    """), {"now": now})

    conn.execute(text("""
        INSERT INTO coin_price_scd (coin, price, start_date, end_date, current_flag)
        VALUES ('bitcoin', :price, :start, NULL, TRUE)
    """), {"price": new_price, "start": now})