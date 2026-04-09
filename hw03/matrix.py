"""Модуль с классом Matrix для задания 3.1."""

from __future__ import annotations

import contextlib
from typing import Self


class Matrix:
    """Класс матрицы с поддержкой арифметики, хеширования и форматирования.

    Примеры использования:
        >>> m = Matrix([[1, 2], [3, 4]])
        >>> m + Matrix([[5, 6], [7, 8]])
        Matrix([[6, 8], [10, 12]])

    TODO: Реализовать следующие методы:
    - __init__(self, data): инициализация из вложенного списка
    - __add__, __sub__: поэлементное сложение/вычитание
    - __mul__: умножение на скаляр
    - __matmul__: матричное умножение
    - __eq__: сравнение матриц
    - __hash__: хеширование (матрица должна быть hashable)
    - __repr__: строковое представление в виде Python-выражения
    - __str__: читаемое табличное представление
    - __format__: форматирование с указанием точности (например, f"{m:.2f}")
    - from_file(path): classmethod/contextmanager для чтения матрицы из файла
    """

    def __init__(self, data: list[list[float]]) -> None:
        # TODO: сохранить данные, проверить прямоугольность
        raise NotImplementedError

    @property
    def rows(self) -> int:
        # TODO
        raise NotImplementedError

    @property
    def cols(self) -> int:
        # TODO
        raise NotImplementedError

    def __add__(self, other: Self) -> Self:
        # TODO
        raise NotImplementedError

    def __sub__(self, other: Self) -> Self:
        # TODO
        raise NotImplementedError

    def __mul__(self, scalar: int | float) -> Self:
        # TODO
        raise NotImplementedError

    def __rmul__(self, scalar: int | float) -> Self:
        # TODO: поддержка записи вида 3 * matrix
        return self.__mul__(scalar)

    def __matmul__(self, other: Self) -> Self:
        # TODO
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        # TODO
        raise NotImplementedError

    def __hash__(self) -> int:
        # TODO
        raise NotImplementedError

    def __repr__(self) -> str:
        # TODO: вернуть строку вида Matrix([[1, 2], [3, 4]])
        raise NotImplementedError

    def __str__(self) -> str:
        # TODO: вернуть читаемую таблицу
        raise NotImplementedError

    def __format__(self, format_spec: str) -> str:
        # TODO: форматирование элементов с указанной точностью
        raise NotImplementedError

    @classmethod
    def from_file(cls, path: str) -> contextlib.AbstractContextManager[Matrix]:
        """Контекстный менеджер для чтения матрицы из файла.

        Использование::

            with Matrix.from_file("data.txt") as m:
                print(m)

        Формат файла: строки матрицы, элементы через пробел.

        TODO: реализовать чтение из файла.
        Подсказка: можно использовать contextlib.contextmanager
        или вернуть объект, поддерживающий протокол контекстного менеджера.
        """
        raise NotImplementedError
