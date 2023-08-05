# coding: utf-8

import unittest
import json

from base_result import Result


class TestResult(unittest.TestCase):
    def test_init(self):
        r = Result(code=1, msg='success')
        self.assertEqual(r.code, 1)
        self.assertEqual(r.msg, 'success')
        self.assertTrue(isinstance(r, Result))
        self.assertTrue(isinstance(r.dict(), dict))

    def test_attr(self):
        r = Result()
        r.code = 1
        self.assertTrue('code' in r)
        self.assertEqual(r.code, 1)
        self.assertEqual(r['code'], 1)

    def test_key(self):
        r = Result()
        r["code"] = 2
        self.assertEqual(r.code, 2)

    def test_key_error(self):
        r = Result()
        with self.assertRaises(KeyError):
            value = r["hahaha"]

    def test_attr_error(self):
        r = Result()
        with self.assertRaises(AttributeError):
            values = r.hahaha

    def test_set_attr(self):
        r = Result()
        r.hahahaha = 1
        self.assertTrue('hahahaha' in r)

    def test_set_item(self):
        r = Result()
        r['hahahaha'] = 1
        self.assertTrue('hahahaha' in r)
