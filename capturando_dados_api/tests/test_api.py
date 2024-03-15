import datetime
import pytest
from ingestao import TickersApi, TradesApi


class TestTickersApi:
    @pytest.mark.parametrize(
        'coin, expected',
        [('BTC-BRL', 'https://api.mercadobitcoin.net/api/v4/tickers/?symbols=BTC-BRL'),
         ('ETH-BRL', 'https://api.mercadobitcoin.net/api/v4/tickers/?symbols=ETH-BRL')]
    )
    def test_get_endpoint_tickers(self, coin, expected):
        actual = TickersApi(coin=coin)._get_endpoint()

        assert actual == expected


class TestTradesApi:
    @pytest.mark.parametrize(
        'coin, date_from, date_to, expected',
        [('BTC-BRL', None, None, 'https://api.mercadobitcoin.net/api/v4/BTC-BRL/trades')]
    )
    def test_get_endpoint_trades(self, coin, date_from, date_to, expected):
        actual = TradesApi(
            'BTC-BRL')._get_endpoint(date_from=date_from, date_to=date_to)

        assert actual == expected
