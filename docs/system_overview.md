# System Overview

This document summarizes the public framework view of Xinkong Home. It is intentionally architectural: it identifies the main modules and responsibilities without publishing the private competition implementation.

## Feature Matrix

| Area | Public Module | Runtime Role | Public Detail Level |
| --- | --- | --- | --- |
| Voice interaction | `main.py`, `app.py` | Accepts voice/text events, applies wake-gated handling, sends replies to TTS. | Startup and event-flow skeleton only. |
| Intent routing | `nlu.py`, `models.py` | Converts natural language into structured intent categories. | Small keyword router showing the interface. |
| Task orchestration | `orchestrator.py` | Converts intents into planned tasks and dispatches them to adapters. | Main task types and dispatch shape are visible. |
| Safety policy | `safety.py` | Classifies risk and blocks high-risk actions for confirmation. | Boundary is visible; private policy tuning is omitted. |
| Smart home | `adapters.py` | Represents Home Assistant REST/MQTT device control. | Protocol and simulation only. |
| OpenClaw / edge actions | `adapters.py` | Represents local edge actions and recovery hooks. | Protocol and simulation only. |
| RDK X5 BPU vision | `adapters.py`, `models.py` | Represents camera scene inspection and BPU detection summaries. | Detection summary boundary only; no model or inference code. |
| ESP32 / MQTT devices | `adapters.py`, `config.example.yaml` | Represents sensor/actuator communication through MQTT-style boundaries. | Integration concept only. |
| Health sensing | `adapters.py` | Represents heart rate, blood oxygen, and grip-force queries. | Protocol and simulation only. |
| Weather query | `adapters.py`, `nlu.py` | Represents automatic-location weather query flow. | Query boundary only. |
| Runtime health | `adapters.py`, `orchestrator.py` | Represents service health checks for voice, smart-home, and BPU modules. | Simulated health check result shape. |

## Public Data Flow

```text
VoiceEvent
  -> XinkongHomeApp
  -> IntentRouter
  -> SafetyPolicy
  -> TaskOrchestrator
  -> RuntimeAdapters
  -> ExecutionOutcome
  -> SpeechSynthesizer
```

## Private Implementation Boundary

The live competition project contains additional logic that is not published here:

- realtime speech session supervision and reconnect strategy;
- full Chinese command normalization and noisy-site wake gating;
- Home Assistant entity maps and OpenClaw action whitelist;
- ESP32 production firmware and hardware pin details;
- RDK camera service implementation and BPU model loading;
- model files, preprocessing parameters, and inference tuning;
- safety-scene fusion, recovery policies, and competition demo scripts.

This public package is therefore suitable for architecture review, but it is not a complete deployable copy of the competition system.
