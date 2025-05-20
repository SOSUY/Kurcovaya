import pandas as pd
import numpy as np
from typing import List, Dict, Any

from src.utils import df_to_transactions


def invest_roundup(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает разницу между фактическими тратами и ближайшими большими значениями,
    округленными до указанного предела (например, 10, 50 или 100 рублей), для зачисления на Инвесткопилку.

    Параметры:
    month (str): Месяц и год формата "%Y-%m", начиная с которого учитываются траты.
    transactions (List[Dict[str, Any]]): Список транзакций.
    limit (int): Округление (10, 50 или 100 руб.).

    Возвращает:
    float: Сумма разницы между фактическими затратами и округленной суммой.
    """
    # Проверка валидных значений лимитов
    if limit not in [10, 50, 100]:
        raise ValueError("Неверный предел округления! Используйте значения 10, 50 или 100.")

    # Конвертируем транзакции в датафрейм
    df = df_to_transactions(transactions)

    # Обрабатываем даты и фильтры
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    mask = df["Дата операции"] < pd.to_datetime(month, format="%Y-%m")

    # Берём только отрицательные транзакции (расходы)
    df_filtered = df[mask]
    amounts = df_filtered["Сумма операции"].abs()

    # Высчитываем округленную сумму вверх и находим разницу
    rounded_amounts = np.ceil(amounts / limit) * limit
    diff = rounded_amounts - amounts

    # Суммируем разницу и возвращаем общий вклад в инвесткопилку
    total_diff = diff.sum()
    return total_diff
