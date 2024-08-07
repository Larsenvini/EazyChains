from requests import get

API_KEY = "62XA11P6M2XFIXWD9SKARQTMFQMKY8FP6K"

def make_api_url(module, action, **kwargs):
    BASE_URL = "https://api.etherscan.io/api"
    BASE_URL += f"?module={module}&action={action}"
    for k, v in kwargs.items():
        BASE_URL += f"&{k}={v}"
    BASE_URL += f"&apikey={API_KEY}"
    return BASE_URL

print(make_api_url("account", "balance", address="0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae", tag="latest"))
