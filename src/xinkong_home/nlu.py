from __future__ import annotations

from .models import Intent, IntentKind


class IntentRouter:
    """Small public router.

    The private project contains richer Chinese normalization, noisy-scene
    command gating, mixed-intent splitting, and competition-tuned aliases.
    This public version keeps enough behavior to show the interface.
    """

    def route(self, text: str) -> Intent:
        normalized = text.strip()

        if any(word in normalized for word in ("状态", "自检", "健康度")):
            return Intent(IntentKind.SYSTEM, normalized, target="runtime", action="health_check")
        if any(word in normalized for word in ("天气", "气温", "下雨")):
            return Intent(IntentKind.WEATHER, normalized, action="query")
        if any(word in normalized for word in ("心率", "血氧", "握力", "健康")):
            return Intent(IntentKind.HEALTH, normalized, target="health", action="query")
        if any(word in normalized for word in ("摄像头", "看看", "识别", "前面")):
            return Intent(IntentKind.VISION, normalized, target="camera", action="inspect")
        if any(word in normalized for word in ("灯", "空调", "风扇", "开关")):
            action = "turn_on" if any(word in normalized for word in ("打开", "启动", "开")) else "turn_off"
            return Intent(IntentKind.SMART_HOME, normalized, target="device", action=action)
        return Intent(IntentKind.DIALOG, normalized, action="reply")
