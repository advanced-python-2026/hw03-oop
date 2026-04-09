"""Тесты для задания 3.2 — дескрипторы атрибутов.

Каждый блок тестов автоматически пропускается, если дескриптор
не входит в вариант студента.
"""

import logging

import pytest

from hw03.descriptors import Cached, Logged, Observable, ReadOnly, Typed, Validated
from tests.conftest import VARIANT_DESCRIPTORS, get_variant

# ---------------------------------------------------------------------------
# Helper: skip if descriptor not in variant
# ---------------------------------------------------------------------------

_STUDENT_FILE = __import__("pathlib").Path(__file__).resolve().parent.parent / "STUDENT.md"


def _current_descriptor_names() -> tuple[str, str, str]:
    """Получить имена дескрипторов текущего варианта (без fixtures)."""
    try:
        text = _STUDENT_FILE.read_text(encoding="utf-8")
        name = ""
        for line in text.splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip()
                break
        if not name:
            return ("", "", "")
        v = get_variant(name, n_variants=6)
        return VARIANT_DESCRIPTORS[v]
    except Exception:
        return ("", "", "")


def _skip_unless(descriptor_name: str) -> pytest.MarkDecorator:
    """Пропустить тест, если дескриптор не в варианте студента."""
    names = _current_descriptor_names()
    return pytest.mark.skipif(
        descriptor_name not in names,
        reason=f"{descriptor_name} не входит в вариант студента ({names})",
    )


# ---------------------------------------------------------------------------
# Validated
# ---------------------------------------------------------------------------


@_skip_unless("Validated")
class TestValidated:
    """Тесты для дескриптора Validated."""

    def test_valid_value_accepted(self) -> None:
        class Config:
            port = Validated(int, min_value=1, max_value=65535)

        c = Config()
        c.port = 8080
        assert c.port == 8080

    def test_wrong_type_raises_type_error(self) -> None:
        class Config:
            port = Validated(int, min_value=1, max_value=65535)

        c = Config()
        with pytest.raises(TypeError):
            c.port = "not a number"

    def test_below_min_raises_value_error(self) -> None:
        class Config:
            port = Validated(int, min_value=1, max_value=65535)

        c = Config()
        with pytest.raises(ValueError):
            c.port = 0

    def test_above_max_raises_value_error(self) -> None:
        class Config:
            port = Validated(int, min_value=1, max_value=65535)

        c = Config()
        with pytest.raises(ValueError):
            c.port = 70000

    def test_boundary_values_accepted(self) -> None:
        class Config:
            port = Validated(int, min_value=1, max_value=65535)

        c = Config()
        c.port = 1
        assert c.port == 1
        c.port = 65535
        assert c.port == 65535

    def test_no_range_only_type_check(self) -> None:
        class Config:
            name = Validated(str)

        c = Config()
        c.name = "hello"
        assert c.name == "hello"
        with pytest.raises(TypeError):
            c.name = 123

    def test_access_before_set_raises_attribute_error(self) -> None:
        class Config:
            port = Validated(int, min_value=1, max_value=65535)

        c = Config()
        with pytest.raises(AttributeError):
            _ = c.port


# ---------------------------------------------------------------------------
# Logged
# ---------------------------------------------------------------------------


@_skip_unless("Logged")
class TestLogged:
    """Тесты для дескриптора Logged."""

    def test_set_logs_message(self, caplog: pytest.LogCaptureFixture) -> None:
        class Config:
            value = Logged()

        c = Config()
        with caplog.at_level(logging.DEBUG):
            c.value = 42

        assert any(
            "value" in record.message and "42" in record.message for record in caplog.records
        )

    def test_get_logs_message(self, caplog: pytest.LogCaptureFixture) -> None:
        class Config:
            value = Logged(default=10)

        c = Config()
        with caplog.at_level(logging.DEBUG):
            _ = c.value

        assert any("value" in record.message for record in caplog.records)

    def test_value_stored_correctly(self) -> None:
        class Config:
            value = Logged()

        c = Config()
        c.value = 99
        assert c.value == 99

    def test_multiple_sets_logged(self, caplog: pytest.LogCaptureFixture) -> None:
        class Config:
            value = Logged()

        c = Config()
        with caplog.at_level(logging.DEBUG):
            c.value = 1
            c.value = 2
            c.value = 3

        set_records = [r for r in caplog.records if "value" in r.message]
        assert len(set_records) >= 3


# ---------------------------------------------------------------------------
# Cached
# ---------------------------------------------------------------------------


@_skip_unless("Cached")
class TestCached:
    """Тесты для дескриптора Cached."""

    def test_first_access_computes(self) -> None:
        call_count = 0

        def factory():
            nonlocal call_count
            call_count += 1
            return 42

        class Config:
            value = Cached(factory)

        c = Config()
        result = c.value
        assert result == 42
        assert call_count == 1

    def test_second_access_uses_cache(self) -> None:
        call_count = 0

        def factory():
            nonlocal call_count
            call_count += 1
            return "computed"

        class Config:
            value = Cached(factory)

        c = Config()
        _ = c.value
        _ = c.value
        _ = c.value
        assert call_count == 1

    def test_different_instances_independent(self) -> None:
        def factory():
            return "shared_factory"

        class Config:
            value = Cached(factory)

        c1 = Config()
        c2 = Config()
        _ = c1.value
        _ = c2.value
        # Both should have the value
        assert c1.value == "shared_factory"
        assert c2.value == "shared_factory"

    def test_set_overrides_cache(self) -> None:
        def factory():
            return "original"

        class Config:
            value = Cached(factory)

        c = Config()
        assert c.value == "original"
        c.value = "overridden"
        assert c.value == "overridden"


# ---------------------------------------------------------------------------
# Typed
# ---------------------------------------------------------------------------


@_skip_unless("Typed")
class TestTyped:
    """Тесты для дескриптора Typed."""

    def test_correct_type_accepted(self) -> None:
        class Config:
            name = Typed(str)

        c = Config()
        c.name = "hello"
        assert c.name == "hello"

    def test_wrong_type_raises_type_error(self) -> None:
        class Config:
            name = Typed(str)

        c = Config()
        with pytest.raises(TypeError):
            c.name = 123

    def test_int_type(self) -> None:
        class Config:
            count = Typed(int)

        c = Config()
        c.count = 5
        assert c.count == 5
        with pytest.raises(TypeError):
            c.count = 5.0

    def test_multiple_typed_fields(self) -> None:
        class Config:
            name = Typed(str)
            age = Typed(int)

        c = Config()
        c.name = "Alice"
        c.age = 30
        assert c.name == "Alice"
        assert c.age == 30

    def test_none_raises_type_error(self) -> None:
        class Config:
            value = Typed(int)

        c = Config()
        with pytest.raises(TypeError):
            c.value = None

    def test_access_before_set_raises_attribute_error(self) -> None:
        class Config:
            name = Typed(str)

        c = Config()
        with pytest.raises(AttributeError):
            _ = c.name


# ---------------------------------------------------------------------------
# ReadOnly
# ---------------------------------------------------------------------------


@_skip_unless("ReadOnly")
class TestReadOnly:
    """Тесты для дескриптора ReadOnly."""

    def test_first_write_succeeds(self) -> None:
        class Config:
            value = ReadOnly()

        c = Config()
        c.value = 42
        assert c.value == 42

    def test_second_write_raises(self) -> None:
        class Config:
            value = ReadOnly()

        c = Config()
        c.value = 42
        with pytest.raises(AttributeError):
            c.value = 99

    def test_value_preserved_after_failed_write(self) -> None:
        class Config:
            value = ReadOnly()

        c = Config()
        c.value = "original"
        with pytest.raises(AttributeError):
            c.value = "changed"
        assert c.value == "original"

    def test_different_instances_independent(self) -> None:
        class Config:
            value = ReadOnly()

        c1 = Config()
        c2 = Config()
        c1.value = "first"
        c2.value = "second"
        assert c1.value == "first"
        assert c2.value == "second"

    def test_default_value(self) -> None:
        class Config:
            value = ReadOnly(default=0)

        c = Config()
        assert c.value == 0


# ---------------------------------------------------------------------------
# Observable
# ---------------------------------------------------------------------------


@_skip_unless("Observable")
class TestObservable:
    """Тесты для дескриптора Observable."""

    def test_callback_called_on_change(self) -> None:
        changes: list[tuple] = []

        class Config:
            value = Observable()

        c = Config()
        Config.value.add_observer(c, lambda name, old, new: changes.append((name, old, new)))
        c.value = 42
        assert len(changes) == 1
        assert changes[0][2] == 42

    def test_callback_receives_old_and_new(self) -> None:
        changes: list[tuple] = []

        class Config:
            value = Observable(default=0)

        c = Config()
        Config.value.add_observer(c, lambda name, old, new: changes.append((name, old, new)))
        c.value = 10
        c.value = 20
        assert changes[-1] == ("value", 10, 20)

    def test_multiple_observers(self) -> None:
        log1: list = []
        log2: list = []

        class Config:
            value = Observable()

        c = Config()
        Config.value.add_observer(c, lambda n, o, v: log1.append(v))
        Config.value.add_observer(c, lambda n, o, v: log2.append(v))
        c.value = 99
        assert 99 in log1
        assert 99 in log2

    def test_value_stored(self) -> None:
        class Config:
            value = Observable(default=0)

        c = Config()
        c.value = 5
        assert c.value == 5

    def test_access_before_set_raises_attribute_error(self) -> None:
        class Config:
            value = Observable()

        c = Config()
        with pytest.raises(AttributeError):
            _ = c.value

    def test_observer_per_instance(self) -> None:
        changes_1: list = []
        changes_2: list = []

        class Config:
            value = Observable()

        c1 = Config()
        c2 = Config()
        Config.value.add_observer(c1, lambda n, o, v: changes_1.append(v))
        Config.value.add_observer(c2, lambda n, o, v: changes_2.append(v))
        c1.value = 1
        c2.value = 2
        assert 1 in changes_1
        assert 1 not in changes_2
        assert 2 in changes_2
        assert 2 not in changes_1
