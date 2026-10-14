import unittest

from space_efficient_string_array import SpaceEfficientStringArray


class TestConstruction(unittest.TestCase):
    def test_empty_input(self):
        arr = SpaceEfficientStringArray([])
        self.assertEqual(len(arr), 0)
        self.assertEqual(list(arr), [])

    def test_single_empty_string(self):
        arr = SpaceEfficientStringArray([""])
        self.assertEqual(len(arr), 1)
        self.assertEqual(arr[0], "")
        self.assertEqual(list(arr), [""])

    def test_multiple_empty_strings(self):
        arr = SpaceEfficientStringArray(["", "", ""])
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], "")
        self.assertEqual(arr[1], "")
        self.assertEqual(arr[2], "")
        self.assertEqual(list(arr), ["", "", ""])

    def test_simple_strings(self):
        arr = SpaceEfficientStringArray(["apple", "banana", "cherry"])
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], "apple")
        self.assertEqual(arr[1], "banana")
        self.assertEqual(arr[2], "cherry")
        self.assertEqual(list(arr), ["apple", "banana", "cherry"])


class TestIndexing(unittest.TestCase):
    def test_positive_index(self):
        arr = SpaceEfficientStringArray(["a", "bb", "ccc"])
        self.assertEqual(arr[0], "a")
        self.assertEqual(arr[1], "bb")
        self.assertEqual(arr[2], "ccc")

    def test_negative_index(self):
        arr = SpaceEfficientStringArray(["a", "bb", "ccc"])
        self.assertEqual(arr[-1], "ccc")
        self.assertEqual(arr[-2], "bb")
        self.assertEqual(arr[-3], "a")

    def test_index_out_of_range_positive(self):
        arr = SpaceEfficientStringArray(["a", "b"])
        with self.assertRaises(IndexError):
            _ = arr[2]

    def test_index_out_of_range_negative(self):
        arr = SpaceEfficientStringArray(["a", "b"])
        with self.assertRaises(IndexError):
            _ = arr[-3]

    def test_slice_raises(self):
        arr = SpaceEfficientStringArray(["a", "b", "c"])
        with self.assertRaises(TypeError):
            _ = arr[0:2]

    def test_string_index_raises(self):
        arr = SpaceEfficientStringArray(["a", "b"])
        with self.assertRaises(TypeError):
            _ = arr["0"]


class TestIteration(unittest.TestCase):
    def test_iter_all_elements(self):
        data = ["one", "two", "three", "four"]
        arr = SpaceEfficientStringArray(data)
        self.assertEqual(list(arr), data)

    def test_iter_empty(self):
        arr = SpaceEfficientStringArray([])
        self.assertEqual(list(arr), [])

    def test_iter_repeated(self):
        arr = SpaceEfficientStringArray(["x", "y"])
        self.assertEqual(list(arr), ["x", "y"])
        self.assertEqual(list(arr), ["x", "y"])


class TestContains(unittest.TestCase):
    def test_present(self):
        arr = SpaceEfficientStringArray(["alpha", "beta", "gamma"])
        self.assertIn("beta", arr)
        self.assertIn("gamma", arr)
        self.assertIn("alpha", arr)

    def test_absent(self):
        arr = SpaceEfficientStringArray(["alpha", "beta"])
        self.assertNotIn("delta", arr)

    def test_empty_string_present(self):
        arr = SpaceEfficientStringArray(["a", "", "b"])
        self.assertIn("", arr)

    def test_empty_string_absent(self):
        arr = SpaceEfficientStringArray(["a", "b"])
        self.assertNotIn("", arr)


class TestEquality(unittest.TestCase):
    def test_equal_lists(self):
        data = ["foo", "bar", "baz"]
        arr = SpaceEfficientStringArray(data)
        self.assertEqual(arr, data)

    def test_unequal_lists_different_lengths(self):
        arr = SpaceEfficientStringArray(["a", "b", "c"])
        self.assertNotEqual(arr, ["a", "b"])

    def test_unequal_lists_same_length(self):
        arr = SpaceEfficientStringArray(["a", "b", "c"])
        self.assertNotEqual(arr, ["a", "b", "d"])

    def test_equal_arrays(self):
        data = ["foo", "bar"]
        a = SpaceEfficientStringArray(data)
        b = SpaceEfficientStringArray(data)
        self.assertEqual(a, b)

    def test_not_equal_to_string(self):
        arr = SpaceEfficientStringArray(["a", "b"])
        self.assertNotEqual(arr, "ab")


class TestCoercion(unittest.TestCase):
    def test_integers_coerced_to_strings(self):
        arr = SpaceEfficientStringArray([1, 2, 3])
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], "1")
        self.assertEqual(arr[1], "2")
        self.assertEqual(arr[2], "3")

    def test_mixed_types_coerced(self):
        arr = SpaceEfficientStringArray([1, "two", 3.0, True])
        self.assertEqual(arr[0], "1")
        self.assertEqual(arr[1], "two")
        self.assertEqual(arr[2], "3.0")
        self.assertEqual(arr[3], "True")


class TestRepr(unittest.TestCase):
    def test_repr_short(self):
        arr = SpaceEfficientStringArray(["a", "b"])
        r = repr(arr)
        self.assertIn("SpaceEfficientStringArray", r)
        self.assertIn("'a'", r)
        self.assertIn("'b'", r)
        self.assertNotIn("...", r)

    def test_repr_truncated(self):
        arr = SpaceEfficientStringArray(["a", "b", "c", "d"])
        r = repr(arr)
        self.assertIn("...", r)

    def test_repr_empty(self):
        arr = SpaceEfficientStringArray([])
        r = repr(arr)
        self.assertIn("SpaceEfficientStringArray", r)
        self.assertIn("[]", r)


class TestUnicode(unittest.TestCase):
    def test_multibyte_characters(self):
        data = ["héllo", "wörld", "日本語"]
        arr = SpaceEfficientStringArray(data)
        self.assertEqual(len(arr), 3)
        self.assertEqual(arr[0], "héllo")
        self.assertEqual(arr[1], "wörld")
        self.assertEqual(arr[2], "日本語")
        self.assertEqual(list(arr), data)

    def test_emoji(self):
        data = ["😀", "🚀", "📦"]
        arr = SpaceEfficientStringArray(data)
        self.assertEqual(arr[0], "😀")
        self.assertEqual(arr[1], "🚀")
        self.assertEqual(arr[2], "📦")


if __name__ == "__main__":
    unittest.main()
