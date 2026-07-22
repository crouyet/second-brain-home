# Resumenes / Statements — where your financial closes read from

The **finance module** (`cierre-finanzas` skill + `tools/finanzas/categorizar.py`) analyzes
the card/account statements you drop **in this folder**. Nothing is auto-fetched — you
export from your bank and save the file here.

## Filename format (required)

The tools match files by name, so the naming convention matters:

```
MM-YYYY-<source>.<ext>
```

- `MM` = month (01–12), `YYYY` = year
- `<source>` = a short lowercase tag for the account/card (e.g. `visa`, `master`, `cuentas`, `mercadopago`)
- `<ext>` = the file type your bank exports (`xls`, `xlsx`, `pdf`, `csv`)

### Examples

```
07-2026-visa.xls
07-2026-master.xls
07-2026-cuentas.pdf
07-2026-mercadopago.pdf
```

A month is considered "complete" (ready to close) when its expected set of files is present.
Define your own expected set in `vault/Projects/Sistema/config.md` under `finanzas.expected_files`.

## Privacy

**These files are personal and git-ignored** (`.gitignore` blocks `*.xls`, `*.pdf`, `*.csv`
in this folder). They never leave your machine. Do not commit real statements.
