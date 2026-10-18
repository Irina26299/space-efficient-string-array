# space-efficient-string-array

Concatenates string elements into a single internal buffer and tracks boundaries, enabling iteration and indexed access with minimal pointer overhead.

```python
from space_efficient_string_array import SpaceEfficientStringArray

arr = SpaceEfficientStringArray(["alpha", "beta", "gamma"])
print(len(arr))     # 3
print(arr[1])       # beta
for s in arr:
    print(s)         # alpha, beta, gamma
```

## Why this exists

A plain `list` of strings gives each element its own `str` object — header,
hash cache, length field, the works. When you have hundreds of thousands of
short, read-mostly strings (a snapshot of identifiers captured at startup
and iterated many times thereafter), that per-object overhead dominates
memory. This class stores one concatenated `str` and a single `list` of
integer end-offsets; the bookkeeping is `len(ends) * 8` bytes regardless of
how long the elements are.

The trade-off: there is no element-level mutation. Build a new array if the
set of strings changes.

## Awkward edge

Non-string inputs are coerced with `str()` at construction time, so
`SpaceEfficientStringArray([1, 2, 3])` is legal and holds `"1"`, `"2"`,
`"3"`. If you pass mixed types you will not get them back as anything but
strings. This is deliberate: the buffer is always a `str`, and `__getitem__`
always returns `str`, so callers never need to second-guess the return type.

## API

- `SpaceEfficientStringArray(strings: Sequence[str])` — constructor; coerces
each element with `str()`.
- `len(arr)` — number of elements.
- `arr[i]` — integer index only; negative indices work. Slicing raises
`TypeError`.
- `iter(arr)` — yields each element as a `str`.
- `x in arr` — membership by value, not by identity.
- `arr == other` — compares equal to a `list` of the same strings in the
same order, or to another `SpaceEfficientStringArray` with identical
contents.
- `repr(arr)` — shows up to three elements, then `...` if truncated.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

