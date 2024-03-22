from datetime import datetime
import requests
import json


def cotacao(valor: float, moeda: str = 'USD-BRL'):
    url = f'https://economia.awesomeapi.com.br/last/{moeda}'

    req = requests.get(url)

    if req:
        content = json.loads(req.text)

        moedas = moeda.replace('-', '')

        cotacao = float(content[moedas]['bid'])
        return f'A cotação de {valor} {moeda[:3]} é: {round(cotacao * valor, 4)} {moeda[-3:]} - Cotação: {cotacao}'
    else:
        return 'Requisição falhou'


with open('cambio.csv', 'a') as f:
    f.write(
        f'{datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")};{cotacao(5)}\n')

# cotacao(10, 'USD-BRL')
# cotacao(10, 'USD-BRLT')
# cotacao(50, 'BRL-USD')
