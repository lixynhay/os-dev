# SKILL.md — OpenComputers / OpenPeripheral

Разработка Lua-кода под Minecraft-моды OpenComputers + OpenPeripheral.
Полный справочник лежит в MCP-сервере `oc-dev` — **не угадывай API из памяти**,
комплектующие сильно зависят от версий модов.

## Порядок работы
1. Перед написанием кода: `search()` или `get_component()` / `get_event()` / `get_library()`.
2. После написания кода — ОБЯЗАТЕЛЬНО `lint_code()`.
3. Сомневаешься в составе методов периферии — в справке написано, как проверить
   через `component.methods()` прямо в игре.

## Железные правила (не нарушать без проверки)
- Кириллица: только `unicode.len/sub/wlen`, оператор `#` считает байты.
- `touch`: `local _, _, x, y = event.pull("touch")` — первый аргумент адрес экрана.
- OpenOS ≠ ComputerCraft: нет `os.pullEvent`, `term.setTextColor`, `term.setCursorPos`.
- В циклах лови `"interrupted"` (Ctrl+C), иначе скрипт не остановить.
- Периферия OpenPeripheral (pim и т.п.) — только через `component.methods(address)`.
