import glob

from config import FIELD_MAPPING


# Ищем файл с заданным расширением. Предполагается, что в директории будет всего один такой файл (CSV для выгрузки из
# Zendesk, JSON для Google API ключа)
def find_file(ext):
    files = glob.glob(f"*.{ext}")

    if len(files) != 1:
        raise Exception(f"В директории должен быть ровно один .{ext} файл")

    return files[0]

# Получаем лист из Гугл-документа
def load_sheet(sheet):
    rows = sheet.get_all_records()
    data = {}
    for i, row in enumerate(rows):
        ticket_id = str(row["ID"])
        data[ticket_id] = {"row": i + 2, "data": row}
    return data

def make_row(t, header_map):
    """Возвращает список значений только для колонок, которые есть в таблице"""
    row = []

    for col_name in header_map:
        if col_name == "Ссылка":
            row.append(force_text(t["link"]))

        elif col_name in FIELD_MAPPING:
            internal = FIELD_MAPPING[col_name]
            value = t.get(internal, "")
            row.append(force_text(value))

        else:
            # пользовательские колонки НЕ трогаем
            row.append(None)

    return row

def force_text(val):
    if val is None:
        return ""
    return str(val)

def get_sheet_headers(sheet):
    return sheet.row_values(1)