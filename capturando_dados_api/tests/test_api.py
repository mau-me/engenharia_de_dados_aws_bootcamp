import datetime
import pytest
from mercado_bitcoin.ingestor import TickersApi, TradesApi


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
        [
            ('BTC-BRL', None, None,
             'https://api.mercadobitcoin.net/api/v4/BTC-BRL/trades'),
            ('BTC-BRL', datetime.datetime(2023, 3, 17), None,
                'https://api.mercadobitcoin.net/api/v4/BTC-BRL/trades/?from=1679022000'),
            ('BTC-BRL', datetime.datetime(2023, 3, 16), datetime.datetime(2023, 3, 17),
                'https://api.mercadobitcoin.net/api/v4/BTC-BRL/trades/?from=1678935600,to=1679022000')
        ]
    )
    def test_get_endpoint_trades(self, coin, date_from, date_to, expected):
        actual = TradesApi(coin)._get_endpoint(
            date_from=date_from, date_to=date_to)

        assert actual == expected

    def test_get_endpoint_trades_datefrom_greater_dateto(self):
        with pytest.raises(RuntimeError):
            TradesApi("TEST")._get_endpoint(
                date_from=datetime.datetime(2023, 3, 17), date_to=datetime.datetime(2023, 3, 16))
