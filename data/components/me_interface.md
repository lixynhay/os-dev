# me_interface — Applied Energistics 2 (через адаптер)

- `getItemsInNetwork([filter]): table` — `{name, label, size, damage, ...}`
- `getCraftables([filter]): table`
- `craft(item): bool, err` — запрос крафта по детали
- filter: `{name = "minecraft:stone", damage = 0}` (поля опциональны)

## Грабли
- Состав методов сильно зависит от версий AE2 + OC. Перед кодом распечатай:
  `for k in pairs(component.methods(address)) do print(k) end`
- `craft` ставит задачу в очередь, крафт может завершиться позже
