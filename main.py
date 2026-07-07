from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from xinkong_home.config import load_public_config
from xinkong_home.factory import build_public_demo_app
from xinkong_home.models import VoiceEvent


async def run_demo(config_path: Path) -> None:
    config = load_public_config(config_path)
    app = build_public_demo_app(config)

    demo_events = [
        "芯控家居，打开客厅灯",
        "芯控家居，看看前面有什么",
        "芯控家居，检测心率血氧",
        "芯控家居，明天天气如何",
        "芯控家居，系统健康度",
    ]

    for text in demo_events:
        print(f"\n[INPUT] {text}")
        outcomes = await app.handle_voice_event(VoiceEvent(text=text))
        for outcome in outcomes:
            print(f"[OUTCOME] {outcome.kind.value}: {outcome.message}")


async def run_service_skeleton(config_path: Path) -> None:
    config = load_public_config(config_path)
    _app = build_public_demo_app(config)

    # Production-only logic intentionally not published:
    # 1. Start local startup TTS immediately after boot.
    # 2. Start realtime ASR session and reconnect supervisor.
    # 3. Warm up local face recognition, RDK camera service, and BPU models.
    # 4. Listen for wake name and perform noisy-scene command gating.
    # 5. Convert audio turns into VoiceEvent objects and call app.handle_voice_event().
    # 6. Route high-risk device or system operations through confirmation.
    # 7. Run watchdog, dashboard, health snapshots, and recovery hooks.
    #
    # The public simulation uses run_demo() instead, so no private hardware,
    # model files, keys, or competition-tuned orchestration details are exposed.
    raise SystemExit("Use --demo in the public repository. Production service loop is redacted.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Xinkong Home public framework entry point")
    parser.add_argument("--config", default="config/config.example.yaml")
    parser.add_argument("--demo", action="store_true", help="Run the offline public simulation")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_path = Path(args.config)
    if args.demo:
        asyncio.run(run_demo(config_path))
    else:
        asyncio.run(run_service_skeleton(config_path))


if __name__ == "__main__":
    main()

