from api_calls import *

def view_balance():
    address = input("Digite o endereço Ethereum: ")
    balance_data = get_balance_by_address(address)
    if "error" not in balance_data:
        print(f"Saldo para {address}:")
        print(f"  - Wei: {balance_data['balance_wei']}")
        print(f"  - Ether: {balance_data['balance_ether']:.18f}")
    else:
        print(f"Falha ao recuperar o saldo: {balance_data['error']}")

def view_last_block():
    block_data = get_last_block()
    if "error" not in block_data:
        print(f"Número do Último Bloco: {block_data['block_number']}")
    else:
        print(f"Falha ao recuperar o último bloco: {block_data['error']}")

def view_last_transactions():
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

def menu():
    while True:
        print("\n--- Menu Interativo ---")
        print("1. Verificar saldo de um endereço Ethereum")
        print("2. Obter o último bloco")
        print("3. Obter últimas transações de um endereço Ethereum")
        print("4. Sair")

        funcs = {"1": view_balance, "2": view_last_block, "3": view_last_transactions}
        escolha = input("Escolha uma opção (1-4): ")

        if escolha == "4":
            print("Saindo do programa...")
            break
        elif escolha in funcs:
            funcs.get(escolha)()
        else:
            print("Não entendi, tente novamente.")