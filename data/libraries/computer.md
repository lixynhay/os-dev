# computer — управление ПК

```lua
local computer = require("computer")
```

- `computer.shutdown([reboot: bool])` — выключить/перезагрузить
- `computer.beep([freq[, duration]])` — пищалка (стандартный сигнал без аргументов)
- `computer.uptime(): number` — секунды с загрузки
- `computer.freeMemory()`, `computer.totalMemory()` — байты RAM
- `computer.energy()`, `computer.maxEnergy()` — заряд внутреннего буфера
- `computer.getBootAddress() / setBootAddress(address)` — с какого диска грузиться
- `computer.pullSignal([timeout])` — низкоуровневый аналог event.pull
