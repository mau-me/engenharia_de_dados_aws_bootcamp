# Imports

import os
import logging
import requests
from abc import ABC, abstractmethod
import datetime
from typing import List
import json
from schedule import repeat, every, run_pending
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Exceptions


class DataTypeNotSupportedException(Exception):
    def __init__(self, data) -> None:
        self.data = data
        self.message = f'Data type {type(data)} is not supported for ingestion'
        super().__init__(self.message)

# Writers


class DataWriter():
    def __init__(self, coin: str, api: str) -> None:
        self.coin = coin
        self.api = api
        self.filename = f'{self.api}/{self.coin}/{datetime.datetime.now()}.json'

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        with open(self.filename, 'a') as f:
            f.write(row)

    def write(self, data):
        if isinstance(data, dict):
            self._write_row(json.dumps(data) + '\n')
        elif isinstance(data, List):
            for element in data:
                self.write(element)
        else:
            raise DataTypeNotSupportedException(data)

# APIs


class MercadoBitcoinApi(ABC):
    def __init__(self, coin: str):
        self.coin = coin
        self.base = 'https://api.mercadobitcoin.net/api/v4'

    @abstractmethod
    def _get_endpoint(self) -> str:
        pass

    def get_data(self, **kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f'Getting data from endpoint: {endpoint}')
        response = requests.get(endpoint)
        return response.json()


class TickersApi(MercadoBitcoinApi):
    type = 'tickers'

    def _get_endpoint(self) -> str:
        return f'{self.base}/{self.type}/?symbols={self.coin}'


class TradesApi(MercadoBitcoinApi):
    type = 'trades'

    def _get_unix_epoch(self, date: datetime) -> int:
        return int(date.timestamp())

    def _get_endpoint(self, date_from: datetime.datetime = None, date_to: datetime.date = None) -> str:

        if date_from and not date_to:
            unix_date_from = self._get_unix_epoch(date_from)
            endpoint = f'{self.base}/{self.coin}/{self.type}/?from={unix_date_from}'
        elif date_from and date_to:
            if (date_from > date_to):
                raise RuntimeError("date_from cannot be greater than date_to")

            unix_date_from = self._get_unix_epoch(date_from)
            unix_date_to = self._get_unix_epoch(date_to)
            endpoint = f'{self.base}/{self.coin}/{self.type}/?from={unix_date_from},to={unix_date_to}'
        else:
            endpoint = f'{self.base}/{self.coin}/{self.type}'

        return endpoint

# Ingestors


class DataIngestor(ABC):
    def __init__(self, writer: DataWriter, coins: List[str], default_start_date: datetime.datetime = None) -> None:
        self.writer = writer
        self.coins = coins
        self.default_start_date = default_start_date
        self._checkpoint = self._load_checkpoint()

    @property
    def _checkpoint_filename(self):
        return f'{self.__class__.__name__}.checkpoint'

    def _write_checkpoint(self):
        with open(self._checkpoint_filename, 'w') as f:
            f.write(f'{self._checkpoint}')

    def _load_checkpoint(self):
        try:
            with open(self._checkpoint_filename, 'r') as f:
                return datetime.datetime.strptime(f.read(), '%Y-%n-%d').date()
        except:
            return self.default_start_date

    def _get_checkpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    def _update_checkpoint(self, value):
        self._checkpoint = value
        self._write_checkpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass


class TickersIngestor(DataIngestor):
    def ingest(self) -> None:
        for coin in self.coins:
            api = TickersApi(coin)
            data = api.get_data()
            self.writer(coin=coin, api=api.type).write(data)


class TradesIngestor(DataIngestor):
    def ingest(self) -> None:
        date = self._get_checkpoint()
        if date < datetime.datetime.today():
            for coin in self.coins:
                api = TradesApi(coin)
                data = api.get_data()
                self.writer(coin=coin, api=api.type).write(data)
            self._update_checkpoint(
                date + datetime.timedelta(days=1))


if __name__ == '__main__':

    ingestorTickers = TickersIngestor(
        writer=DataWriter, coins=['BTC-BRL', 'ETH-BRL'])
    ingestorTickers.ingest()

    ingestorTrades = TradesIngestor(writer=DataWriter, coins=[
                                    'BTC-BRL', 'ETH-BRL'], default_start_date=datetime.datetime(2024, 3, 4))
    ingestorTrades.ingest()

    @repeat(every(1).seconds)
    def job():
        ingestorTrades.ingest()

    while True:
        run_pending()
        time.sleep(0.5)
