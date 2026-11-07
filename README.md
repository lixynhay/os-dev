# oc-dev — MCP-сервер для разработки под OpenComputers / OpenPeripheral

Офлайн-справочник по API модов + линтер типовых ошибок. Контекстная экономия:
вместо простыни скилла агент дергает `get_component("gpu")` и получает 2 КБ.

## Установка

```bash
pip install fastmcp
```

## Подключение

**Claude Desktop / Cursor** (`claude_desktop_config.json` / `mcp.json`):

```json
{
  "mcpServers": {
    "oc-dev": {
      "command": "python",
      "args": ["/abs/path/to/oc-mcp/server.py"]
    }
  }
}
```

**Claude Code**:

```bash
claude mcp add oc-dev python /abs/path/to/oc-mcp/server.py
```

## Инструменты

| Инструмент | Что делает |
|---|---|
| `list_api()` | Список всего справочника |
| `get_component(name)` | API компонента (gpu, screen, modem, redstone, me_interface, pim...) |
| `get_event(name)` | Сигнатура события + пример (touch, scroll, key_down, modem_message...) |
| `get_library(name)` | Библиотека OpenOS (component, event, computer, serialization...) |
| `search(query)` | Полнотекстовый поиск по базе |
| `lint_code(code)` | Проверка Lua на типовые грабли OC |

## Структура

```
oc-mcp/
  server.py            # MCP-сервер (FastMCP, stdio)
  data/
    components/*.md    # API компонентов
    events/*.md        # Сигнатуры событий
    libraries/*.md     # Библиотеки OpenOS
    pitfalls.md        # Сводка граблей
    patterns.md        # Типовые паттерны кода
```

## Дополнение базы

Файлы в `data/` — обычный markdown, один файл = одна сущность. Добавил файл —
сразу доступен через инструменты, перезапуск не нужен.

⚠️ API периферии зависит от версий OC/OpenPeripheral/MC. Точный состав методов
любого компонента в игре: `for k,v in pairs(component.methods(address)) do print(k) end`.
