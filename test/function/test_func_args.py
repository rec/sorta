from vl8.function.func_args import FuncArgs
import unittest


class TestFuncArgs(unittest.TestCase):
    def test_simple_function(self):
        f = FuncArgs('test.function.test_function.simp(required: true)')
        assert f.is_simple
        assert f.missing == set()
        assert f('one') == ('one', True, 1)

    def test_simple_function2(self):
        f = FuncArgs('test.function.test_function.simp(r: true)')
        assert f.is_simple
        assert f.missing == set()
        assert f('one') == ('one', True, 1)

    def test_simple_error(self):
        f = FuncArgs('test.function.test_function.simp')
        assert f.is_simple
        assert f.missing == {'required'}
        with self.assertRaises(TypeError) as m:
            f(0)
        assert m.exception.args == ("Missing required arguments {'required'}",)