from typing import Optional
from datetime import datetime
import uuid


class StudentRepository:

    def __init__(self):
        self._store: dict = {}

    def create(self, data: dict) -> dict:
        student_id = str(uuid.uuid4())[:8]
        record = {"id": student_id, "created_at": datetime.now().isoformat(), **data}
        self._store[student_id] = record
        return record

    def get(self, student_id: str) -> Optional[dict]:
        return self._store.get(student_id)

    def get_all(self) -> list[dict]:
        return list(self._store.values())

    def update(self, student_id: str, data: dict) -> Optional[dict]:
        if student_id not in self._store:
            return None
        self._store[student_id].update(data)
        return self._store[student_id]

    def delete(self, student_id: str) -> bool:
        if student_id not in self._store:
            return False
        del self._store[student_id]
        return True

    def count(self) -> int:
        return len(self._store)

    def filter_by_risk(self, risk_label: str) -> list[dict]:
        return [s for s in self._store.values() if s.get("predicted_risk") == risk_label]


student_repo = StudentRepository()
