from __future__ import annotations

from dataclasses import dataclass

from .adapters import EdgeGateway, HealthGateway, HealthMonitor, SmartHomeGateway, VisionGateway, WeatherGateway
from .models import ExecutionOutcome, Intent, IntentKind, PlannedTask, RiskLevel, TaskKind
from .safety import SafetyPolicy


@dataclass
class RuntimeAdapters:
    smart_home: SmartHomeGateway
    edge: EdgeGateway
    vision: VisionGateway
    health: HealthGateway
    weather: WeatherGateway
    monitor: HealthMonitor


class TaskOrchestrator:
    """Coordinates intent planning, safety checks, and adapter dispatch.

    This is intentionally compact. The private version includes more complete
    multi-turn context, mixed command splitting, scene modes, fallback routing,
    and competition-specific recovery paths.
    """

    def __init__(self, adapters: RuntimeAdapters, safety: SafetyPolicy | None = None) -> None:
        self.adapters = adapters
        self.safety = safety or SafetyPolicy()

    def plan(self, intent: Intent) -> list[PlannedTask]:
        risk = self.safety.classify(intent)
        if self.safety.requires_confirmation(risk):
            return [
                PlannedTask(
                    kind=TaskKind.REPLY,
                    text="High-risk operation requires confirmation.",
                    target=intent.target,
                    action=intent.action,
                    risk=RiskLevel.HIGH,
                )
            ]

        if intent.kind == IntentKind.SMART_HOME:
            return [PlannedTask(TaskKind.SMART_HOME_CONTROL, intent.text, intent.target, intent.action, risk)]
        if intent.kind == IntentKind.VISION:
            return [PlannedTask(TaskKind.BPU_VISION_CHECK, intent.text, "camera", "inspect", risk)]
        if intent.kind == IntentKind.HEALTH:
            return [PlannedTask(TaskKind.HEALTH_QUERY, intent.text, "health", "query", risk)]
        if intent.kind == IntentKind.WEATHER:
            return [PlannedTask(TaskKind.WEATHER_QUERY, intent.text, "weather", "query", risk)]
        if intent.kind == IntentKind.SYSTEM:
            return [PlannedTask(TaskKind.SYSTEM_HEALTH, intent.text, "runtime", "health_check", risk)]

        return [PlannedTask(TaskKind.REPLY, intent.text, action="reply", risk=risk)]

    async def execute(self, task: PlannedTask) -> ExecutionOutcome:
        if task.kind == TaskKind.SMART_HOME_CONTROL:
            return await self.adapters.smart_home.control(task.target or "device", task.action or "toggle")

        if task.kind == TaskKind.BPU_VISION_CHECK:
            summary = await self.adapters.vision.inspect_scene()
            return ExecutionOutcome(
                kind=task.kind,
                success=summary.available,
                target="camera",
                action="inspect",
                message=f"BPU summary: {', '.join(summary.labels) or 'no labels'}",
                metadata={"backend": summary.backend, "latency_ms": summary.latency_ms},
            )

        if task.kind == TaskKind.HEALTH_QUERY:
            return await self.adapters.health.query(task.target or "health")

        if task.kind == TaskKind.WEATHER_QUERY:
            return await self.adapters.weather.query_weather(task.text)

        if task.kind == TaskKind.SYSTEM_HEALTH:
            checks = await self.adapters.monitor.checks()
            ok_count = sum(1 for check in checks if check.ok)
            return ExecutionOutcome(
                kind=task.kind,
                success=ok_count == len(checks),
                target="runtime",
                action="health_check",
                message=f"{ok_count}/{len(checks)} runtime checks healthy",
            )

        return ExecutionOutcome(
            kind=TaskKind.REPLY,
            success=True,
            action="reply",
            message="Public demo reply. Private dialog logic is not included.",
        )

