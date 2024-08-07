import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')  

if not BASE_URL:
    raise ValueError("A URL base não foi encontrada. Verifique o arquivo .env.")

def make_api_url(module: str, action: str, **params) -> str:
    api_key = os.getenv('ETHERSCAN_API_KEY')
    if not api_key:
        raise ValueError("A chave de API não foi encontrada. Verifique o arquivo .env.")

    params_list = [f"{key}={value}" for key, value in params.items()]
    params_str = "&".join(params_list)
    url = f"{BASE_URL}?module={module}&action={action}&{params_str}&apikey={api_key}"
    return url

def get_balance_by_address(address: str) -> dict:
    url = make_api_url(module="account", action="balance", address=address, tag="latest")
    response = requests.get(url)
    return response.json()

def get_last_block() -> dict:
    url = make_api_url(module="proxy", action="eth_blockNumber")
    response = requests.get(url)
    return response.json()
