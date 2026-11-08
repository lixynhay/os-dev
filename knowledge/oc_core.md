# OpenComputers Core API

Consolidated reference for the OpenOS core libraries and events used by `me-control`
and any OC program. Sources: ocdoc.cil.li, OC wiki, and this project.

> Golden rule: when a peripheral's method list is uncertain, dump it in-game:
> `for k, v in pairs(component.methods(address)) do print(k, v) end`

---

## `component` — component access

```lua
local component = require("component")
```

| Function | Returns | Notes |
|---|---|---|
| `component.list([filter: string])` | iterator `(address, type)` | `filter` is an exact component name or a prefix (`"gpu"`). |
| `component.proxy(address: string)` | component proxy | Methods of the component by address. Preferred for multi-component setups. |
| `component.methods(address: string)` | `table { name = docstring }` | Full method list; primary way to verify API version. |
| `component.doc(address, method)` | `string` | Docstring of one method. |
| `component.isAvailable(type: string)` | `boolean` | Whether a component of this type exists. |
| `component.getPrimary(type: string)` | proxy | The primary (first) component of a type. Also `component.type`, `component.slot`. |
| `component.gpu`, `component.screen`, ... | proxy | Direct access to the primary component of that type. |

### Example — iterate all screens
```lua
local component = require("component")
for address, ctype in component.list("screen") do
  print(ctype, address)
end
```

### Pitfalls
- `component.<name>` returns the **primary** component; with several same-type
  components, address them explicitly via `component.proxy(list(...))`.
- Component fields are resolved lazily — a returned proxy never uses the
  `__index` metamethod, so save it to a local (`local gpu = component.gpu`).

---

## `event` — event model

```lua
local event = require("event")
```

| Function | Returns | Notes |
|---|---|---|
| `event.pull([timeout: number[, name: string[, ...]]])` | `name, args...` | Blocks up to `timeout` (or forever without it). Optional filters restrict event types. |
| `event.pullMultiple(name1, name2, ...)` | `name, args...` | Wait for any of several event types. |
| `event.listen(name: string, callback: function)` | - | Callback-style handler. |
| `event.ignore(name: string, callback: function)` | - | Remove a handler. |
| `event.timer(interval: number, callback: function[, times: number])` | `id` | Periodic timer; cancel via `event.cancel(id)`. |
| `event.cancel(id)` | - | Cancel timer/registration. |
| `event.push(name: string, ...)` | - | Queue an event manually (testing). |

### Event signatures (critical)

| Event | Signature |
|---|---|
| `touch` | `touch(screenAddress: string, x: number, y: number, button: number, playerName: string)` |
| `drag` | `drag(screenAddress: string, x: number, y: number, button: number, playerName: string)` — same shape as `touch` |
| `drop` | `drop(screenAddress: string, x: number, y: number, button: number, playerName: string)` — same shape as `touch` |
| `scroll` | `scroll(screenAddress: string, x: number, y: number, direction: number, playerName: string)` — same shape as `touch`; `direction` replaces `button` (−1/1) |
| `modem_message` | `modem_message(localNetworkCard: string, remoteAddress: string, port: number, distance: number, payload: any)` |
| `key_down` | `key_down(keyboardAddress: string, char: number, code: number, playerName: string)` |
| `key_up` | `key_up(keyboardAddress: string, char: number, code: number, playerName: string)` |

`char` is the character code (0 for special keys); `code` is the scan code
(compare against `keyboard.keys.*`). `touch`/`drag`/`drop`/`scroll` `button`:
`0` = left, `1` = right.

### The #1 unpacking mistake
```lua
-- WRONG: x gets the screen address (a string), y gets the X coordinate
local x, y = event.pull("touch")
-- RIGHT
local _, _, x, y = event.pull("touch")
-- or
local _, addr, x, y, btn, player = event.pull("touch")
```

### Pitfalls
- `pull()` with no timeout blocks forever — use a timeout (`event.pull(0.05)`) in loops.
- In an infinite loop always handle `"interrupted"` (Ctrl+C), or the script can't stop.
- `event.pull` returns the **event name first**, so handlers often `select(2, ...)`.

---

## `gpu` — video

```lua
local gpu = require("component").gpu
```

| Function | Returns | Notes |
|---|---|---|
| `gpu.setResolution(w, h)` | `boolean` | Does **not** clear the screen — `gpu.fill()` after. |
| `gpu.maxResolution()` | `w, h` | Max for the bound screen. |
| `gpu.getResolution()` | `w, h` | Current resolution. |
| `gpu.set(x, y, value[, vertical])` | - | `value` may be a UTF-8 string. |
| `gpu.get(x, y)` | `char, fg, bg` | Read one cell. |
| `gpu.fill(x, y, w, h, char)` | - | Fill a rectangle. |
| `gpu.copy(x, y, w, h, tx, ty)` | - | Copy a region (basis of fast scrolling). |
| `gpu.setForeground(color[, palette])` | `oldColor` | `0xRRGGBB` (T3) or palette index. |
| `gpu.getForeground()` | `color, palette` | |
| `gpu.setBackground(color[, palette])` | `oldColor` | |
| `gpu.getBackground()` | `color, palette` | |
| `gpu.maxDepth()`, `gpu.getDepth()`, `gpu.setDepth(d)` | - | Color depth (T2 = 4-bit/16 colors, T3 = 8-bit/256). |

| Screen tier | maxResolution | Colors |
|---|---|---|
| T1 | 50×16 | 2 (1-bit) |
| T2 | 80×25 | 16 (4-bit) |
| T3 | 160×50 | 256 (8-bit) |

### Pitfalls
- Coordinates outside the screen raise an error — clamp to bounds.
- Center text with `unicode.wlen()`, not `#`, so double-width glyphs line up.

---

## `unicode` — UTF-8 strings (critical for Cyrillic)

```lua
local unicode = require("unicode")
```

| Function | Returns | Notes |
|---|---|---|
| `unicode.len(s)` | number of **characters** | `#` counts **bytes** (a Cyrillic letter = 2 bytes). |
| `unicode.sub(s, i[, j])` | string | Slice by characters. |
| `unicode.char(...)` | string | Build a string from character codes. |
| `unicode.wlen(s)` | printed width | Double-width chars count as 2 columns — use for centering. |
| `unicode.lower(s)`, `unicode.upper(s)` | string | Case conversion. |

```lua
local s = "Привет"
print(#s)             -- 12 bytes  (WRONG for UI math)
print(unicode.len(s)) -- 6 chars
```

---

## `term` — terminal

```lua
local term = require("term")
```

| Function | Returns | Notes |
|---|---|---|
| `term.clear()` | - | Clear screen; cursor to (1, 1). |
| `term.clearLine()` | - | Clear the current line (progress bars). |
| `term.write(s)` | - | Output without a trailing newline. |
| `term.setCursor(x, y)` | - | Move cursor. |
| `term.getCursor()` | `x, y` | Read cursor position. |

### OpenOS ≠ ComputerCraft
| ComputerCraft | OpenOS equivalent |
|---|---|
| `term.setTextColor()` / `term.setBackgroundColor()` | `gpu.setForeground()` / `gpu.setBackground()` |
| `term.getCursorPos()` / `term.setCursorPos()` | `term.getCursor()` / `term.setCursor()` |
| `term.isColor()` | `gpu.getDepth()` / `gpu.maxDepth()` |
| `os.pullEvent()` | `event.pull()` |

---

## Cross-references
- Events deep-dive: `data/events/touch.md`, `key_down.md`, `modem_message.md`, `player_on_off.md`.
- Libraries: `data/libraries/component.md`, `event.md`, `unicode.md`, `term.md`.
- Common gotchas: `data/pitfalls.md`; code recipes: `data/patterns.md`.
