#!/usr/bin/env python3
"""
oc-dev - MCP-сервер для разработки под OpenComputers / OpenPeripheral.
Справочник по API + статическая проверка Lua-кода на типовые ошибки.
Работает офлайн. Транспорт: stdio (FastMCP).

Запуск:  python server.py
Требует: pip install fastmcp
"""
import os
import re
import difflib
from fastmcp import FastMCP

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

mcp = FastMCP("oc-dev")

ALIASES = {
    "player_on": "player_on_off",
    "player_off": "player_on_off",
}

NEWLINE = chr(10)


def _list_names(subdir):
    path = os.path.join(DATA_DIR, subdir)
    if not os.path.isdir(path):
        return []
    return sorted(f[:-3] for f in os.listdir(path) if f.endswith(".md"))


def _read(subdir, name):
    name = ALIASES.get(name, name)
    path = os.path.join(DATA_DIR, subdir, name + ".md")
    if os.path.isfile(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return None


def _suggest(subdir, name):
    names = _list_names(subdir)
    close = difflib.get_close_matches(name, names, n=3, cutoff=0.4)
    if close:
        return " Не найдено. Возможно, ты имел в виду: " + ", ".join(close) + "?"
    return " Не найдено. Доступные: " + ", ".join(names) + "."


@mcp.tool()
def list_api():
    """Список всего справочника: компоненты, события, библиотеки OpenOS."""
    out = []
    for subdir, title in [("components", "КОМПОНЕНТЫ"),
                          ("events", "СОБЫТИЯ"),
                          ("libraries", "БИБЛИОТЕКИ OPENOS")]:
        names = _list_names(subdir)
        out.append("## " + title + " (" + str(len(names)) + ")" + NEWLINE + ", ".join(names))
    for extra in ("pitfalls.md", "patterns.md"):
        p = os.path.join(DATA_DIR, extra)
        if os.path.isfile(p):
            with open(p, encoding="utf-8") as f:
                first = f.readline().strip("# \n")
            out.append("## ДОПОЛНИТЕЛЬНО" + NEWLINE + "- " + extra[:-3] + ": " + first)
    return (NEWLINE + NEWLINE).join(out)


@mcp.tool()
def get_component(name):
    """Полное API компонента: gpu, screen, modem, redstone, filesystem,
    inventory_controller, me_interface, pim, eeprom и др."""
    name = name.strip().lower()
    doc = _read("components", name)
    if doc is None:
        return "Компонент '" + name + "' не найден." + _suggest("components", name)
    return doc


@mcp.tool()
def get_event(name):
    """Сигнатура и пример обработки события: touch, drag, drop, scroll,
    key_down, key_up, modem_message, player_on/player_off, interrupted."""
    name = name.strip().lower()
    doc = _read("events", name)
    if doc is None:
        return "Событие '" + name + "' не найдено." + _suggest("events", name)
    return doc


@mcp.tool()
def get_library(name):
    """Документация по библиотеке OpenOS: component, event, computer,
    unicode, term, filesystem, serialization, text, keyboard, sides,
    internet, io_os."""
    name = name.strip().lower()
    doc = _read("libraries", name)
    if doc is None:
        return "Библиотека '" + name + "' не найдена." + _suggest("libraries", name)
    return doc


@mcp.tool()
def search(query, max_results=10):
    """Полнотекстовый поиск по всей базе. Ищи по-русски или по-английски:
    scroll, палитра, touch, порт."""
    q = query.strip().lower()
    if not q:
        return "Пустой запрос."
    hits = []
    for base, _, files in os.walk(DATA_DIR):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(base, fn)
            rel = os.path.relpath(path, DATA_DIR)[:-3]
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if q in line.lower():
                        hits.append("- " + rel + ":" + str(i) + ": " + line.strip()[:160])
                        break
    if not hits:
        return "По запросу '" + query + "' ничего не найдено."
    head = "Найдено " + str(min(len(hits), max_results)) + ":"
    return head + NEWLINE + NEWLINE.join(hits[:max_results])


RULES = [
    (re.compile(r"local\s+\w+\s*,\s*\w+\s*=\s*event\.pull\([^)]*touch"),
     "КРИТИЧНО: event.pull(touch) возвращает (event, screenAddress, x, y, button, player). "
     "При такой распаковке x получит адрес экрана, y - координату X. "
     "Правильно: local _, _, x, y = event.pull(touch)"),
    (re.compile(r"os\.pullEvent"),
     "os.pullEvent - это ComputerCraft API. В OpenOS используй event.pull()"),
    (re.compile(r"term\.(setTextColor|getCursorPos|setCursorPos|isColor|setBackgroundColor)"),
     "Это ComputerCraft API. В OpenOS: gpu.setForeground()/gpu.setBackground(), term.setCursor()/term.getCursor()"),
    (re.compile(r"event\.pull\([^)]*(touch|player_on|player_off)"),
     "pull без таймаута: для разового срабатывания ок, но в цикле ставь таймаут event.pull(0.05), "
     "иначе обработаешь ровно одно событие и зависнешь"),
    (re.compile(r"while\s+true"),
     "Цикл while true: проверь, что внутри ловится событие 'interrupted' (Ctrl+C), иначе скрипт не остановить"),
]

CYRILLIC = re.compile(r"[а-яёА-ЯЁ]")
BYTE_LEN = re.compile(r"#\s*[A-Za-z_]\w*")


@mcp.tool()
def lint_code(code):
    """Статическая проверка Lua-кода на типовые ошибки OpenComputers.
    Прогоняй ВСЕГДА перед тем как отдать код пользователю."""
    findings = []
    for rx, msg in RULES:
        for m in rx.finditer(code):
            line = code[:m.start()].count(NEWLINE) + 1
            findings.append("- стр. " + str(line) + ": " + msg)
    if CYRILLIC.search(code):
        for m in BYTE_LEN.finditer(code):
            line = code[:m.start()].count(NEWLINE) + 1
            findings.append(
                "- стр. " + str(line) + ": оператор # считает БАЙТЫ (кириллица = 2 байта/символ). "
                "Для строк используй unicode.len() / unicode.wlen()")
    if not findings:
        return "Типовых ошибок не найдено."
    return "Найдено проблем: " + str(len(findings)) + NEWLINE + NEWLINE.join(findings)


if __name__ == "__main__":
    mcp.run()
