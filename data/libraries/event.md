# event

## Методы
- `pull([timeout: number], [eventName: string], [filter1: any], ...): string, any, ...` — ждать событие. Возвращает `eventName` и аргументы.
- `pullMultiple([timeout: number], [eventName1: string, eventName2: string, ...]): string, any, ...` — ждать любое из нескольких событий.
- `listen(eventName: string, callback: function)` — подписаться на событие (callback-стиль).
- `timer(interval: number, callback: function[, times: number]): number` — таймер.
- `cancel(timerId: number)` — отменить таймер.

## Важно
- `event.pull()` без таймаута может заблокировать скрипт навсегда.
- Не фильтруй `touch` через `event.pull("touch")` при нескольких событиях — может пропускать. Лучше ловить всё и проверять `if ev == "touch"`.
