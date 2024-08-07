from defs import get_balance_by_address, get_last_block

def main():
    address = "0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"  # Exemplo de endereço Ethereum

    # obter saldo por endereço
    balance_data = get_balance_by_address(address)
    print("Dados do Saldo por Endereço:")
    print(balance_data)
    print("Saldo (em Wei):", balance_data.get("result", "Não disponível"))
    print("\nSeparação\n")

    # obter último bloco
    last_block_data = get_last_block()
    print("Dados do Último Bloco:")
    print(last_block_data)
    last_block_number = int(last_block_data.get("result", "0"), 16)
    print("Número do Último Bloco:", last_block_number)

if __name__ == "__main__":
    main()
