# me_interface (Applied Energistics 2)

## Методы
- `getItemsInNetwork([filter: table]): table` — список предметов. Поля: `label`, `name`, `size`, `damage`, `fingerprint`.
- `getFluidsInNetwork(): table` — список жидкостей.
- `getCraftables([filter: table]): userdata` — список доступных рецептов (проверяй через pcall!).
- `getCpus(): table` — список сопроцессоров.
- `getStoredPower(): number` — текущая энергия.
- `getMaxStoredPower(): number` — максимальная энергия.
- `getAvgPowerInjection(): number` — входящая энергия (AE/t).
- `getAvgPowerUsage(): number` — расход энергии (AE/t).
- `exportItem(fingerprint: table, direction: string, amount: number, mode: number): number` — выдать предмет. Для NBT используй `item.fingerprint` из `getItemsInNetwork`.

## Craftable userdata
- `getItemStack(): table` — возвращает `{label, name, damage}`.
- `request([amount: int[, prioritizePower: boolean[, cpuName: string]]]): userdata` — отправить запрос на крафт.

## CraftingStatus userdata
- `isDone(): boolean`
- `isCanceled(): boolean`
