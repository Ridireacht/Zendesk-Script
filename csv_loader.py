import csv
from datetime import datetime
from config import FIELD_MAPPING, ZENDESK_URL

# Чистим значение от мусора
def clean_value(value: str) -> str:
    if not value:
        return ""

    value = value.strip()

    if value in ("'-", "-", "''", '"-"'):
        return ""

    return value

# Приводим дату к единому формату
def normalize_date(date_str: str) -> str:
    if not date_str or date_str.strip() in ("'-", "-"):
        return ""

    date_str = date_str.strip()

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%H:%M %d-%m-%Y")
        except ValueError:
            continue

# Обрабатываем CSV-выгрузку, извлекаем тикеты с нужными полями и добавляем к ним ссылку, собираем всё это в словарь
def parse_tickets_from_file(file_path: str) -> dict:
    result = {}

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            ticket = {}

            for original_field, new_field in FIELD_MAPPING.items():
                value = clean_value(row.get(original_field))

                if new_field in ("requested", "updated"):
                    value = normalize_date(value)

                ticket[new_field] = value

            ticket["link"] = ZENDESK_URL + ticket["id"]
            result[ticket["id"]] = ticket

    return result