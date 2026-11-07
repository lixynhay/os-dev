# inventory_controller — контроллер инвентаря

Работает через адаптер у сундука/механизма или как апгрейд робота.

- `getInventorySize(side): number`
- `getInventoryName(side): string`
- `getStackInSlot(side, slot): table|nil` — `{name, label, size, damage, maxDamage, maxSize, ...}`; набор полей зависит от версии MC/мода
- `getAllStacks(side)` — итератор (deprecated в новых версиях)
- `extractItem(side, slot, count[, direction]): number` — **только роботы**

## Грабли
- Слоты нумеруются с 1
- Возле адаптера поле `side` = сторона блока с инвентарём
