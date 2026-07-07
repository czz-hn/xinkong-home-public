from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by plain stdlib demos.
    yaml = None


@dataclass(frozen=True)
class PublicConfig:
    app_name: str = "Xinkong Home"
    wake_names: tuple[str, ...] = ("芯控家居", "芯控")
    demo_mode: bool = True
    raw: dict[str, Any] = field(default_factory=dict)


def load_public_config(path: str | Path = "config/config.example.yaml") -> PublicConfig:
    config_path = Path(path)
    if not config_path.exists():
        return PublicConfig()
    if yaml is None:
        return PublicConfig()

    data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    interaction = data.get("interaction", {}) if isinstance(data, dict) else {}
    app = data.get("app", {}) if isinstance(data, dict) else {}
    wake_names = tuple(interaction.get("wake_names") or ("芯控家居", "芯控"))

    return PublicConfig(
        app_name=str(app.get("name") or "Xinkong Home"),
        wake_names=wake_names,
        demo_mode=str(app.get("mode", "public-demo")) == "public-demo",
        raw=data,
    )
