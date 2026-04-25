import requests

def get_coin_price(coin_name, api_key):

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "vs_currencies": "usd",
        "ids": coin_name,
        "x_cg_demo_api_key": api_key
    }
    
    try: 
        response = requests.get(url, params=params)

        if response.status_code == 401:
            print("Problema com a requisição")


        data = response.json()
        return data.get(coin_name).get("usd")
    
    except requests.exceptions.RequestException as e:
        print(f"[ERRO] Falha na requisição: {e}")





