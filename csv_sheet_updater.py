from utils import get_sheet_headers, make_row, load_sheet


def update_sheet_with_tickets(current_sheet, add, update, delete, tickets):
    # Заголовки листов
    current_sheet_headers = get_sheet_headers(current_sheet)

    loaded_current_sheet = load_sheet(current_sheet)


    # --- 1. Обновления в Active ---
    updates = []
    for ticket_id in update:
        row_index = loaded_current_sheet[ticket_id]["row"]
        row_values = make_row(tickets[ticket_id], current_sheet_headers)
        updates.append({
            "range": f"A{row_index}:{chr(64 + len(row_values))}{row_index}",
            "values": [row_values]
        })

    if updates:
        current_sheet.batch_update(updates, value_input_option="USER_ENTERED")

    # --- 2. Добавление новых тикетов в Active ---
    new_rows = [make_row(tickets[tid], current_sheet_headers) for tid in add]
    if new_rows:
        current_sheet.append_rows(new_rows, value_input_option="USER_ENTERED")


    if delete:
        # удаляем все строки в Active в обратном порядке
        for tid in sorted(delete, key=lambda x: loaded_current_sheet[x]["row"], reverse=True):
            current_sheet.delete_rows(loaded_current_sheet[tid]["row"])