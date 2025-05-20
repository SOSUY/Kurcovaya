from unittest.mock import mock_open, patch
from src.utils import read_json_file

# Первый тест: проверка чтения правильного JSON-файла
@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data="""[
        {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    ]""",
)
def test_valid_read_json_file(mock_file):
    """Тест проверки корректного JSON-файла."""
    path = "valid_user_settings.json"
    result = read_json_file(path)
    expected_output = [
        {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]}
    ]
    assert result == expected_output, f"Результат отличается от ожидаемого ({expected_output})"


# Второй тест: обработка ситуации, когда JSON-данные представляют собой объект, а не список
@patch("builtins.open", new_callable=mock_open, read_data='{"key": "value"}')
def test_invalid_json_format(mock_file):
    """Тест на обработку неправильного формата данных (JSON-объект)."""
    path = "invalid_user_settings.json"
    result = read_json_file(path)
    assert result == [], f"При неправильном формате данных ожидается пустой список, а получилось {result}"


# Третий тест: обработка отсутствующего файла
@patch("builtins.open", side_effect=FileNotFoundError)
def test_missing_file(mock_file):
    """Тест на обработку случая отсутствия файла."""
    path = "nonexistent_file.json"
    result = read_json_file(path)
    assert result == [], f"Пустой список ожидается при отсутствии файла, а получился {result}"
