"""Демонстрация хеширования и коллизий для задания 3.3.

TODO: Реализовать следующее:

1. Создать несколько объектов Matrix и поместить их в set и dict.
   Показать, что равные матрицы дают одинаковый hash, а разные — могут
   иметь разный (но не обязательно).

2. Создать умышленную коллизию хешей:
   - Две РАЗНЫЕ матрицы (m1 != m2), у которых hash(m1) == hash(m2).
   - Показать, что Python корректно различает их в set/dict,
     несмотря на одинаковый hash.

3. Объяснить в комментариях/docstring:
   - Почему hash и __eq__ должны быть согласованы.
   - Как Python разрешает коллизии в set/dict.
   - Какая сложность поиска при наличии коллизий.

Подсказка: для создания коллизии можно переопределить __hash__
в подклассе Matrix или подобрать данные, дающие одинаковый hash
при вашей реализации.
"""

from hw03.matrix import Matrix


def demonstrate_set_dict() -> dict:
    """Демонстрация использования Matrix в set и dict.

    Returns:
        dict с ключами:
        - "matrices_in_set": set из Matrix объектов
        - "matrix_dict": dict с Matrix ключами

    TODO: реализовать
    """
    raise NotImplementedError


def demonstrate_collision() -> tuple[Matrix, Matrix]:
    """Демонстрация коллизии хешей.

    Returns:
        Кортеж из двух матриц (m1, m2), где:
        - m1 != m2 (разные матрицы)
        - hash(m1) == hash(m2) (одинаковый хеш)

    TODO: реализовать
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("=== Демонстрация Matrix в set/dict ===")
    result = demonstrate_set_dict()
    print(f"Матрицы в set: {result['matrices_in_set']}")
    print(f"Matrix dict: {result['matrix_dict']}")

    print("\n=== Демонстрация коллизии хешей ===")
    m1, m2 = demonstrate_collision()
    print(f"m1 = {m1!r}")
    print(f"m2 = {m2!r}")
    print(f"m1 == m2: {m1 == m2}")
    print(f"hash(m1) == hash(m2): {hash(m1) == hash(m2)}")
    print(f"Обе в set: { {m1, m2} }")
