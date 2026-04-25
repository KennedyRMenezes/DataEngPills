from sqlalchemy import text

def test_conn(engine):
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(result.fetchone())

    except Exception as e:
        print("[ERRO SQLALCHEMY]", repr(e))


def get_current_price(conn, coin_name):


    query = """
        SELECT price
        FROM coin_price_scd
        WHERE coin = :coin_name
        AND current_flag = TRUE
    """

    result = conn.execute(text(query), {"coin_name": coin_name})
    row = result.fetchone()
    return row[0] if row else None