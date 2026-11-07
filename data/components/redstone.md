# redstone — карта/блок красного камня

Стороны (библиотека `sides`): bottom=0, top=1, north=2, south=3, west=4, east=5

- `getInput(side): number` — сигнал 0..15
- `setOutput(side, value)`, `getOutput(side)`
- `getBundledInput(side, color)`, `getBundledOutput(side, color)`, `setBundledOutput(side, color, value)` — Project Red bundled cables

## Грабли
- Сторона считается ОТ БЛОКА-компонента, а не от игрока
- `setOutput` подаёт сигнал постоянно, пока не вызовешь снова (нет "импульса" из коробки — делай через event.timer или os.sleep)
