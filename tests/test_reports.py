import json
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Тестирование декорированной функции расчета расходов по категориям
def test_calculate_expenses_by_category():
    # Данные для тестирования
    lst_for_tests_csv_xlsx = [
        {"Дата операции": "31.10.2021", "Категория": "Переводы", "Сумма операции": -20000},
        {"Дата операции": "01.11.2021", "Категория": "Кафе", "Сумма операции": -5000},
        {"Дата операции": "01.07.2021", "Категория": "Перелеты", "Сумма операции": -15000}
    ]

    # Создание датафрейма для теста
    df_test = pd.DataFrame(lst_for_tests_csv_xlsx)

    # Ожидаемый результат
    expected_data = [{"Сумма операции": -20000.0}]

    # Запускаем тестируемую функцию с использованием декоратора
    from src.reports import calculate_expenses_by_category
    result_df = calculate_expenses_by_category(df_test, "Переводы", "31.10.2021")

    # Проверяем правильность результата
    actual_data = result_df.to_dict('records')
    assert actual_data == expected_data, f"Ожидалось {expected_data}, получено {actual_data}"

    # Проверяем наличие сохраненного файла JSON
    try:
        with open("logs/category_expenses.json", 'r', encoding='utf-8') as file:
            saved_data = json.load(file)

        # Убеждаемся, что данные совпадают с ожидаемым результатом
        assert saved_data == expected_data, f"Сохранённые данные отличаются от ожидаемых."
    except FileNotFoundError:
        raise AssertionError(f"Файл logs/category_expenses.json не найден!")
