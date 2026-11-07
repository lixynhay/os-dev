# screen — монитор

- `isTouchModeInverted(): bool`
- `setTouchModeInverted(bool): bool`
  - `false` (дефолт): правый клик = GUI, **Shift + правый клик = touch**
  - `true`: правый клик = touch, Shift + клик = GUI
- `setPrecise(bool)` / `isPrecise()` — высокоточный тач, **только T3**;
  в старых версиях OC может отсутствовать — проверь `component.methods()`

## Грабли
- «Клики не работают» в 90% случаев = не тот touch mode. Первым делом включай инвертированный режим.
- События тача: `touch`, `drag`, `drop`, `scroll` — см. get_event.
