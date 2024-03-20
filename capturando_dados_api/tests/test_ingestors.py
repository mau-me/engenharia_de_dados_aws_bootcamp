import datetime
from unittest.mock import mock_open, patch
import pytest

from mercado_bitcoin.ingestor import DataIngestor, DataWriter


@pytest.fixture
@patch('mercado_bitcoin.ingestor.DataIngestor.__abstractmethods__', set())
def data_ingestor_fixture():
    return DataIngestor(writer=DataWriter, coins=[
        'TESTE01', 'TESTE02'], default_start_date=datetime.datetime(2024, 3, 17))


@patch('mercado_bitcoin.ingestor.DataIngestor.__abstractmethods__', set())
class TestIngerstors:

    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename

        expected = 'DataIngestor.checkpoint'
        assert actual == expected

    def test_load_checkpoint_existing(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()

        expected = datetime.datetime(2024, 3, 17)
        assert actual == expected

    @patch('builtins.open', new_callable=mock_open, read_data='2021-06-25')
    def test_load_checkpoint_nonexistent(self, mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()

        expected = datetime.datetime(2024, 3, 17)
        assert actual == expected

    @patch('mercado_bitcoin.ingestor.DataIngestor._write_checkpoint', return_value=None)
    def test_update_checkpoint_update(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.datetime(2024, 3, 17))

        actual = data_ingestor._checkpoint

        expected = datetime.datetime(2024, 3, 17)
        assert actual == expected

    @patch('mercado_bitcoin.ingestor.DataIngestor._write_checkpoint', return_value=None)
    def test_update_checkpoint_written(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.datetime(2024, 3, 17))

        mock.assert_called_once()
