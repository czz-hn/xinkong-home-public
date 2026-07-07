# Public Boundary

This repository is designed for GitHub publication while protecting the private competition implementation.

## Included

- Public entry-point skeleton: `main.py`.
- Module interfaces and simplified data models.
- Simulated adapters for Home Assistant, OpenClaw, BPU vision, health sensors, weather, and TTS.
- Example redacted configuration.
- Basic tests that prove the public framework is runnable.
- Architecture notes.

## Excluded

- `.env`, tokens, cloud keys, API secrets, Wi-Fi passwords, and real network addresses.
- Model files: `.onnx`, `.bin`, Vosk archives, Piper voices, and model cache directories.
- Full production `main.py`.
- Full orchestration logic for mixed commands, fallback ordering, safety fusion, and competition demo recovery.
- Real Home Assistant entity maps, OpenClaw whitelist, MQTT topics, and ESP32 production firmware.
- Face gallery data, logs, runtime state, screenshots, reports, and final demo documents.

## Why This Boundary Exists

The competition requires public code, but the live system contains private deployment knowledge and field-tuned logic. Publishing this skeleton gives reviewers a truthful view of the architecture while avoiding direct reuse of the complete project.

## Before Publishing To GitHub

Run:

```bash
pytest
grep -RInE "sk-|AKIA|SECRET|TOKEN|PASSWORD|123456|192\\.168|DASHSCOPE|BAILIAN|HA_API|OPENCLAW" .
find . -type f \( -name "*.onnx" -o -name "*.bin" -o -name "*.zip" -o -name ".env" \)
```

The first command should pass. The second command may find placeholder names in documentation or config, but it must not reveal real secrets. The third command should print nothing except intentional documentation matches if you change it.

