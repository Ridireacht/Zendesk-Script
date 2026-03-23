from utils import get_sheet_headers, make_row, load_sheet


def update_sheet_with_tickets(active_sheet, inactive_sheet, add, update, deactivate, reactivate, tickets):
    # Заголовки листов
    active_headers = get_sheet_headers(active_sheet)
    inactive_headers = get_sheet_headers(inactive_sheet)

    active = load_sheet(active_sheet)
    inactive = load_sheet(inactive_sheet)


    # --- 1. Обновления в Active ---
    updates = []
    for ticket_id in update:
        row_index = active[ticket_id]["row"]
        row_values = make_row(tickets[ticket_id], active_headers)
        updates.append({
            "range": f"A{row_index}:{chr(64 + len(row_values))}{row_index}",
            "values": [row_values]
        })

    if updates:
        active_sheet.batch_update(updates, value_input_option="USER_ENTERED")

    # --- 2. Добавление новых тикетов в Active ---
    new_rows = [make_row(tickets[tid], active_headers) for tid in add]
    if new_rows:
        active_sheet.append_rows(new_rows, value_input_option="USER_ENTERED")

    # --- 3. Batch перемещение Active → Inactive ---
    if deactivate:
        deact_rows = []
        for tid in deactivate:
            r_idx = active[tid]["row"]
            row_vals = active_sheet.row_values(r_idx)
            # формируем значения под заголовки Inactive
            row_inactive = [row_vals[active_headers.index(h)] if h in active_headers else "" for h in inactive_headers]
            deact_rows.append(row_inactive)
        if deact_rows:
            inactive_sheet.append_rows(deact_rows, value_input_option="USER_ENTERED")
        # удаляем все строки в Active в обратном порядке
        for tid in sorted(deactivate, key=lambda x: active[x]["row"], reverse=True):
            active_sheet.delete_rows(active[tid]["row"])

    # --- 4. Batch перемещение Inactive → Active ---
    if reactivate:
        react_rows = []
        for tid in reactivate:
            r_idx = inactive[tid]["row"]
            row_vals = inactive_sheet.row_values(r_idx)
            row_active = [row_vals[inactive_headers.index(h)] if h in inactive_headers else "" for h in active_headers]
            react_rows.append(row_active)
        if react_rows:
            active_sheet.append_rows(react_rows, value_input_option="USER_ENTERED")
        # удаляем строки из Inactive
        for tid in sorted(reactivate, key=lambda x: inactive[x]["row"], reverse=True):
            inactive_sheet.delete_rows(inactive[tid]["row"])