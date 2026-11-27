# Control versions registry (the one place to look)

Last verified against a real Studio round trip: **27/11/2026** (Branch Contact Groups, four screens pasted into Studio and copied back out of the Screen YAML Vault).

**If anything else in this Bible names a control version that disagrees with this file, this file wins.** Fix the other page when you find it.

## Where the truth comes from (best first)

1. **What Power Apps Studio itself writes out.** Microsoft does not publish a per-control version table. Its pages on [modern control updates](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-control-updates) and [Power Apps YAML](https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/power-apps-yaml) list no version numbers (checked 27/11/2026). So the version Studio exports is the evidence. Every Screen YAML Vault save is a fresh sample.
2. **Microsoft's description of what changed** between versions, on the modern control updates page above (for example Dropdown `DefaultSelectedItems` became `Default`; Checkbox `FontColor` became `Color`, `FontSize` became `Size`; Text Input `OnChange` fires on focus-out only).
3. **Microsoft's YAML page says** that the `@` version is optional and that, without one, the most current version of the control is used. Not yet tested in Studio by us. See "Open experiment" below.
4. The fresh-control lab (`powerapps-control-defaults.md`) for property defaults. It was last run 20/06/2026, so treat its version column as old.

## Current versions (seen in Studio output on 27/11/2026)

| Control | Version | Notes |
|---|---|---|
| Classic/Button | `Classic/Button@2.2.0` | |
| Classic/DatePicker | `Classic/DatePicker@2.6.0` | `DefaultDate` is settable, `SelectedDate` is read-only |
| Classic/Icon | `Classic/Icon@2.5.0` | |
| Classic/TextInput | `Classic/TextInput@2.3.2` | Multi-line via `Mode: =TextMode.MultiLine` |
| Gallery | `Gallery@2.15.0` | Needs `Variant:` |
| Image | `Image@2.2.3` | |
| Label | `Label@2.5.1` | |
| ModernButton | `ModernButton@1.0.0` | |
| ModernCheckbox | `ModernCheckbox@1.0.2` | Input is `Default`, output is `.Checked`. Studio drops `Height` |
| ModernDropdown | `ModernDropdown@1.0.3` | Write `ItemDisplayText: =ThisItem.Value` yourself |
| ModernTextInput | `ModernTextInput@1.1.2` | |
| Timer | `Timer@2.1.0` | |

## Superseded (do not generate these any more)

| Old | Now | What changes |
|---|---|---|
| `CheckBox@0.0.30` | `ModernCheckbox@1.0.2` | The type name changes. `Checked` as an input becomes `Default`. Studio adds `FontWeight: =""` and empty `OnCheck` / `OnUncheck`, and drops `Height`. `chk.Checked` still works as an output. |
| `ModernTextInput@1.1.0` | `ModernTextInput@1.1.2` | No property changes seen. |
| `ModernDropdown@1.0.1` | `ModernDropdown@1.0.3` | Studio adds `ItemDisplayText: =ThisItem.Value`. |

## Not re-checked since the old allowlist (assume they may be stale)

`Classic/DropDown@2.3.1`, `Classic/ComboBox@2.4.0`, `Classic/CheckBox@2.1.0`, `Classic/Toggle@2.1.0`, `Toggle@1.1.5`, `Form@2.4.4`, `GroupContainer@1.5.0`, `Rectangle@2.3.0`, `HtmlViewer@2.1.0`, `ModernCombobox@1.1.0`, `ModernDatePicker@1.0.0`. Nobody has seen these in a Studio export since the allowlist was written. The first time one is used in a real app, run the checker and update this table.

## The "Value1" mystery, explained (27/11/2026)

`ThisItem.Value1` appears in the dropdown's `ItemDisplayText`, which Studio generates itself when it upgrades a `ModernDropdown` to 1.0.3. Copying the control back out does not contain `Value1`, so it is not in our YAML. Studio's auto-binding sometimes picks the wrong column name. Workaround: delete the `1`. Writing `ItemDisplayText: =ThisItem.Value` ourselves should reduce it, but is not proven. A different `Value`/`Value1` collision (record literal `{Value: x.Value}` in `Default`) is covered in `live-build-lessons.md`.

Also, **control names are unique across the whole app, not per screen.** Pasting a screen that reuses a name from another screen makes Studio rename it (`recHeader_1`) and rewrite the references. Give every control a name that is unique in the app (we add a screen suffix, for example `recHeaderMg`).

## How to keep this file evergreen

1. **After every Studio round trip** (any time screens are saved back to the Screen YAML Vault), run:
   `python tools/check-control-versions.py --vault <app-slug>`
   It reads the vault, lists every `Control: Type@version`, and tells you which are current, superseded or unknown. Anything unknown or superseded: update the table above and fix the pages below.
2. Also check a project's own source: `python tools/check-control-versions.py path\to\screen.yaml`.
3. When Studio shows the update notice on a control, or a paste warns about a version (PA2105), treat that as a trigger to re-run the check.
4. Pages that quote versions and must be kept in step: `yaml-validation-checklist.md` (allowlist), `verified-control-reference.md`, `powerapps-control-defaults.md`.

## Open experiment (not done yet)

Microsoft says that leaving the `@version` off means "latest". If a paste of unversioned controls works in Studio, we could stop pinning versions and this file would matter much less. Test with one small screen before changing any generator.

## Machine-readable lists (read by `tools/check-control-versions.py`, keep the format)

```current-versions
Classic/Button@2.2.0
Classic/DatePicker@2.6.0
Classic/Icon@2.5.0
Classic/TextInput@2.3.2
Gallery@2.15.0
Image@2.2.3
Label@2.5.1
ModernButton@1.0.0
ModernCheckbox@1.0.2
ModernDropdown@1.0.3
ModernTextInput@1.1.2
Timer@2.1.0
```

```unverified-versions
Classic/DropDown@2.3.1
Classic/ComboBox@2.4.0
Classic/CheckBox@2.1.0
Classic/Toggle@2.1.0
Toggle@1.1.5
Form@2.4.4
GroupContainer@1.5.0
Rectangle@2.3.0
HtmlViewer@2.1.0
ModernCombobox@1.1.0
ModernDatePicker@1.0.0
```

```superseded-versions
CheckBox@0.0.30 -> ModernCheckbox@1.0.2
ModernTextInput@1.1.0 -> ModernTextInput@1.1.2
ModernDropdown@1.0.1 -> ModernDropdown@1.0.3
```
