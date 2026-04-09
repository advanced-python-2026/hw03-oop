"""Тесты для задания 3.3 — хеширование и коллизии."""

from hw03.collision_demo import demonstrate_collision, demonstrate_set_dict
from hw03.matrix import Matrix


class TestDemonstrateSetDict:
    """Тесты для demonstrate_set_dict."""

    def test_returns_dict_with_required_keys(self) -> None:
        result = demonstrate_set_dict()
        assert isinstance(result, dict)
        assert "matrices_in_set" in result
        assert "matrix_dict" in result

    def test_matrices_in_set_is_set(self) -> None:
        result = demonstrate_set_dict()
        assert isinstance(result["matrices_in_set"], set)

    def test_set_contains_matrices(self) -> None:
        result = demonstrate_set_dict()
        s = result["matrices_in_set"]
        assert len(s) >= 1
        for item in s:
            assert isinstance(item, Matrix)

    def test_dict_has_matrix_keys(self) -> None:
        result = demonstrate_set_dict()
        d = result["matrix_dict"]
        assert isinstance(d, dict)
        assert len(d) >= 1
        for key in d:
            assert isinstance(key, Matrix)

    def test_two_different_matrices_in_set(self) -> None:
        result = demonstrate_set_dict()
        s = result["matrices_in_set"]
        assert len(s) >= 2, "Множество должно содержать хотя бы 2 разные матрицы"


class TestDemonstrateCollision:
    """Тесты для demonstrate_collision."""

    def test_returns_two_matrices(self) -> None:
        m1, m2 = demonstrate_collision()
        assert isinstance(m1, Matrix)
        assert isinstance(m2, Matrix)

    def test_matrices_not_equal(self) -> None:
        m1, m2 = demonstrate_collision()
        assert m1 != m2, "Матрицы должны быть различными"

    def test_hashes_are_equal(self) -> None:
        m1, m2 = demonstrate_collision()
        assert hash(m1) == hash(m2), "Хеши должны совпадать (коллизия)"

    def test_collision_handled_in_set(self) -> None:
        m1, m2 = demonstrate_collision()
        s = {m1, m2}
        assert len(s) == 2, "Python должен различить матрицы с одинаковым хешем в set"

    def test_collision_handled_in_dict(self) -> None:
        m1, m2 = demonstrate_collision()
        d = {m1: "first", m2: "second"}
        assert len(d) == 2
        assert d[m1] == "first"
        assert d[m2] == "second"


class TestCollisionDemoRunnable:
    """Проверка, что collision_demo.py запускается без ошибок."""

    def test_demonstrate_set_dict_no_error(self) -> None:
        result = demonstrate_set_dict()
        assert result is not None

    def test_demonstrate_collision_no_error(self) -> None:
        result = demonstrate_collision()
        assert result is not None
        assert len(result) == 2
