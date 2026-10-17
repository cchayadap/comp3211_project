"""PIR classes: Note (US2), Task (US3), Event (US4), Contact (US5)."""
from abc import ABC, abstractmethod
from datetime import datetime

TIME_FORMAT = "%Y-%m-%d %H:%M"


def parse_time(text: str) -> datetime:
    """Parse 'YYYY-MM-DD HH:MM'. Raises ValueError if malformed."""
    try:
        return datetime.strptime(text.strip(), TIME_FORMAT)
    except ValueError:
        raise ValueError(f"Invalid time '{text}'; expected YYYY-MM-DD HH:MM")


def format_time(value: datetime) -> str:
    return value.strftime(TIME_FORMAT)


def check_text(value) -> str:
    """Return value unchanged if it is non-blank text. Raises ValueError otherwise."""
    if not isinstance(value, str):
        raise ValueError(f"Text value must be a string, got {value!r}")
    if not value.strip():
        raise ValueError("Text value must not be blank")
    return value


def to_time(value) -> datetime:
    """Accept a datetime or a 'YYYY-MM-DD HH:MM' string. Raises ValueError otherwise."""
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return parse_time(value)
    raise ValueError(f"Time value must be a string, got {value!r}")


class PIR(ABC):
    """Base class of all personal information records."""
    TYPE = "pir"
    # field name -> "text" | "time"
    FIELDS: dict = {}

    _next_id = 1

    def __init__(self, pir_id: int = None):
        if pir_id is None:
            pir_id = PIR._next_id
        PIR._next_id = max(PIR._next_id, pir_id + 1)
        self.id = pir_id

    # --- generic field access (used by modify, search, storage) ---
    def get(self, field: str):
        if field not in self.FIELDS:
            raise KeyError(f"{self.TYPE} has no field '{field}'")
        return getattr(self, field)

    def set(self, field: str, value: str) -> None:
        kind = self.FIELDS.get(field)
        if kind is None:
            raise KeyError(f"{self.TYPE} has no field '{field}'")
        setattr(self, field, to_time(value) if kind == "time" else check_text(value))

    def text_fields(self):
        return [self.get(f) for f, k in self.FIELDS.items() if k == "text"]

    def time_fields(self):
        return [self.get(f) for f, k in self.FIELDS.items() if k == "time"]

    def to_dict(self) -> dict:
        data = {"type": self.TYPE, "id": self.id}
        for f, k in self.FIELDS.items():
            v = self.get(f)
            data[f] = format_time(v) if k == "time" else v
        return data

    @abstractmethod
    def __str__(self) -> str: ...


class Note(PIR):
    TYPE = "note"
    FIELDS = {"text": "text"}

    def __init__(self, text: str, pir_id: int = None):
        self.text = check_text(text)
        super().__init__(pir_id)

    def __str__(self):
        return f"[{self.id}] Note: {self.text}"


class Task(PIR):
    TYPE = "task"
    FIELDS = {"description": "text", "deadline": "time"}

    def __init__(self, description: str, deadline, pir_id: int = None):
        self.description = check_text(description)
        self.deadline = to_time(deadline)
        super().__init__(pir_id)

    def __str__(self):
        return (f"[{self.id}] Task: {self.description} "
                f"(deadline {format_time(self.deadline)})")


class Event(PIR):
    TYPE = "event"
    FIELDS = {"description": "text", "start": "time", "alarm": "time"}

    def __init__(self, description: str, start, alarm, pir_id: int = None):
        self.description = check_text(description)
        self.start = to_time(start)
        self.alarm = to_time(alarm)
        super().__init__(pir_id)

    def __str__(self):
        return (f"[{self.id}] Event: {self.description} "
                f"(start {format_time(self.start)}, alarm {format_time(self.alarm)})")


class Contact(PIR):
    TYPE = "contact"
    FIELDS = {"name": "text", "address": "text", "mobile": "text"}

    def __init__(self, name: str, address: str, mobile: str, pir_id: int = None):
        self.name = check_text(name)
        self.address = check_text(address)
        self.mobile = check_text(mobile)
        super().__init__(pir_id)

    def __str__(self):
        return (f"[{self.id}] Contact: {self.name}, {self.address}, "
                f"mobile {self.mobile}")


RECORD_TYPES = {c.TYPE: c for c in (Note, Task, Event, Contact)}
