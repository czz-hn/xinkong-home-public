from __future__ import annotations

from .adapters import (
    ConsoleSpeechSynthesizer,
    SimulatedEdgeGateway,
    SimulatedHealthGateway,
    SimulatedHealthMonitor,
    SimulatedSmartHomeGateway,
    SimulatedVisionGateway,
    SimulatedWeatherGateway,
)
from .app import XinkongHomeApp
from .config import PublicConfig
from .nlu import IntentRouter
from .orchestrator import RuntimeAdapters, TaskOrchestrator


def build_public_demo_app(config: PublicConfig) -> XinkongHomeApp:
    adapters = RuntimeAdapters(
        smart_home=SimulatedSmartHomeGateway(),
        edge=SimulatedEdgeGateway(),
        vision=SimulatedVisionGateway(),
        health=SimulatedHealthGateway(),
        weather=SimulatedWeatherGateway(),
        monitor=SimulatedHealthMonitor(),
    )
    return XinkongHomeApp(
        config=config,
        intent_router=IntentRouter(),
        orchestrator=TaskOrchestrator(adapters),
        speech=ConsoleSpeechSynthesizer(),
    )

