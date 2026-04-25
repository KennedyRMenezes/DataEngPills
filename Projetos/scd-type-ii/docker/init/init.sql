CREATE TABLE coin_price_scd(
    id SERIAL PRIMARY KEY,
    coin VARCHAR(50) NOT NULL,
    price NUMERIC(18, 8) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP,
    current_flag BOOLEAN NOT NULL
);

CREATE UNIQUE INDEX unique_current_coin
ON coin_price_scd (coin)
WHERE current_flag = TRUE;