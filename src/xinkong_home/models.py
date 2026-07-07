from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class IntentKind(str, Enum):
    DIALOG = "dialog"
    SMART_HOME = "smart_home"
    LOCAL_EDGE = "local_edge"
    VISION = "vision"
    HEALTH = "health"
    WEATHER = "weather"
    SYSTEM = "system"


class TaskKind(str, Enum):
    REPLY = "reply"
    SMART_HOME_CONTROL = "smart_home_control"
    EDGE_ACTION = "edge_action"
    BPU_VISION_CHECK = "bpu_vision_check"
    HEALTH_QUERY = "health_query"
    WEATHER_QUERY = "weather_query"
    SYSTEM_HEALTH = "system_health"


class RiskLevel(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class VoiceEvent:
    text: str
    source: str = "demo"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Intent:
    kind: IntentKind
    text: str
    target: str | None = None
    action: str | None = None
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlannedTask:
    kind: TaskKind
    text: str
    target: str | None = None
    action: str | None = None
    risk: RiskLevel = RiskLevel.NONE
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExecutionOutcome:
    kind: TaskKind
    success: bool
    target: str | None = None
    action: str | None = None
    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class BpuDetectionSummary:
    available: bool
    backend: str
    labels: tuple[str, ...] = ()
    latency_ms: float | None = None
    note: str = ""


@dataclass(frozen=True)
class RuntimeHealth:
    service: str
    ok: bool
    detail: str

