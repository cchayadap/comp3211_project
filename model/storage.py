"""Persistence to / from '.pim' files (US10, US11). JSON lines, stdlib only."""
import json
from .collection import PIMCollection
from .records import RECORD_TYPES


def _check_ext(path: str) -> None:
    if not path.lower().endswith(".pim"):
        raise ValueError("File name must end with '.pim'")


def save_pim(collection: PIMCollection, path: str) -> None:
    _check_ext(path)
    with open(path, "w", encoding="utf-8") as f:
        for pir in collection.all():
            f.write(json.dumps(pir.to_dict()) + "\n")


def load_pim(path: str) -> PIMCollection:
    """Load a .pim file into a NEW collection. Raises on bad content."""
    _check_ext(path)
    result = PIMCollection()
    seen = set()
    with open(path, "r", encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                if not isinstance(data, dict):
                    raise ValueError("expected a JSON object")
                cls = RECORD_TYPES[data.pop("type")]
                pir_id = data.pop("id")
                # bool is a subclass of int, so exclude it explicitly
                if type(pir_id) is not int or pir_id <= 0:
                    raise ValueError(f"invalid id {pir_id!r}")
                if pir_id in seen:
                    raise ValueError(f"duplicate id {pir_id}")
                seen.add(pir_id)
                result.add(cls(**data, pir_id=pir_id))
            except (ValueError, KeyError, TypeError) as e:
                raise ValueError(f"Corrupt .pim file at line {n}: {e}")
    return result
