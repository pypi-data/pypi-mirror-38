# This file contains the test only.
# You can run the tests with `python test.py` on the console.

import random
from decimal import *

import arithmetics

_DECIMAL_LIMIT = 10000.0

# Testing some edge cases manually.
_STATIC_TESTS = [
    [arithmetics.OPERAND_ADD, 0, 0],
    [arithmetics.OPERAND_SUBTRACT, 0, 0],
    [arithmetics.OPERAND_ADD, 1.23, 0],
    [arithmetics.OPERAND_SUBTRACT, 1.23, 0],
    [arithmetics.OPERAND_ADD, -1.23, 0],
    [arithmetics.OPERAND_SUBTRACT, -1.23, 0],
    [arithmetics.OPERAND_ADD, 0, 4.56789],
    [arithmetics.OPERAND_SUBTRACT, 0, 4.56789],
    [arithmetics.OPERAND_ADD, 1.23, 4.56789],
    [arithmetics.OPERAND_SUBTRACT, 1.23, 4.56789],
    [arithmetics.OPERAND_ADD, -1.23, 4.56789],
    [arithmetics.OPERAND_SUBTRACT, -1.23, 4.56789],
]

# Python can't calculate these numerically
_PRECOMPUTED_TESTS = [
    [arithmetics.OPERAND_ADD, '0.123456789', '0.123456789', '0.246913578'],
    [arithmetics.OPERAND_ADD,
     '0.9999999999999999999999999999999999999', '0.0000000000000000000000000000000000001', '1'],
    [arithmetics.OPERAND_SUBTRACT,
     '0.9999999999999999999999999999999999999', '0.0000000000000000000000000000000000001',
     '0.9999999999999999999999999999999999998'],
    [arithmetics.OPERAND_ADD,
     '-1.0000000000000000000000000000000000001', '0.0000000000000000000000000000000000002',
     '-0.9999999999999999999999999999999999999'],
    [arithmetics.OPERAND_MULTIPLY, '-0.249', '0.69', '-0.17181'],
    [arithmetics.OPERAND_MULTIPLY, '-12042.249', '949138.69', '-11429764440.51381'],
    [arithmetics.OPERAND_MULTIPLY, '31352725584.2464', '-4389.999945479936', '-137638463605489.0905724488802304'],
    [arithmetics.OPERAND_MULTIPLY, '4376531231238346534654738521343658334865834.8739879827913213',
     '-123380950827290485196703213.8735298304756982704423',
     '-539980584635519517644606174820023097370977572779217236866897631496501.40991196066825563084376519821275241099'],
]


# From http://docs.python.org/2/library/decimal.html#decimal-faq
def _remove_exponent(d):
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


def _r(limit=_DECIMAL_LIMIT):
    return random.randint(0, limit)


def _random_sign():
    return -1 if _r() % 2 == 0 else 1


def _generate_test():
    operand = arithmetics.OPERANDS[_r() % 2]  # Python can't do multiplication
    random1 = _random_sign() * (_r() + _r() / _DECIMAL_LIMIT)
    random2 = _random_sign() * (_r() + _r() / _DECIMAL_LIMIT)
    return _test(operand, random1, random2)


def _test(operand, random1, random2):
    random1str = Decimal(str(random1))
    random2str = Decimal(str(random2))
    expected = None
    if operand == arithmetics.OPERAND_ADD:
        expected = _remove_exponent(random1str + random2str)
    elif operand == arithmetics.OPERAND_SUBTRACT:
        expected = _remove_exponent(random1str - random2str)

    pr = arithmetics.calculate(operand, str(random1), str(random2))
    test_result = pr == str(expected)
    _print_result(test_result, random1, operand, random2, expected, pr)
    return test_result, random1, random2, operand


def _print_result(test_result, random1, operand, random2, expected, pr):
    print('[{0}] Inputs: {1} {2} {3}; expected: {4}, actual: {5}'.format(
        test_result, random1, operand, random2, expected, pr))


def _run_tests():
    failed_tests = []
    tests_ran = 0

    # Randomly generated tests.
    for x in range(0, 1000):
        tests_ran += 1
        test_result, random1, random2, operand = _generate_test()
        if not test_result:
            failed_tests.append([random1, operand, random2])

    for t in _STATIC_TESTS:
        tests_ran += 1
        test_result, random1, random2, operand = _test(t[0], t[1], t[2])
        if not test_result:
            failed_tests.append([random1, operand, random2])

    for t in _PRECOMPUTED_TESTS:
        tests_ran += 1
        pr = arithmetics.calculate(t[0], t[1], t[2])
        test_result = pr == t[3]
        _print_result(test_result, t[1], t[0], t[2], t[3], pr)
        if not test_result:
            failed_tests.append([t[1], t[0], t[2]])

    print('{0} tests ran, {1} failed.'.format(tests_ran, len(failed_tests)))
    if failed_tests:
        print('Failed tests: {0}'.format(failed_tests))


def main():
    _run_tests()


if __name__ == '__main__':
    main()
