import pytest

number_1 = 10
number_2 = 5
number_0 = 0


def test_add():
    from my_functions import add
    assert add(number_1, number_2) == number_1 + number_2


def test_subtract():
    from my_functions import subtract
    assert subtract(number_1, number_2) == number_1 - number_2

def test_multiply():
    from my_functions import multiply
    assert multiply(number_1, number_2) == number_1 * number_2

def test_divide():
    from my_functions import divide
    assert divide(number_1, number_2) == number_1 / number_2


if __name__ == '__main__':
    pytest.main()