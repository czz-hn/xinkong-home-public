# Xinkong Home Public Framework

`Xinkong Home` is an edge AIoT home-control framework built around an RDK X5 device. This public repository is a competition-facing framework snapshot: it shows the main architecture, module boundaries, and extension points without publishing private deployment details or the complete competition implementation.

Chinese name: `芯控家居`

## What This Repository Shows

- Voice-first interaction flow with wake-gated command handling.
- Intent routing from natural language into structured tasks.
- A central orchestrator that coordinates smart-home control, local edge actions, camera/BPU vision, health sensing, weather queries, and voice replies.
- Adapter boundaries for Home Assistant, OpenClaw, ESP32/MQTT devices, RDK X5 BPU inference, and local TTS.
- Runtime health checks and graceful fallback concepts for edge deployment.
- A runnable simulation that demonstrates the control flow without real keys, models, or devices.

## Competition Highlights

- **RDK X5 edge hub:** the system is organized around an RDK X5 edge node, with camera/BPU perception, voice interaction, local services, and smart-home control sharing one runtime.
- **Multi-modal closed loop:** voice commands can trigger device control, local vision inspection, health sensing, weather queries, and runtime status checks through one orchestration layer.
- **BPU-aware design:** the public skeleton exposes the BPU vision boundary while keeping model files, preprocessing details, and private inference tuning out of the repository.
- **Safety-first orchestration:** high-risk actions pass through a risk policy boundary before adapter dispatch; private scene-fusion rules are intentionally not published.
- **Hybrid reliability:** the full project combines online AI services with local fallbacks, startup warmup, watchdog checks, and health snapshots for competition-site stability.
- **Clear extension points:** adapters keep Home Assistant, OpenClaw, ESP32/MQTT, health sensors, weather, TTS, and vision modules replaceable.

## What Is Intentionally Not Published

The full competition project contains hardware parameters, production configuration, model files, private recovery logic, field-tuned safety policies, and complete orchestration code. Those parts are not included here.

This public version replaces sensitive or high-value implementation details with interfaces, short example logic, and comments. In particular, this repository does not include:

- API keys, tokens, hotspot passwords, real network addresses, or `.env` files.
- BPU `.bin` models, ONNX models, Vosk models, Piper voices, or model conversion scripts.
- Full `main.py` production logic.
- Full Home Assistant/OpenClaw whitelist configuration.
- Complete ESP32 firmware used in the live competition setup.
- Competition reports, demo scripts, private logs, face galleries, or runtime data.

## High-Level Flow

```text
Voice/Text Input
  -> wake gate and session guard
  -> intent router
  -> task orchestrator
  -> safety policy
  -> adapters: Home Assistant / OpenClaw / Camera+BPU / Health / Weather
  -> reply assembler
  -> local or cloud TTS
```

## Quick Start

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
python main.py --demo
PYTHONPATH=src python -m unittest discover -s tests
```

The demo uses only simulated adapters. It does not connect to Home Assistant, MQTT, OpenClaw, cloud speech services, or RDK hardware.

## Repository Layout

```text
main.py                      Public entry-point skeleton.
config/config.example.yaml   Redacted example configuration.
src/xinkong_home/            Framework modules and interfaces.
examples/simulated_run.py    Small offline simulation.
tests/                       Interface-level tests for the public skeleton.
docs/architecture.md         System architecture overview.
docs/system_overview.md      Feature matrix and module responsibilities.
docs/open_source_boundary.md What is public and what remains private.
```

## Public `main.py` Boundary

The public `main.py` keeps the startup shape visible: config loading, module construction, event handling, planning, safety checking, adapter dispatch, and reply generation.

Production details are deliberately represented as comments, including:

- realtime cloud speech session supervision;
- noisy-scene wake-word tuning;
- RDK X5 boot optimization and warmup scheduling;
- hardware-specific BPU inference calls;
- safety-scene fusion logic;
- competition demo recovery paths.

## License And Use

This repository is published for competition review and technical demonstration. Unless a separate open-source license is added by the author, all rights are reserved. Do not copy, redistribute, commercialize, or reuse the code as a complete product without permission.
