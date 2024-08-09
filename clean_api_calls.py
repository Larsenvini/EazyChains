import os
import requests

def clean_account_balance(data: dict) -> dict:
    if data.get("status") != "1":
        return {"error": data.get("message", "Unexpected error.")}

    try:
        wei_balance = int(data["result"])
        ether_balance = wei_balance / 10**18  # Converter Wei para Ether
        return {
            "status": "success",
            "balance_wei": wei_balance,
            "balance_ether": ether_balance
        }
    except (ValueError, KeyError) as e:
        return {"error": f"Failed to parse balance: {str(e)}"}



def clean_last_block(data: dict) -> dict:
    if "result" not in data:
        return {"error": "Unexpected format in block data."}

    try:
        block_number = int(data["result"], 16)  # Converter hexadecimal para int
        return {
            "status": "success",
            "block_number": block_number
        }
    except ValueError as e:
        return {"error": f"Failed to parse block number: {str(e)}"}
    

    
def clean_transactions(data: dict) -> dict:
    if data.get("status") != "1":
        return {"error": data.get("message", "Unexpected error.")}

    try:
        transactions = data["result"]
        return {
            "status": "success",
            "transactions": transactions
        }
    except KeyError as e:
        return {"error": f"Failed to parse transactions: {str(e)}"}