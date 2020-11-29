#! /usr/bin/python3

import unittest
import sys

sys.path.insert(1, '../src')

from main import checkTriangleArgs
from main import checkTriangle

class Test(unittest.TestCase):
    def testCheckTriangleArgs(self):
        self._testCheckTriangleArgsCase({ "1" }, True)
        self._testCheckTriangleArgsCase({ "1", "2.2", "3", "4.4" }, True)
        self._testCheckTriangleArgsCase({ "1", "2", "3", "4", "123" }, True)
        self._testCheckTriangleArgsCase({ "a", "b", "c", "d" }, False)
        self._testCheckTriangleArgsCase({ "1", "b", "3", "d" }, False)
        self._testCheckTriangleArgsCase({ "1", "2", "3", "4d" }, False)
        self._testCheckTriangleArgsCase({ "1", "2", "3", " " }, False)
        self._testCheckTriangleArgsCase({ "1", "", "3", "d" }, False)
        self._testCheckTriangleArgsCase({ }, True)
        self._testCheckTriangleArgsCase({ "" }, False)
        self._testCheckTriangleArgsCase({ " " }, False)

    def testCheckTriangle(self):
        self._testCheckTriangleCase([ "2", "4", "5" ], "Обычный")
        self._testCheckTriangleCase([ "123", "120", "125.2" ], "Обычный")
        self._testCheckTriangleCase([ "123.1", "120.1", "125.2" ], "Обычный")
        self._testCheckTriangleCase([ "2.2", "2.2", "2.2" ], "Равносторонний")
        self._testCheckTriangleCase([ "4", "4", "4" ], "Равносторонний")
        self._testCheckTriangleCase([ "1.78E+308", "1.78E+308", "1.78E+308" ], "Равносторонний")
        self._testCheckTriangleCase([ "2", "4", "4" ], "Равнобедренный")
        self._testCheckTriangleCase([ "2.2", "3", "2.2" ], "Равнобедренный")
        self._testCheckTriangleCase([ "0", "0", "0" ], "Не Треугольник")
        self._testCheckTriangleCase([ "1", "2.2", "1" ], "Не Треугольник")
        self._testCheckTriangleCase([ "1.1", "2.2", "1.1" ], "Не Треугольник")
        self._testCheckTriangleCase([ "2", "4.2" ], "Не Треугольник")
        self._testCheckTriangleCase([ "2" ], "Не Треугольник")
        self._testCheckTriangleCase([ "2", "4", "5", "123" ], "Не Треугольник")
        self._testCheckTriangleCase([ ], "Не Треугольник")
        self._testCheckTriangleCase([ "2", "-4", "5" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "", "", "" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ " ", " ", " " ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "a", "5" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", " ", "5" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", " ", "5.4" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "4.2", "5", "asd" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "", "5sa" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "", "5" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "4", "5sd" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "a" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "as", "s", "d", "asd" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "4.1", "5", "asd" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2", "4d" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "2E+309", "2E+308", "2E+307" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "-2E+309", "2E+308", "-2E+307" ], "Неизвестная ошибка")
        self._testCheckTriangleCase([ "0xAA", "20", "10" ], "Неизвестная ошибка")

    def _testCheckTriangleArgsCase(self, args, res):
        self.assertEqual(checkTriangleArgs(args), res)

    def _testCheckTriangleCase(self, args, res):
        self.assertEqual(checkTriangle(args), res)




if __name__ == "__main__":
    unittest.main()
