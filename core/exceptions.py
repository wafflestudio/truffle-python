from dataclasses import dataclass
from enum import Enum
import traceback


@dataclass(frozen=True)
class _Element(Enum):
    class_name: str
    method_name: str
    line_number: int
    file_name: str
    is_in_app_include: bool


class ClassMethod:
    pass


@dataclass(frozen=True)
class TruffleException:
    class_name: str
    message: str
    elements: str  # Element 클래스 쓸 수 있나?

    @classmethod
    def of(cls, exc: Exception):
        return TruffleException(
            class_name=exc.__class__.__name__,
            message=str(exc),
            elements=''.join(traceback.TracebackException.from_exception(exc).format())
        )
