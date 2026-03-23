from config import FIELD_MAPPING

# Список полей, которые отслеживаются для обновления
TRACK_FIELDS = ["category", "component", "jira", "jira_status", "updated"]


# Превращаем внутреннее имя FIELD_MAPPING в название колонки в таблице
def field_name(field):
    reverse_map = {v: k for k, v in FIELD_MAPPING.items()}
    return reverse_map.get(field, field)

def normalize(val):
    if val is None:
        return ""
    return str(val).strip()

# Определяем изменения, которые будут внесены в таблицу
def detect_changes(csv_tickets, active):
    # Набор тикетов на добавление; обновление; перемещение на лист Inactive; перемещение с листа Inactive на лист Active
    add = []
    update = {}

    for ticket_id, t in csv_tickets.items():
        changes = {}

        # Тикет есть на листе Active
        if ticket_id in active:
            sheet_data = active[ticket_id]["data"]

            # Проверяем на наличие изменений
            for field in TRACK_FIELDS:
                sheet_val = normalize(sheet_data.get(field_name(field), ""))
                csv_val = normalize(t.get(field, ""))

                if sheet_val != csv_val:
                    changes[field_name(field)] = (sheet_val, csv_val)

            if changes:
                update[ticket_id] = changes

        # Тикета нет на листе
        else:
            add.append(ticket_id)

    return add, update


# Выводим список потенциальных изменений в Гугл-доку
def print_plan(add, update):
    print()

    if add:
        print("Новые тикеты:")
        for tid in add:
            print(" +", tid)

    if update:
        print("\nОбновления:")
        for tid, fields in update.items():
            print(f"\n~ {tid}")
            for f, (old, new) in fields.items():
                print(f"{f}: {old} ---> {new}")

    print()