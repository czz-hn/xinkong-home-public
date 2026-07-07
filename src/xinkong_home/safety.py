from __future__ import annotations

from .models import Intent, RiskLevel


class SafetyPolicy:
    """Public safety boundary.

    The private project contains complete risk scene fusion and recovery rules.
    Here we only expose the decision shape, not the field-tuned policy details.
    """

    _HIGH_RISK_WORDS = ("关机", "重启", "删除", "格式化")

    def classify(self, intent: Intent) -> RiskLevel:
        if any(word in intent.text for word in self._HIGH_RISK_WORDS):
            return RiskLevel.HIGH
        if intent.kind.value in {"smart_home", "local_edge"}:
            return RiskLevel.LOW
        return RiskLevel.NONE

    def requires_confirmation(self, risk: RiskLevel) -> bool:
        return risk == RiskLevel.HIGH
