import json
import os
from datetime import datetime  # Импортируем datetime для проверки типов
from decimal import Decimal  # Импортируем Decimal для обработки

import psycopg2  # type: ignore
from dotenv import load_dotenv

from config.config import DATA_DIR

load_dotenv()


def serialize(value):
    """Функция для преобразования значений в JSON-сериализуемый формат."""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")  # Преобразуем datetime в строку
    if isinstance(value, Decimal):
        return float(value)  # Преобразуем Decimal в float
    return value  # Возвращаем значение, если не datetime и не Decimal


def export_tables_to_json(dbname: str) -> None:
    """Загружает фикстуры таблиц из базы данных"""

    # Создание соединения с базой данных
    conn = psycopg2.connect(
        dbname=dbname,
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT"),
    )

    # Получение курсора
    cur = conn.cursor()

    # Получение имен таблиц
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cur.fetchall()

    # Создание директории для JSON-файлов в data/fixtures
    output_dir = os.path.join(DATA_DIR, "fixtures")  # Конструируем путь
    os.makedirs(output_dir, exist_ok=True)  # Создает папку, если не существует

    # Получение данных для каждой таблицы и запись в файлы JSON
    for table in tables:
        table_name = table[0]

        # Получаем данные из таблицы
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()

        # Получаем имена колонок
        colnames = [desc[0] for desc in cur.description]

        # Создание списка словарей для фикстур
        fixtures = []
        for row in rows:
            fixture = {col: serialize(value) for col, value in zip(colnames, row)}
            # Исключаем поле password, если оно есть
            fixture.pop("password", None)  # Удаляет поле password, если оно существует
            fixtures.append(fixture)

        # Сохранение в JSON-файл
        with open(os.path.join(output_dir, f"{table_name}.json"), "w", encoding="utf-8") as json_file:
            json.dump(fixtures, json_file, ensure_ascii=False, indent=4)

    # Закрытие курсора и соединения
    cur.close()
    conn.close()

    print("Фикстуры успешно сохранены в папку 'config/data/fixtures'.")


if __name__ == "__main__":
    export_tables_to_json("learning_system")
