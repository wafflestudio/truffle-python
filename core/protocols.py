from dataclasses import dataclass
from enum import Enum

from core.exceptions import TruffleException


class TruffleVersion(Enum):
    V1 = 0


@dataclass(frozen=True)
class TruffleApp:
    name: str
    phase: str = None


@dataclass(frozen=True)
class TruffleRuntime:
    name: str
    version: str


@dataclass(frozen=True)
class TruffleEvent:
    app: TruffleApp
    runtime: TruffleRuntime
    exception: TruffleException
    version: str = TruffleVersion.V1

