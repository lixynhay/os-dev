# Сводка граблей OpenComputers

1. **touch-распаковка**: `event.pull("touch")` → `(name, screenAddress, x, y, ...)`. Первый аргумент — адрес экрана.
2. **# vs unicode**: `#` считает байты; кириллица = 2 байта/символ. Только `unicode.len/wlen/sub`.
3. **CC ≠ OC**: `os.pullEvent`, `term.setTextColor`, `term.getCursorPos` — не существуют в OpenOS.
4. **Ctrl+C**: без обработки `"interrupted"` вечный цикл не остановить.
5. **Модем**: порт не открыт → сообщения теряются молча.
6. **touch mode**: клики «не работают» → `screen.setTouchModeInverted(true)`.
7. **Разрешение**: после `gpu.setResolution()` сделай `gpu.fill`, старый текст не затирается полностью.
8. **Версии API**: состав методов периферии плавает между версиями OC/OpenPeripheral/MC — проверяй `component.methods(address)` в игре.
9. **Стороны блоков**: `side` в redstone/inventory — относительно блока-компонента.
10. **RAM/энергия**: скрипты едят память; большие строки/таблицы — контролируй `computer.freeMemory()`.
