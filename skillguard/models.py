"""Small data models used by SkillGuard."""

from dataclasses import asdict, dataclass


@dataclass
class Finding:
    """A single scanner observation."""

    code: str
    severity: str
    message: str
    file: str
    line: int | None = None

    def to_dict(self) -> dict:
        return asdict(self)
