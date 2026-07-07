from __future__ import annotations

from dataclasses import dataclass

from .adapters import SpeechSynthesizer
from .config import PublicConfig
from .models import ExecutionOutcome, TaskKind, VoiceEvent
from .nlu import IntentRouter
from .orchestrator import TaskOrchestrator


@dataclass
class XinkongHomeApp:
    config: PublicConfig
    intent_router: IntentRouter
    orchestrator: TaskOrchestrator
    speech: SpeechSynthesizer

    async def handle_voice_event(self, event: VoiceEvent) -> list[ExecutionOutcome]:
        if not self._passes_public_wake_gate(event.text):
            outcome = ExecutionOutcome(
                kind=TaskKind.REPLY,
                success=False,
                message="Wake name not detected in public demo.",
            )
            return [outcome]

        command = self._remove_wake_name(event.text)
        intent = self.intent_router.route(command)
        tasks = self.orchestrator.plan(intent)

        outcomes: list[ExecutionOutcome] = []
        for task in tasks:
            outcome = await self.orchestrator.execute(task)
            outcomes.append(outcome)

        reply = self._assemble_public_reply(outcomes)
        await self.speech.speak(reply)
        return outcomes

    def _passes_public_wake_gate(self, text: str) -> bool:
        return any(name in text for name in self.config.wake_names)

    def _remove_wake_name(self, text: str) -> str:
        command = text
        for name in self.config.wake_names:
            command = command.replace(name, "", 1)
        return command.strip(" ，,")

    def _assemble_public_reply(self, outcomes: list[ExecutionOutcome]) -> str:
        if not outcomes:
            return "未识别到可执行任务"
        if all(outcome.success for outcome in outcomes):
            return outcomes[-1].message or "已处理"
        return "部分任务未完成，请查看系统状态"
