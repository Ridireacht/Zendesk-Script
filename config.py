# Формат URL для тикетов в Зендеске (без учёта /ID)
ZENDESK_URL = "https://virtual-ats.zendesk.com/agent/tickets/"

# Ссылка на Гугл-доку, где хранятся данные по тикетам на удержании
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1vGWl0ASmUsYroAQqOjl23PKc6hWPhD3X0ByZzU5szoY/edit"

# Название листов в Гугл-доке
CURRENT_SHEET = "Текущие тикеты"

# Маппинг полей (столбцов) между Гугл-докой и местной структурой для хранения тикетов
FIELD_MAPPING = {
    "ID": "id",
    "Организация": "organization",
    "Домен клиента": "domain",
    "Категория обращения": "category",
    "Компонент": "component",
    "JIRA issue ID": "jira",
    "Состояние задачи Jira": "jira_status",
    "Запрошен": "requested",
    "Обновлен": "updated",
}