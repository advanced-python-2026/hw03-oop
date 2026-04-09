import hashlib
import re
from pathlib import Path

import pytest

STUDENT_FILE = Path(__file__).resolve().parent.parent / "STUDENT.md"
HW_NUMBER = 3
SEMESTER = "2026-spring"

VARIANT_DESCRIPTORS = {
    0: ("Validated", "Logged", "Cached"),
    1: ("Typed", "ReadOnly", "Observable"),
    2: ("Validated", "Cached", "ReadOnly"),
    3: ("Logged", "Typed", "Observable"),
    4: ("Validated", "Observable", "Typed"),
    5: ("Cached", "ReadOnly", "Logged"),
}


def _read_student_name() -> str:
    text = STUDENT_FILE.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
            if name == "Фамилия Имя Отчество":
                raise RuntimeError("Заполни своё ФИО в STUDENT.md (поле 'name:')")
            return name
    raise RuntimeError("Не найдено поле 'name:' в STUDENT.md")


def _normalize(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def get_variant(name: str, n_variants: int, hw: int = HW_NUMBER) -> int:
    key = f"{_normalize(name)}:hw{hw}:{SEMESTER}"
    h = hashlib.sha256(key.encode()).hexdigest()
    return int(h[:8], 16) % n_variants


@pytest.fixture
def student_name() -> str:
    return _read_student_name()


@pytest.fixture
def variant(student_name: str) -> int:
    return get_variant(student_name, n_variants=6)


@pytest.fixture
def descriptor_names(variant: int) -> tuple[str, str, str]:
    """Возвращает кортеж из трёх имён дескрипторов для варианта студента."""
    return VARIANT_DESCRIPTORS[variant]
