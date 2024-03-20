from mercado_bitcoin.ingestor import TickersApi


class TestTickersApi:
    def test_get_data(self):
        actual = TickersApi('BTC-BRL').get_data()[0].get('pair')
        expected = 'BTC-BRL'
        assert actual == expected
