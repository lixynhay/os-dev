# Applied Energistics 2 — OpenComputers integration

Reference for driving an ME network from OpenComputers via the `me_interface`
component (requires an Adapter on the ME block). Sources: AE2 wiki, OC/AE2
integration notes, and this project (`me_api.lua`).

> Method names drift between AE2 + OC versions. Always verify in-game:
> `for k, v in pairs(component.methods(component.list("me_interface")())) do print(k, v) end`

---

## `me_interface` component

| Method | Returns | Notes |
|---|---|---|
| `getItemsInNetwork([filter: table])` | `table` | Array of stacks: `{ name, label, size, damage, ... }`. `label` is the display name, `size` the count, `damage` the metadata. |
| `getFluidsInNetwork()` | `table` | Array of fluid stacks `{ name, label, amount, ... }`. |
| `getCraftables([filter: table])` | `table` | Array of **craftable userdata** objects (see below) — not plain tables. |
| `getCpus()` | `table` | Array of crafting-CPU records / proxies. |
| `getStoredPower()` | `number` | Stored energy in AE. (Also named `getEnergyStored` on some builds.) |
| `getMaxStoredPower()` | `number` | Capacity in AE. (Also `getMaxEnergyStored`.) |
| `getAvgPowerInjection()` | `number` | Average energy input, AE/t. |
| `getAvgPowerUsage()` | `number` | Average energy consumption, AE/t. |
| `exportItem(fingerprint: table, direction: string, amount: number, mode: number)` | `number` | Push items out of the ME network to an adjacent inventory. |

### `filter` table
Partial match; omitted fields are ignored.
```lua
local items = me.getItemsInNetwork({ name = "minecraft:iron_ingot", damage = 0 })
```

### `exportItem` and NBT-bearing items
`fingerprint` is not just `{name, damage}` — for items with NBT data you must pass
the **full stack table returned by `getItemsInNetwork`** (which carries the NBT /
fingerprint fields). Constructing a minimal `{name, damage}` table will move the
wrong stack or fail.
```lua
for _, stack in ipairs(me.getItemsInNetwork()) do
  if stack.label == "Iron Ingot" then
    -- pass the object as-is: it carries the fingerprint/NBT
    me.exportItem(stack, "west", 64, 1)
    break
  end
end
```
- `direction`: side of the ME Interface, e.g. `"north"`, `"up"`, `"west"`.
- `amount`: item count. `mode`: transfer mode (see AE2 for exact constants).

---

## `me_controller` component

Exists on some setups alongside `me_interface`. It **duplicates the energy and
network-query methods** so you can read them without the interface:

| Method | Returns |
|---|---|
| `getStoredPower()` / `getMaxStoredPower()` | `number` |
| `getItemsInNetwork([filter])` | `table` |
| `getFluidsInNetwork()` | `table` |
| `getCraftables([filter])` | `table` |

Reading strategy used in `me_api.lua`: try the method on `me_interface`, then on
`me_controller`, then fall back to alternative names (`getEnergyStored`,
`getMaxEnergyStored`, `getEnergy`, `getMaxEnergy`).

---

## Craftable userdata (recipe object)

Returned by `getCraftables()`. Access via methods, not fields.

| Method | Returns | Notes |
|---|---|---|
| `getItemStack()` | `table` | The output stack: `{ label, name, damage, ... }`. |
| `request([amount: int[, prioritizePower: boolean[, cpuName: string]]])` | `userdata` (CraftingStatus) | Submit a craft job to the network. |
| `requestCrafting(...)` | `userdata` or `boolean` | Alternate name on some builds — probe with `component.methods`. |

```lua
for _, recipe in ipairs(me.getCraftables()) do
  local stack = recipe.getItemStack()
  if stack.label == "Iron Gear" then
    local status = recipe.request(8)          -- craft 8
    -- optionally: recipe.request(8, true, "MyCPU")
    break
  end
end
```

### Pitfalls
- `getCraftables()` entries are **opaque userdata** with methods — never index them
  as tables.
- Wrapping `request` in `pcall` is mandatory: a busy CPU or missing pattern raises.
- `request` only **queues** the job; poll status separately (see below).

---

## CraftingStatus userdata (job status object)

Returned by `request(...)` and by status-query calls.

| Method | Returns | Notes |
|---|---|---|
| `isDone()` | `boolean` | Job finished successfully. |
| `isCanceled()` | `boolean` | Job was canceled. |
| `isComputing()` | `boolean` | Still in progress (on some builds). |
| `hasFailed()` | `boolean` | Failed (e.g. resources vanished). |
| `cancel()` | - | Cancel the job if supported. |

```lua
local status = recipe.request(8)
while not (status.isDone() or status.isCanceled()) do
  os.sleep(1)
end
if status.isDone() then print("ready") else print("canceled") end
```

### Pitfalls
- Status is **not** pushed as an event — poll the userdata periodically.
- A stale status object may stop being readable; treat a `pcall` failure as
  "tracking lost", matching `main.lua`'s behavior.

---

## Cross-references
- Component stub in the data dir: `data/components/me_interface.md`.
- Project implementation: `me_api.lua` (`getNetworkInfo`, `getCraftables`,
  `getCraftingInfo`, `exportToPlayer`, `depositAll`).
