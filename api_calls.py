import os
import requests
from dotenv import load_dotenv
from clean_api_calls import *

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
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lançar HTTPError para respostas ruins
        data = response.json()
        return clean_account_balance(data)
    except requests.exceptions.RequestException as e:
        return {"error": f"HTTP request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"JSON decoding failed: {str(e)}"}



def get_last_block() -> dict:
    url = make_api_url(module="proxy", action="eth_blockNumber")
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return clean_last_block(data)
    except requests.exceptions.RequestException as e:
        return {"error": f"HTTP request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"JSON decoding failed: {str(e)}"}
    

    
def get_last_transactions(address: str, start_block: int = 0, end_block: int = 99999999, sort: str = "desc") -> dict:
    url = make_api_url(
        module="account",
        action="txlist",
        address=address,
        startblock=start_block,
        endblock=end_block,
        sort=sort
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return clean_transactions(data)
    except requests.exceptions.RequestException as e:
        return {"error": f"HTTP request failed: {str(e)}"}
    except ValueError as e:
        return {"error": f"JSON decoding failed: {str(e)}"}
