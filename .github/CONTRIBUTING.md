# Contributing to CashPilot

Contributions are welcome! Here's how to get started.

## Adding a Service (easiest contribution)

This is the most impactful way to contribute. Each service is a single YAML file.

1. Create `services/{category}/{slug}.yml` following the schema in `services/_schema.yml`
2. Add a guide page at `docs/guides/{slug}.md` with setup instructions
3. Update the service table in `README.md`
4. Submit a PR

Look at any existing YAML file in `services/` for reference. Categories: `bandwidth`, `depin`, `storage`, `compute`, `mining`.

## Adding an Earnings Collector

Collectors fetch balance/earnings from service APIs. See `app/collectors/` for examples.

1. Create `app/collectors/{slug}.py` extending `BaseCollector` from `app/collectors/base.py`
2. Register it in `app/collectors/__init__.py`
3. Add required credentials as `?optional` or required params

## Bug Fixes and Features

1. Fork the repo and create a branch (`fix/description` or `feature/description`)
2. Make your changes
3. Run linting: `ruff check app/ && ruff format --check app/`
4. Submit a PR with a clear description

## Adding or Changing Text in the Web UI

The web UI shows each message in 20 languages. The English is in `app/i18n/en.json`, and code shows a message by its key: `t("key")` in Python and the templates, `t('key')` in the JavaScript. Each other language has its own file, `app/i18n/<locale>.json`, where every entry is `{"text": ..., "source": ...}`. The `source` is a hash of the English that the text translates. When the English changes, the hash no longer matches, and the UI shows the English until the text is translated again.

Catalog Check runs `python scripts/i18n_check.py app/i18n/en.json app/i18n/*.json` on every PR. It fails when a locale file lacks a key, or when a text's placeholders, tags or links differ from the English. An out-of-date translation (a stale hash) is only a warning.

So a new key must be in all 19 locale files in the same PR. You can do this in two ways.

**Translate it.** Write the translation into each locale file as a plain string, `"my.new_key": "..."`. Then run the check with `--stamp`. It turns each plain string into `{"text", "source"}` with the current hash:

```bash
python scripts/i18n_check.py app/i18n/en.json app/i18n/*.json --stamp
```

**Ship the English first.** Copy the English into each locale file with a hash that does not match, for example `"my.new_key": {"text": "<the English>", "source": "000000000000"}`. The check passes with a stale warning, and the UI shows the English. Each night a sync job translates stale and missing entries and opens a PR with the translations (`scripts/i18n-sync/`).

Do not use the real hash on an English copy, and do not leave the hash out. The check would then pass with no warning, and the English would stay as if it were the finished translation. The sync job records a hash for an entry that has none, so it would never translate that entry either.

When you change the English of a key, its translations go stale, and the sync job translates them again. If the change adds, removes or renames a placeholder, a tag or a link, the old translations no longer match the English, and the check fails. Then also replace that key's entry in each locale file with the new English and the hash that does not match, as for a new key: `{"text": "<the new English>", "source": "000000000000"}`. When you remove a key from `en.json`, remove it from each locale file too.

## Code Style

- **Linter:** [Ruff](https://docs.astral.sh/ruff/) with pycodestyle, pyflakes, isort, pyupgrade, bugbear, simplify
- **Line length:** 120
- **Formatting:** Ruff formatter (double quotes, 4-space indent)

Run before committing:

```bash
ruff check app/ --fix
ruff format app/
```

## Commit Messages

Use conventional commits: `type(scope): description`

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:
- `feat(collector): add Bitping earnings collector`
- `fix(deploy): handle missing Docker socket gracefully`
- `docs(service): add ProxyBase setup guide`
