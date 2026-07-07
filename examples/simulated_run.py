from __future__ import annotations

import asyncio

from xinkong_home.config import load_public_config
from xinkong_home.factory import build_public_demo_app
from xinkong_home.models import VoiceEvent


async def main() -> None:
    app = build_public_demo_app(load_public_config())
    await app.handle_voice_event(VoiceEvent(text="芯控家居，打开灯"))


if __name__ == "__main__":
    asyncio.run(main())

