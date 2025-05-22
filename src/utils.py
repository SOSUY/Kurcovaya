import json
from unittest.mock import mock_open, patch
from src.utils import read_json_file


# Первый тест: проверка чтения правильного JSON-файла
@patch('builtins.open', new_callable=mock_open, read_data='[{"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}]')
def test_valid_read_json_file(mock_file):
    """
    Тест проверяет успешное чтение валидного JSON-файла с правильным форматом данных — списком объектов.
    """
    path = 'valid_user_settings.json'
    result = read_json_file(path)
    expected_output = [{
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    }]
    assert result == expected_output, f'Результат отличается от ожидаемого ({expected_output})'


# Второй тест: обработка ситуации, когда JSON-данные представляют собой объект, а не список
@patch('builtins.open', new_callable=mock_open, read_data='{"key": "value"}')
def test_invalid_json_format(mock_file):
    """
    Тест проверяет поведение при некорректном формате данных — JSON-объекте вместо списка.
    Ожидается возвращение пустого списка.
    """
    path = 'invalid_user_settings.json'
    result = read_json_file(path)
    assert result == [], f'Ожидался пустой список при неверном формате данных, получил {result}'


# Третий тест: обработка отсутствующего файла
@patch('builtins.open', side_effect=FileNotFoundError)
def test_missing_file(mock_file):
    """
    Тест проверяет ситуацию, когда файл отсутствует.
    Функция должна вернуть пустой список.
    """
    path = 'nonexistent_file.json'
    result = read_json_file(path)
    assert result == [], f'Ожидалось получение пустого списка при отсутствии файла, получил {result}'
