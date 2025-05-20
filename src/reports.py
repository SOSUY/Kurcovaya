import json
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta


# Декоратор для сохранения данных в JSON
def save_results_to_file(file_name: str):
    """
    Сохраняет результаты выполнения функции в JSON-файл.

    :param file_name: Имя файла для сохранения результатов.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                # Получение результатов основной функции
                result = func(*args, **kwargs)
                # Преобразование результатов в словарь и сохранение в JSON
                with open(file_name, "w", encoding="utf-8") as output_file:
                    json.dump(result.to_dict("records"), output_file, ensure_ascii=False)
                return result
            except FileNotFoundError:
                print("Не удалось сохранить информацию в файл.")

        return wrapper

    return decorator


# Функция для подсчета расходов по конкретной категории
@save_results_to_file("logs/category_expenses.json")
def calculate_expenses_by_category(
        df: pd.DataFrame, category: str, reference_date: Optional[str] = str(datetime.now())
) -> pd.DataFrame:
    """
    Вычисляет суммы расходов по определенной категории за последние три месяца от заданной даты.

    :param df: Исходный датафрейм с операциями.
    :param category: Название категории расходов.
    :param reference_date: Строка с датой, относительно которой считаем последние три месяца.
    :return: Итоговый датафрейм с суммой расходов по заданной категории.
    """
    # Преобразуем строки дат в объекты типа datetime
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    # Создаем условия фильтра: выбираем нужные операции по дате и категории
    conditions = (
            (df["Дата операции"] <= pd.to_datetime(reference_date, dayfirst=True)) &
            (df["Дата операции"] >= (pd.to_datetime(reference_date, dayfirst=True) - relativedelta(months=3))) &
            (df["Категория"].str.upper() == category.upper())
    )

    # Применяем фильтр и группируем по сумме операций
    expenses = df.loc[conditions].groupby(["Категория"], as_index=False)["Сумма операции"].sum()

    # Ренеймим итоговую колонку сумм на имя категории
    final_result = expenses.rename(columns={"Сумма операции": category})

    return final_result
