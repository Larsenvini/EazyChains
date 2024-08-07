from requests import get

API_KEY = "62XA11P6M2XFIXWD9SKARQTMFQMKY8FP6K"
BASE_URL = "https://api.etherscan.io/api"

def make_api_url(module, action, **kwargs):
    url = BASE_URL + f"?module={module}&action={action}&apikey={API_KEY}"
    for k, v in kwargs.items():
        url += f"&{k}={v}"
    return url

def balance_byAddress(wallet):
    data = get(make_api_url("account", "balance", address=wallet, tag="latest"))
    data = data.json()
    return data

print(balance_byAddress("0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"))
