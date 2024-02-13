import requests
import json


def cotacao(valor: float, moeda: str):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'

    req = requests.get(url)

    if req:
        content = json.loads(req.text)

        moedas = moeda.replace('-', '')

        cotacao = float(content[moedas]['bid'])
        print(
            f'A cotação de {valor} {moeda[:3]} é: {round(cotacao * valor, 4)} {moeda[-3:]} - Cotação: {cotacao}')
    else:
        print('Requisição falhou')


cotacao(10, 'USD-BRL')
cotacao(10, 'USD-BRLT')
cotacao(50, 'BRL-USD')
