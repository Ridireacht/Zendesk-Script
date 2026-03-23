from csv_sheet_updater import update_sheet_with_tickets
from utils import find_file, load_sheet
from csv_loader import parse_tickets_from_file
from google_client import init_google
from diff_engine import detect_changes, print_plan
from config import CURRENT_SHEET


def main():
    # Получаем вспомогательные файлы для работы скрипта (свежую выгрузку из Zendesk и Google API ключ)
    csv_file = find_file("csv")
    json_key = find_file("json")
    print("CSV:", csv_file)

    # Получаем отформатированный список тикетов из выгрузки Zendesk
    tickets = parse_tickets_from_file(csv_file)

    # Получаем себе Гугл-доку, с которой работаем, а также её листы
    spreadsheet = init_google(json_key)
    current_sheet = spreadsheet.worksheet(CURRENT_SHEET)

    current = load_sheet(current_sheet)

    # Обрабатываем тикеты из выгрузки на предмет потенциальных изменений в Гугл-доку
    add, update = detect_changes(
        tickets, current
    )

    # И выводим, что предполагается изменить
    print_plan(add, update)

    # Изменений нет — ничего не трогаем
    if not any([add, update]):
        print("Изменений нет")
        return

    # Изменения есть — получаем у пользователя подтверждение на изменение
    ans = input("Применить изменения? (y/n): ")
    if ans.lower() != "y":
        print("Отменено")
        return

    # Обновляем Гугл-доку данными
    update_sheet_with_tickets(current_sheet, add, update, tickets)

    print("Готово")


if __name__ == "__main__":
    main()