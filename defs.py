from requests import get

API_KEY = "62XA11P6M2XFIXWD9SKARQTMFQMKY8FP6K"

def make_api_url(**kwargs):
    BASE_URL = "https://api.etherscan.io/api"
    BASE_URL += "?module=account&action=balance"
    for item in kwargs:
        BASE_URL += f"&{item}={kwargs[item]}"
    BASE_URL += f"&apikey={API_KEY}"
    return BASE_URL

make_api_url(address="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae", tag="latest")
