from __future__ import annotations

from typing import Protocol

from .models import BpuDetectionSummary, ExecutionOutcome, RuntimeHealth, TaskKind


class SpeechSynthesizer(Protocol):
    async def speak(self, text: str) -> None:
        ...


class SmartHomeGateway(Protocol):
    async def control(self, target: str, action: str) -> ExecutionOutcome:
        ...


class EdgeGateway(Protocol):
    async def run_action(self, action: str, target: str | None = None) -> ExecutionOutcome:
        ...


class VisionGateway(Protocol):
    async def inspect_scene(self) -> BpuDetectionSummary:
        ...


class HealthGateway(Protocol):
    async def query(self, metric: str) -> ExecutionOutcome:
        ...


class WeatherGateway(Protocol):
    async def query_weather(self, text: str) -> ExecutionOutcome:
        ...


class HealthMonitor(Protocol):
    async def checks(self) -> list[RuntimeHealth]:
        ...


class ConsoleSpeechSynthesizer:
    async def speak(self, text: str) -> None:
        print(f"[TTS] {text}")


class SimulatedSmartHomeGateway:
    async def control(self, target: str, action: str) -> ExecutionOutcome:
        return ExecutionOutcome(
            kind=TaskKind.SMART_HOME_CONTROL,
            success=True,
            target=target,
            action=action,
            message=f"Simulated smart-home action: {action} {target}",
        )


class SimulatedEdgeGateway:
    async def run_action(self, action: str, target: str | None = None) -> ExecutionOutcome:
        return ExecutionOutcome(
            kind=TaskKind.EDGE_ACTION,
            success=True,
            target=target,
            action=action,
            message="Simulated edge gateway action accepted",
        )


class SimulatedVisionGateway:
    async def inspect_scene(self) -> BpuDetectionSummary:
        return BpuDetectionSummary(
            available=True,
            backend="rdk-x5-bpu-simulation",
            labels=("person", "indoor"),
            latency_ms=18.5,
            note="Public version does not include model files or inference code.",
        )


class SimulatedHealthGateway:
    async def query(self, metric: str) -> ExecutionOutcome:
        return ExecutionOutcome(
            kind=TaskKind.HEALTH_QUERY,
            success=True,
            target=metric,
            action="query",
            message=f"Simulated {metric} reading is available",
        )


class SimulatedWeatherGateway:
    async def query_weather(self, text: str) -> ExecutionOutcome:
        return ExecutionOutcome(
            kind=TaskKind.WEATHER_QUERY,
            success=True,
            target="auto-location",
            action="query",
            message="Simulated weather: clear, suitable for demo",
        )


class SimulatedHealthMonitor:
    async def checks(self) -> list[RuntimeHealth]:
        return [
            RuntimeHealth("voice-service", True, "simulation online"),
            RuntimeHealth("home-assistant", True, "simulation online"),
            RuntimeHealth("bpu-vision", True, "simulation online"),
        ]

