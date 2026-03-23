from csv_sheet_updater import update_sheet_with_tickets
from utils import find_file, load_sheet, get_sheet_headers, make_row
from csv_loader import parse_tickets_from_file
from google_client import init_google
from diff_engine import detect_changes, print_plan
from config import ACTIVE_SHEET, INACTIVE_SHEET


def main():
    # Получаем вспомогательные файлы для работы скрипта (свежую выгрузку из Zendesk и Google API ключ)
    csv_file = find_file("csv")
    json_key = find_file("json")
    print("CSV:", csv_file)

    # Получаем отформатированный список тикетов из выгрузки Zendesk
    tickets = parse_tickets_from_file(csv_file)

    # Получаем себе Гугл-доку, с которой работаем, а также её листы
    spreadsheet = init_google(json_key)
    active_sheet = spreadsheet.worksheet(ACTIVE_SHEET)
    inactive_sheet = spreadsheet.worksheet(INACTIVE_SHEET)

    active = load_sheet(active_sheet)
    inactive = load_sheet(inactive_sheet)

    # Обрабатываем тикеты из выгрузки на предмет потенциальных изменений в Гугл-доку
    add, update, deactivate, reactivate = detect_changes(
        tickets, active, inactive
    )

    # И выводим, что предполагается изменить
    print_plan(add, update, deactivate, reactivate)

    # Изменений нет — ничего не трогаем
    if not any([add, update, deactivate, reactivate]):
        print("Изменений нет")
        return

    # Изменения есть — получаем у пользователя подтверждение на изменение
    ans = input("Применить изменения? (y/n): ")
    if ans.lower() != "y":
        print("Отменено")
        return

    # Обновляем Гугл-доку данными
    update_sheet_with_tickets(active_sheet, inactive_sheet, add, update, deactivate, reactivate, tickets)

    print("Готово")


if __name__ == "__main__":
    main()