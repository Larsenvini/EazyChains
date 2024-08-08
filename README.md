API_KEY = "62XA11P6M2XFIXWD9SKARQTMFQMKY8FP6K"

# 2 FUNÇÕES NOVAS PARA VCS TENTAREM FAZER:

1 - Pegar as últimas transações de um endereço

2 - Pelo CLI, criar uma interação/inputs (menu) pelo terminal p deixar o APP meio funcional

3 - (Opcional) Com as txhash, dissecar e ver se existe alguma forma de retornar oque a transação foi

# Imports

from requests import get

	- get é uma função que recebe como argumento uma url. Responsável por realizar a chamada de api ou "request"
	- .json() é um método p transformar essa informação em formato json (pré existente em python nativo)
 
# Variables

BASE_URL = "https://api.etherscan.io/api"

	- get é uma função que recebe como argumento uma url. Responsável por realizar a chamada de api ou "request"
	- .json() é um método p transformar essa informação em formato json (pré existente em python nativo)

# Functions

make_api_url()

	- Uma função que recebe os parâmetros p/ chamada de api e retorna a url específica p cada chamada
	Exemplo, criar uma url específica para uma chamada de api que precise de um endereço (address) e uma tag (latest) como argumentos.

	make_api_url(address="0xasidj182dias...",tag=latest) -> BASE_URL + url
 	

get_balance_byAddress()

	- Função responsável por retornar o saldo de uma carteira específica


get_last_block()

	- Retorna o último bloco lançado na blockchain

=======
# EazyChains - Projeto da turma presencial

# Lead: Rodrigo Paiva

# Members: Larsen, Pastore, Boeing & Fernando

