# GitHub Publish Checklist

Use this directory as an independent GitHub repository:

```text
/Users/czz/Documents/New project/rdk_migration/xinkong-home-public
```

## Files Intended For Publication

- `README.md`
- `LICENSE`
- `pyproject.toml`
- `.gitignore`
- `main.py`
- `config/config.example.yaml`
- `src/xinkong_home/*.py`
- `examples/simulated_run.py`
- `tests/test_public_skeleton.py`
- `docs/architecture.md`
- `docs/system_overview.md`
- `docs/open_source_boundary.md`
- `docs/github_publish_checklist.md`

## Must Not Be Added

- `.env`
- real `config/*.private.yaml`
- `models/`
- `logs/`
- `data/`
- `*.onnx`
- `*.bin`
- `*.zip`
- private reports or demo scripts
- full ESP32 production firmware
- Home Assistant entity maps with real device names
- OpenClaw private whitelist files

## Local Verification

Run from the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 main.py --demo
find . -type f \( -name "*.onnx" -o -name "*.bin" -o -name "*.zip" -o -name ".env" -o -name "*.pyc" \) -print
```

The first command should pass. The second command should print simulated outcomes. The third command should print nothing.

## Suggested Git Commands

```bash
git init
git add README.md LICENSE pyproject.toml .gitignore main.py config src examples tests docs
git status --short
git commit -m "Add public Xinkong Home framework skeleton"
```

Review `git status --short` before committing. Only the public files listed above should appear.
