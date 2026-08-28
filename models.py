from dataclasses import dataclass, field
from typing import Any


@dataclass
class GameEntry:
    name: str
    path: str
    size: int = 0
    last_save: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GameEntry":
        return cls(
            name=data["game"],
            path=data["path"],
            size=int(data.get("size", 0)),
            last_save=str(data.get("last_save", "")),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "game": self.name,
            "path": self.path,
            "size": self.size,
            "last_save": self.last_save,
        }


@dataclass
class AppSettings:
    user_location: str
    destination_location: str
    mode: str = "collect"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AppSettings":
        return cls(
            user_location=data["user_location"],
            destination_location=data["destination_location"],
            mode=data.get("mode", "collect"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_location": self.user_location,
            "destination_location": self.destination_location,
            "mode": self.mode,
        }


@dataclass
class OperationResult:
    game_name: str
    success: bool
    message: str
    source: str = ""
    destination: str = ""


@dataclass
class BackupReport:
    results: list[OperationResult] = field(default_factory=list)

    @property
    def successes(self) -> list[OperationResult]:
        return [result for result in self.results if result.success]

    @property
    def failures(self) -> list[OperationResult]:
        return [result for result in self.results if not result.success]
