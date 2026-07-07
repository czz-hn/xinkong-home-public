from __future__ import annotations

import asyncio
import unittest

from xinkong_home.config import PublicConfig
from xinkong_home.factory import build_public_demo_app
from xinkong_home.models import TaskKind, VoiceEvent
from xinkong_home.nlu import IntentRouter


class PublicSkeletonTest(unittest.TestCase):
    def test_router_maps_weather_query(self) -> None:
        intent = IntentRouter().route("明天天气如何")
        self.assertEqual(intent.kind.value, "weather")
        self.assertEqual(intent.action, "query")

    def test_router_prioritizes_system_health(self) -> None:
        intent = IntentRouter().route("系统健康度")
        self.assertEqual(intent.kind.value, "system")
        self.assertEqual(intent.action, "health_check")

    def test_public_app_handles_smart_home_command(self) -> None:
        app = build_public_demo_app(PublicConfig())
        outcomes = asyncio.run(app.handle_voice_event(VoiceEvent(text="芯控家居，打开客厅灯")))
        self.assertEqual(outcomes[0].kind, TaskKind.SMART_HOME_CONTROL)
        self.assertTrue(outcomes[0].success)

    def test_public_app_rejects_command_without_wake_name(self) -> None:
        app = build_public_demo_app(PublicConfig())
        outcomes = asyncio.run(app.handle_voice_event(VoiceEvent(text="打开客厅灯")))
        self.assertFalse(outcomes[0].success)
        self.assertIn("Wake name", outcomes[0].message)


if __name__ == "__main__":
    unittest.main()
