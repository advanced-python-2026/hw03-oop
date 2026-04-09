"""Тесты для задания 3.1 — класс Matrix."""

import pytest

from hw03.matrix import Matrix

# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestMatrixConstruction:
    def test_create_from_nested_list(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        assert m.rows == 2
        assert m.cols == 2

    def test_create_single_element(self) -> None:
        m = Matrix([[42]])
        assert m.rows == 1
        assert m.cols == 1

    def test_create_rectangular(self) -> None:
        m = Matrix([[1, 2, 3], [4, 5, 6]])
        assert m.rows == 2
        assert m.cols == 3


# ---------------------------------------------------------------------------
# Addition
# ---------------------------------------------------------------------------


class TestMatrixAdd:
    def test_add_correct_result(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        result = a + b
        assert result == Matrix([[6, 8], [10, 12]])

    def test_add_identity(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        zero = Matrix([[0, 0], [0, 0]])
        assert a + zero == a

    def test_add_dimension_mismatch_raises(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2, 3]])
        with pytest.raises(ValueError):
            _ = a + b


# ---------------------------------------------------------------------------
# Subtraction
# ---------------------------------------------------------------------------


class TestMatrixSub:
    def test_sub_correct_result(self) -> None:
        a = Matrix([[5, 6], [7, 8]])
        b = Matrix([[1, 2], [3, 4]])
        result = a - b
        assert result == Matrix([[4, 4], [4, 4]])

    def test_sub_self_is_zero(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        result = a - a
        assert result == Matrix([[0, 0], [0, 0]])

    def test_sub_dimension_mismatch_raises(self) -> None:
        a = Matrix([[1, 2]])
        b = Matrix([[1], [2]])
        with pytest.raises(ValueError):
            _ = a - b


# ---------------------------------------------------------------------------
# Scalar multiplication
# ---------------------------------------------------------------------------


class TestMatrixMul:
    def test_mul_scalar_int(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        result = m * 3
        assert result == Matrix([[3, 6], [9, 12]])

    def test_mul_scalar_float(self) -> None:
        m = Matrix([[2, 4], [6, 8]])
        result = m * 0.5
        assert result == Matrix([[1.0, 2.0], [3.0, 4.0]])

    def test_mul_scalar_zero(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        result = m * 0
        assert result == Matrix([[0, 0], [0, 0]])

    def test_rmul_scalar(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        result = 3 * m
        assert result == Matrix([[3, 6], [9, 12]])


# ---------------------------------------------------------------------------
# Matrix multiplication (@)
# ---------------------------------------------------------------------------


class TestMatrixMatmul:
    def test_matmul_square(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        result = a @ b
        assert result == Matrix([[19, 22], [43, 50]])

    def test_matmul_rectangular(self) -> None:
        a = Matrix([[1, 2, 3]])
        b = Matrix([[4], [5], [6]])
        result = a @ b
        assert result == Matrix([[32]])

    def test_matmul_identity(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        identity = Matrix([[1, 0], [0, 1]])
        assert a @ identity == a

    def test_matmul_dimension_mismatch_raises(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2, 3]])
        with pytest.raises(ValueError):
            _ = a @ b


# ---------------------------------------------------------------------------
# Equality
# ---------------------------------------------------------------------------


class TestMatrixEq:
    def test_equal_matrices(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 4]])
        assert a == b

    def test_unequal_matrices(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 5]])
        assert a != b

    def test_different_dimensions_not_equal(self) -> None:
        a = Matrix([[1, 2]])
        b = Matrix([[1], [2]])
        assert a != b

    def test_not_equal_to_non_matrix(self) -> None:
        m = Matrix([[1, 2]])
        assert m != [[1, 2]]


# ---------------------------------------------------------------------------
# Hash
# ---------------------------------------------------------------------------


class TestMatrixHash:
    def test_equal_matrices_same_hash(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 4]])
        assert hash(a) == hash(b)

    def test_usable_in_set(self) -> None:
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2], [3, 4]])
        c = Matrix([[5, 6], [7, 8]])
        s = {a, b, c}
        assert len(s) == 2

    def test_usable_as_dict_key(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        d = {m: "hello"}
        assert d[Matrix([[1, 2], [3, 4]])] == "hello"


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------


class TestMatrixRepr:
    def test_repr_valid_python(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        r = repr(m)
        assert r.startswith("Matrix(")
        assert "[[" in r

    def test_repr_roundtrip(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        reconstructed = eval(repr(m))  # noqa: S307
        assert reconstructed == m


# ---------------------------------------------------------------------------
# __str__
# ---------------------------------------------------------------------------


class TestMatrixStr:
    def test_str_readable(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        s = str(m)
        assert isinstance(s, str)
        assert len(s) > 0
        # Should contain the numbers
        assert "1" in s
        assert "4" in s

    def test_str_differs_from_repr(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        assert str(m) != repr(m)


# ---------------------------------------------------------------------------
# __format__
# ---------------------------------------------------------------------------


class TestMatrixFormat:
    def test_format_precision(self) -> None:
        m = Matrix([[1.123456, 2.654321], [3.0, 4.0]])
        result = f"{m:.2f}"
        assert "1.12" in result
        assert "2.65" in result

    def test_format_no_spec(self) -> None:
        m = Matrix([[1, 2], [3, 4]])
        result = format(m)
        assert isinstance(result, str)
        assert len(result) > 0


# ---------------------------------------------------------------------------
# from_file (context manager)
# ---------------------------------------------------------------------------


class TestMatrixFromFile:
    def test_from_file_reads_correctly(self, tmp_path) -> None:
        p = tmp_path / "matrix.txt"
        p.write_text("1 2 3\n4 5 6\n")
        with Matrix.from_file(str(p)) as m:
            assert m == Matrix([[1, 2, 3], [4, 5, 6]])

    def test_from_file_single_row(self, tmp_path) -> None:
        p = tmp_path / "matrix.txt"
        p.write_text("10 20 30\n")
        with Matrix.from_file(str(p)) as m:
            assert m == Matrix([[10, 20, 30]])

    def test_from_file_float_values(self, tmp_path) -> None:
        p = tmp_path / "matrix.txt"
        p.write_text("1.5 2.5\n3.5 4.5\n")
        with Matrix.from_file(str(p)) as m:
            assert m == Matrix([[1.5, 2.5], [3.5, 4.5]])

    def test_from_file_missing_raises(self) -> None:
        with pytest.raises((FileNotFoundError, OSError)):
            with Matrix.from_file("/nonexistent/path/matrix.txt") as _:
                pass
