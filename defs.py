import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BASE_URL')  

if not BASE_URL:
    raise ValueError("A URL base não foi encontrada. Verifique o arquivo .env.")

def make_api_url(module: str, action: str, **params) -> str:
    """
    Constrói a URL da API para fazer solicitações à API do Etherscan.

    :param module: O módulo da API a ser chamado (por exemplo, "account").
    :param action: A ação específica dentro do módulo (por exemplo, "balance").
    :param params: Parâmetros adicionais a serem passados para a chamada da API.
    :return: A URL completa para a chamada da API.
    """
    api_key = os.getenv('ETHERSCAN_API_KEY')
    if not api_key:
        raise ValueError("A chave de API não foi encontrada. Verifique o arquivo .env.")

    params_list = [f"{key}={value}" for key, value in params.items()]
    params_str = "&".join(params_list)
    url = f"{BASE_URL}?module={module}&action={action}&{params_str}&apikey={api_key}"
    return url

def clean_account_balance(data: dict) -> dict:
    """
    Limpa e analisa os dados de saldo da conta retornados pela API do Etherscan.

    :param data: Os dados JSON contendo o saldo da conta.
    :return: Um dicionário contendo o status, a mensagem e o saldo em Ether.
    """
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
    """
    Limpa e analisa os dados do último bloco retornados pela API do Etherscan.

    :param data: Os dados JSON contendo o número do último bloco.
    :return: Um dicionário contendo o número do bloco como um inteiro.
    """
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
    """
    Limpa e analisa os dados de transações retornados pela API do Etherscan.

    :param data: Os dados JSON contendo as transações.
    :return: Um dicionário contendo as transações ou um erro, se ocorrer.
    """
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

def get_balance_by_address(address: str) -> dict:
    """
    Obtém o saldo de um endereço Ethereum usando a API do Etherscan.

    :param address: O endereço Ethereum para o qual o saldo deve ser obtido.
    :return: Um dicionário contendo o saldo em Ether ou um erro, se ocorrer.
    """
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
    """
    Obtém o último número de bloco usando a API do Etherscan.

    :return: Um dicionário contendo o número do último bloco ou um erro, se ocorrer.
    """
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
    """
    Obtém as últimas transações de um endereço Ethereum usando a API do Etherscan.

    :param address: O endereço Ethereum para o qual as transações devem ser obtidas.
    :param start_block: O bloco inicial para buscar transações (padrão é 0).
    :param end_block: O bloco final para buscar transações (padrão é 99999999).
    :param sort: A ordem de classificação das transações ('asc' ou 'desc', padrão é 'desc').
    :return: Um dicionário contendo as transações ou um erro, se ocorrer.
    """
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

def menu_interativo():
    """
    Menu interativo para interação com o aplicativo via terminal.
    """
    while True:
        print("\n--- Menu Interativo ---")
        print("1. Verificar saldo de um endereço Ethereum")
        print("2. Obter o último bloco")
        print("3. Obter últimas transações de um endereço Ethereum")
        print("4. Sair")

        escolha = input("Escolha uma opção (1-4): ")

        if escolha == "1":
            address = input("Digite o endereço Ethereum: ")
            balance_data = get_balance_by_address(address)
            if "error" not in balance_data:
                print(f"Saldo para {address}:")
                print(f"  - Wei: {balance_data['balance_wei']}")
                print(f"  - Ether: {balance_data['balance_ether']:.18f}")
            else:
                print(f"Falha ao recuperar o saldo: {balance_data['error']}")

        elif escolha == "2":
            block_data = get_last_block()
            if "error" not in block_data:
                print(f"Número do Último Bloco: {block_data['block_number']}")
            else:
                print(f"Falha ao recuperar o último bloco: {block_data['error']}")

        elif escolha == "3":
            address = input("Digite o endereço Ethereum: ")
            num_transacoes = int(input("Digite o número de transações a serem retornadas: "))
            transactions_data = get_last_transactions(address)
            if "error" not in transactions_data:
                print(f"Últimas {num_transacoes} transações para {address}:")
                transactions = transactions_data['transactions'][:num_transacoes]
                for i, tx in enumerate(transactions, start=1):
                    print(f"\nTransação {i}:")
                    print(f"  Hash: {tx['hash']}")
                    print(f"  De: {tx['from']}")
                    print(f"  Para: {tx['to']}")
                    print(f"  Valor: {int(tx['value']) / 10**18} Ether")
                    print(f"  Bloco: {tx['blockNumber']}")
            else:
                print(f"Falha ao recuperar as transações: {transactions_data['error']}")

        elif escolha == "4":
            print("Saindo do programa...")
            break

        else:
            print("Opção inválida. Tente novamente.")
