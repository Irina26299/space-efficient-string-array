from __future__ import annotations

from typing import Iterator, List, Sequence


class SpaceEfficientStringArray(Sequence[str]):
    """
    Stores many strings inside a single concatenated buffer, tracking only
    element boundaries as integer offsets.

    Design rationale
    ----------------
    A normal Python list keeps one ``str`` object per element, and every
    ``str`` object carries its own header, hash cache, and length field.
    When the data is large, numerous, and read-mostly (for example a
    snapshot of identifiers captured at startup and iterated many times
    thereafter), that per-object overhead dominates memory.

    This class concatenates every element into one ``str`` (``_buffer``)
    and records the cumulative end position of each element in a single
    ``list`` of integers (``_ends``). ``_ends[i]`` is the exclusive end
    offset of element ``i``, and element ``i`` spans
    ``(_ends[i-1], _ends[i]]``.

    The trade-off: iteration and indexed access cost an O(1) slice of the
    buffer plus a list lookup, but the aggregate memory is
    ``len(buffer) + len(ends) * 8`` bytes for the bookkeeping, versus one
    full ``str`` object per element in a plain list. Element-level
    mutation is not supported; build a new array instead.
    """

    __slots__ = ("_buffer", "_ends")

    def __init__(self, strings: Sequence[str]) -> None:
        self._buffer: str = ""
        self._ends: List[int] = []
        self._build(strings)

    def _build(self, strings: Sequence[str]) -> None:
        """Concatenate ``strings`` into ``_buffer`` and record boundaries.

        The explicit ``str()`` coercion matters: the type hint says
        ``Sequence[str]`` but callers hand us all sorts of iterables whose
        elements are not necessarily ``str`` (notably lists of ``bytes``
        or of mixed types). Coercing here keeps the invariant that
        ``_buffer`` is always a ``str`` and that slicing it returns a
        ``str``, so callers never need to second-guess the return type of
        ``__getitem__``.
        """
        buffer_parts: List[str] = []
        ends: List[int] = []
        offset = 0
        # Materialise once. A generator input cannot be indexed, and we
        # need ``len`` for ``__len__`` anyway.
        materialised = list(strings)
        for s in materialised:
            element = str(s)
            buffer_parts.append(element)
            offset += len(element)
            ends.append(offset)
        self._buffer = "".join(buffer_parts)
        self._ends = ends

    def __len__(self) -> int:
        return len(self._ends)

    def __getitem__(self, index: int) -> str:
        if isinstance(index, slice):
            raise TypeError(
                "SpaceEfficientStringArray does not support slicing; "
                "use a range and index individually."
            )
        if not isinstance(index, int):
            # ``__index__`` lets bool/int-subclasses etc. through, which is
            # the conventional Python behaviour for numeric indices.
            raise TypeError(
                f"indices must be integers, not {type(index).__name__}"
            )
        n = len(self._ends)
        if index < 0:
            index += n
        if index < 0 or index >= n:
            raise IndexError("array index out of range")
        start = self._ends[index - 1] if index > 0 else 0
        end = self._ends[index]
        return self._buffer[start:end]

    def __iter__(self) -> Iterator[str]:
        # Rebinding locally avoids attribute lookups in the hot loop; for
        # very large arrays this is the difference between a tolerable and
        # an interminable full scan.
        buffer = self._buffer
        ends = self._ends
        prev = 0
        for end in ends:
            yield buffer[prev:end]
            prev = end

    def __contains__(self, item: object) -> bool:
        # ``Sequence.__contains__`` falls back to iteration; overriding with
        # a direct comparison avoids constructing intermediate slices when
        # the item is absent, which is the common case.
        target = item if isinstance(item, str) else str(item)
        buffer = self._buffer
        prev = 0
        for end in self._ends:
            if buffer[prev:end] == target:
                return True
            prev = end
        return False

    def __eq__(self, other: object) -> bool:
        # Only compares equal to a list of strings with identical
        # contents. Order matters; this is not a set-like comparison.
        if isinstance(other, SpaceEfficientStringArray):
            return self._ends == other._ends and self._buffer == other._buffer
        if isinstance(other, list):
            if len(other) != len(self._ends):
                return False
            for i, value in enumerate(other):
                if self[i] != value:
                    return False
            return True
        return NotImplemented

    def __repr__(self) -> str:
        sample = ", ".join(repr(self[i]) for i in range(min(3, len(self))))
        suffix = ", ..." if len(self) > 3 else ""
        return f"SpaceEfficientStringArray([{sample}{suffix}])"
