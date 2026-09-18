<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/logo-dark.svg">
    <img src="assets/logo-light.svg" alt="TPowerPlanSwitcher" width="420">
  </picture>
</div>

A tiny Windows tray app that switches between two power plans with one click. Default: **Balanced** / **Power saver**.

- Left click — switch to the other plan
- Icon/tooltip always reflect the real active plan, even when changed from Windows Settings or the battery flyout

## How it works

Uses `PowerGetActiveScheme` / `PowerSetActiveScheme` from `powrprof.dll` — no `powercfg.exe`, no console flash. External changes are caught via a registry change notification (`RegNotifyChangeKeyValue`), so the watcher consumes zero CPU when idle (no polling).

## Requirements

- Windows 10/11, Python ≥ 3.9
- `pip install pystray pillow`

## Run from source

```bash
python TPowerPlanSwitcher.py
```

## Build .exe

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "TPowerPlanSwitcher" --icon "TPowerPlanSwitcher.ico" TPowerPlanSwitcher.py
```

## Custom plans

Edit near the top of `TPowerPlanSwitcher.py`:

```python
BALANCED_GUID = "381b4222-f694-41f0-9685-ff5bb260df2e"
POWER_SAVER_GUID = "a1841308-3541-4fab-bc81-f71556f20b4a"

PLAN_NAMES = {
    BALANCED_GUID: "Balanced",
    POWER_SAVER_GUID: "Power saver",
}
```

Standard GUIDs (list all on your machine with `powercfg /list`):

| Plan | GUID |
| --- | --- |
| Balanced | `381b4222-f694-41f0-9685-ff5bb260df2e` |
| Power saver | `a1841308-3541-4fab-bc81-f71556f20b4a` |
| High performance | `8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c` |
| Ultimate performance | `e9a42b02-d5df-448d-aa00-03f14749eb61` |

High/Ultimate performance are hidden on many Windows 11 installs — search internet how to activate them.

## Notes

- PyInstaller exes may be flagged by antivirus (false positive); add an exclusion if needed.

## License

MIT
