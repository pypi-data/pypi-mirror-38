# coding: utf-8

import unittest
import json

from validate_param import validParam
from base_result import Result


class TestResult(unittest.TestCase):
    def test_class(self):
        @validParam(a=int)
        def func(a, b=1, *args, **kwargs):
            result = Result()
            result.data = a, b, args, kwargs
            return result
        func_result = func(1)
        self.assertEqual(func_result.flag, True)
        # self.assertEqual(func_result.code, True)
        self.assertEqual(func_result.data, (1, 1, (), {}))
        func_result = func('a')
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -3000)
        self.assertEqual(func_result.status, -3000)

    def test_custom_func(self):
        def max_11(x):
            if x > 11:
                return True, 'success', 1
            else:
                return False, 'less than 11', -1

        @validParam(a=int, b=max_11)
        def func(a, b=1, *args, **kwargs):
            result = Result()
            result.data = a, b, args, kwargs
            return result
        func_result = func(1, 11)
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -1)
        self.assertEqual(func_result.status, -1)
        func_result = func('s', 11)
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -3000)
        self.assertEqual(func_result.status, -3000)
        func_result = func(1, 12)
        print func_result
        self.assertEqual(func_result.flag, True)

    def test_args(self):
        def max_11(x):
            if x > 11:
                return True, 'success', 1
            else:
                return False, 'less than 11', -1

        @validParam(a=int, b=max_11, args=int)
        def func(a, b=1, *args, **kwargs):
            result = Result()
            result.data = a, b, args, kwargs
            return result
        func_result = func(1, 11)
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -1)
        self.assertEqual(func_result.status, -1)
        func_result = func('s', 11)
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -3000)
        self.assertEqual(func_result.status, -3000)
        func_result = func(1, 12)
        self.assertEqual(func_result.flag, True)
        func_result = func(1, 12, 'a')
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -3000)
        self.assertEqual(func_result.status, -3000)
        func_result = func(1, 12, 14)
        self.assertEqual(func_result.flag, True)

    def test_kwargs(self):
        def max_11(x):
            if x > 11:
                return True, 'success', 1
            else:
                return False, 'less than 11', -1

        @validParam(a=int, b=max_11, kwargs=int)
        def func(a, b=1, *args, **kwargs):
            result = Result()
            result.data = a, b, args, kwargs
            return result
        func_result = func(1, 11)
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -1)
        self.assertEqual(func_result.status, -1)
        func_result = func('s', 11)
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -3000)
        self.assertEqual(func_result.status, -3000)
        func_result = func(1, 12)
        self.assertEqual(func_result.flag, True)
        func_result = func(1, 12, z='a')
        self.assertEqual(func_result.flag, False)
        self.assertEqual(func_result.code, -3000)
        self.assertEqual(func_result.status, -3000)
        func_result = func(1, 12, z=14)
        self.assertEqual(func_result.flag, True)
