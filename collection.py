"""PIMCollection: holds all PIRs (US1, US6, US8, US9, US7 search)."""
from .records import PIR, RECORD_TYPES


class PIMCollection:
    def __init__(self):
        self._records: dict = {}

    def add(self, pir: PIR) -> PIR:
        self._records[pir.id] = pir
        return pir

    def create(self, type_name: str, *args) -> PIR:
        cls = RECORD_TYPES.get(type_name.lower())
        if cls is None:
            raise ValueError(f"Unknown PIR type '{type_name}'")
        return self.add(cls(*args))

    def get(self, pir_id: int) -> PIR:
        if pir_id not in self._records:
            raise KeyError(f"No PIR with id {pir_id}")
        return self._records[pir_id]

    def modify(self, pir_id: int, field: str, value: str) -> PIR:
        pir = self.get(pir_id)
        pir.set(field, value)
        return pir

    def delete(self, pir_id: int) -> None:
        self.get(pir_id)
        del self._records[pir_id]

    def all(self) -> list:
        return [self._records[k] for k in sorted(self._records)]

    def search(self, criterion) -> list:
        return [p for p in self.all() if criterion.matches(p)]

    def clear(self) -> None:
        self._records.clear()

    def __len__(self):
        return len(self._records)
