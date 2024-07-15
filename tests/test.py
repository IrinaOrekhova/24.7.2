import pytest

from app.calculator import Calculator

def setup(self):
    self.calc = calculator

def test_adding_success(self):
    assert self.calc.adding(self, 1, 1) == 2

def test_adding_unsuccess(self):
    assert self.calc.adding(self, 1, 1) == 3

def test_zero_divdsion(self):
    with pytest.raises(ZeroDivisionError):
        self.calc.divdsion(self, 1, 0)

def test_multiply(self):
    assert self.calc.multiply(self, 2, 2) == 4

def test_divide(self):
    assert self.calc.division(self, 6, 3) == 2

def test_subtraction(self):
    assert self.calc.subtraction(self, 10, 7) == 3

def teardown(self):
    print('Выполнение метода Teardown')