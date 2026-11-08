# OpenPeripheral — PIM and Adapter

Reference for the OpenPeripheral integration used by `me-control`. Sources:
OpenPeripheral wiki, OC peripheral docs, and this project (`me_api.lua`).

> OpenPeripheral method names shift between versions. Verify in-game:
> `for k, v in pairs(component.methods(address)) do print(k, v) end`
> and watch events live with `=event.pull()` in the OpenOS shell.

---

## PIM — Personal Inventory Manager

A block layer the player stands on; it exposes the standing player's inventory
as a peripheral. The computer talks to it via the `pim` component.

### Inventory queries

| Method | Returns | Notes |
|---|---|---|
| `getInventorySize()` | `number` | Number of slots in the player's inventory. |
| `getStackInSlot(slotNumber: number)` | `table` or `nil` | Item in a slot — see field note below. |
| `getInventoryName()` | `string` | Nickname of the player on the PIM. |

### `getStackInSlot` field names — critical
The returned table uses **OpenPeripheral** field names, **not** the OC/AE names:

| OpenPeripheral (PIM) | OC / inventory_controller | Meaning |
|---|---|---|
| `display_name` | `label` | Human-readable item name |
| `qty` | `size` | Stack count |

```lua
local stack = pim.getStackInSlot(1)
if stack then
  print(stack.display_name, stack.qty)   -- NOT stack.label / stack.size
end
```
Other fields (e.g. `id`, `damage`, `max_size`) also vary by version.

### Moving items (player <-> adjacent inventory)

| Method | Returns | Notes |
|---|---|---|
| `pushItem(direction: string, slot: number[, maxAmount: number[, intoSlot: number]])` | `number` | Push from the player's inventory into an adjacent inventory (e.g. ME Interface). Returns items moved. |
| `pullItem(direction: string, slot: number[, maxAmount: number[, intoSlot: number]])` | `number` | Pull from an adjacent inventory into the player's inventory. |
| `condenseItems()` | - | Merge partial stacks. |
| `swapStacks(from: number, to: number)` | - | Swap two slots. |
| `destroyStack(slot: number)` | - | Delete a slot's contents. |

```lua
-- give the player 64 iron from the ME network via the interface
pim.pullItem("up", 1, 64)
-- take everything from the player's slot 1 back into the network
pim.pushItem("up", 1)
```

### Events
The PIM emits player-presence events when a player steps on/off:
- `player_on(name, uuid)`
- `player_off(name, uuid)`

```lua
local event = require("event")
while true do
  local ev, name = event.pull()          -- no timeout: wait for presence change
  if ev == "player_on" then print("Hi", name) end
end
```

### Pitfalls
- Gated on OpenPeripheral being installed — `component.isAvailable("pim")` first.
- `pushItem`/`pullItem` `direction` is a block side (`"up"`, `"down"`, `"north"`...).
- Method/field names drift between OpenPeripheral versions — always probe.

---

## Adapter

A block that **wraps a neighbouring block** and exposes it to the computer as a
peripheral, letting OC interact with blocks from other mods (IC2 reactors, AE2
interfaces, chests, machines, ...).

### How it works
- Place the Adapter **next to** the target block; it presents that block's
  peripheral methods to the connected computer.
- The wrapped block's own methods appear on the `component` of the matching type
  (e.g. an AE2 ME Interface becomes `me_interface`).
- Typical uses: energy/machine control (IC2, GT), reading chests via
  `inventory_controller`, driving AE2 via `me_interface`.

### Pitfalls
- The adapter sees only the block on its facing side; orientation matters.
- Wrapped-block method names depend on the mod's OC integration — verify with
  `component.methods(address)`.
- Some machines expose only a subset (or nothing) — not every block is wrappable.

---

## Cross-references
- Component stubs: `data/components/pim.md`, `data/components/inventory_controller.md`.
- Events: `data/events/player_on_off.md`.
- Project implementation: `me_api.lua` (`getPlayerInventory`, `pushFromPlayer`,
  `exportToPlayer`, `depositAll`, `isPlayerPresent`).
