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
