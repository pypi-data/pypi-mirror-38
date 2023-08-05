_ZERO_CHAR = ord('0')
OPERAND_ADD = '+'
OPERAND_SUBTRACT = '-'
OPERAND_MULTIPLY = '*'
OPERANDS = [OPERAND_ADD, OPERAND_SUBTRACT, OPERAND_MULTIPLY]


def calculate(operand, input1, input2):
    """Adds, subtracts or multiples 2 numbers in string format.

    :param operand: +, - or *
    :param input1: First number
    :param input2: Second number
    :return: Result of the arithmetics operation
    """
    if operand == OPERAND_ADD:
        if _is_positive(input1) and _is_positive(input2):  # a + b
            return _add(input1, input2)
        if _is_positive(input1) and not _is_positive(input2):  # a + -b  == a - b
            return _subtract(input1, _make_positive(input2))
        if not _is_positive(input1) and not _is_positive(input2):  # -a + -b == -1 * (a + b)
            return _make_negative(_add(_make_positive(input1), _make_positive(input2)))
        if not _is_positive(input1) and _is_positive(input2):  # -a + b == b - a
            return _subtract(input2, _make_positive(input1))
    if operand == OPERAND_SUBTRACT:
        if _is_positive(input1) and _is_positive(input2):  # a - b
            return _subtract(input1, input2)
        if _is_positive(input1) and not _is_positive(input2):  # a - -b  == a + b
            return _add(input1, _make_positive(input2))
        if not _is_positive(input1) and not _is_positive(input2):  # -a - -b == b - a
            return _subtract(_make_positive(input2), _make_positive(input1))
        if not _is_positive(input1) and _is_positive(input2):  # -a - b == -1*(a + b)
            return _make_negative(_add(_make_positive(input1), input2))
    if operand == OPERAND_MULTIPLY:
        if _is_positive(input1) and _is_positive(input2):  # a * b
            return _multiply(input1, input2)
        if _is_positive(input1) and not _is_positive(input2):  # a * -b  == -1 * a * b
            return _make_negative(_multiply(input1, _make_positive(input2)))
        if not _is_positive(input1) and not _is_positive(input2):  # -a * -b == a * b
            return _multiply(_make_positive(input2), _make_positive(input1))
        if not _is_positive(input1) and _is_positive(input2):  # -a * b == -1 * a * b
            return _make_negative(_multiply(_make_positive(input1), input2))
    raise Exception('Unknown operand: ' + operand)


class Numeric:
    def __init__(self, integer_part, decimal_part, is_negative=False):
        self.integer_part = integer_part
        self.decimal_part = decimal_part
        self.is_negative = is_negative


class SignAwareString:
    def __init__(self, number, is_negative=False):
        self.number = number
        self.is_negative = is_negative


def _add(input1, input2):
    n1 = _split_number(input1)
    n2 = _split_number(input2)
    _equalize_decimal_digits(n1, n2)

    dec_result = _add_numbers(n1.decimal_part, n2.decimal_part)
    if len(dec_result) > len(n1.decimal_part):
        dec_result = dec_result[1:]
        n1.integer_part = _add_numbers(n1.integer_part, '1')

    if not _is_greater_or_equivalent(n1.integer_part, n2.integer_part):
        n1, n2 = n2, n1
    int_result = _add_numbers(n1.integer_part, n2.integer_part)

    return _format_result(int_result, dec_result)


def _add_numbers(input1, input2):
    carry = False
    result = ''
    for x in range(0, len(input1)):
        c1pos = len(input1) - x - 1
        c2pos = len(input2) - x - 1
        i1 = ord(input1[c1pos]) - _ZERO_CHAR
        if c2pos < 0:
            i2 = 0
        else:
            i2 = ord(input2[c2pos]) - _ZERO_CHAR
        if carry:
            i1 += 1
            carry = False
        if i1 + i2 >= 10:
            carry = True
        result = chr(_ZERO_CHAR + ((i1 + i2) % 10)) + result
    return ('1' if carry else '') + result


def _equalize_decimal_digits(n1, n2):
    dec_diff = len(n1.decimal_part) - len(n2.decimal_part)
    if dec_diff:
        if dec_diff > 0:
            n2.decimal_part += ('0' * dec_diff)
        else:
            n1.decimal_part += ('0' * -dec_diff)


def _is_greater_or_equivalent(input1, input2):
    if len(input1) < len(input2):
        return False
    if len(input2) < len(input1):
        return True
    for x in range(0, len(input1)):
        if ord(input1[x]) > ord(input2[x]):
            return True
        if ord(input2[x]) > ord(input1[x]):
            return False
    return True


def _is_negative(s):
    return s[0] == '-'


def _is_positive(s):
    return not _is_negative(s)


def _format_result(integer_part, decimal_part, is_negative=False):
    f_integer = _format_integer(integer_part)
    f_decimal = _format_decimal(decimal_part)
    total = f_integer + f_decimal
    return _make_negative(total) if is_negative else total


def _format_decimal(decimal_part):
    s = ''
    for x in range(0, len(decimal_part)):
        position = len(decimal_part) - 1 - x
        c = decimal_part[position]
        if c == '0' and len(s) == 0:
            continue
        s = c + s
    return '.' + s if s else ''


def _format_integer(integer_part):
    s = ''
    for x in range(0, len(integer_part)):
        c = integer_part[x]
        if c == '0' and len(s) == 0:
            continue
        s += c
    return s or '0'


def _make_positive(s):
    if not _is_negative(s):
        raise Exception(s + ' is not a negative number')
    return s[1:]


def _make_negative(s):
    return s if s == '0' else '-' + s


def _multiply(input1, input2):
    n1, dot1 = _remove_decimal(input1)
    n2, dot2 = _remove_decimal(input2)
    lines = []
    carry = 0
    for x in range(0, len(n1)):
        c1pos = len(n1) - x - 1
        i1 = ord(n1[c1pos]) - _ZERO_CHAR
        line = '' + str('0' * x)
        for j in range(0, len(n2)):
            c2pos = len(n2) - j - 1
            i2 = ord(n2[c2pos]) - _ZERO_CHAR
            tmp = i1 * i2 + carry
            carry = tmp / 10
            line = str(tmp % 10) + line
        line = (str(carry) if carry else '') + line
        lines.append(line)
        carry = 0
    result = '0'
    for l in lines:
        result = _add(result, l)
    dots_from_right = dot1 + dot2
    return _format_result(result[:-dots_from_right], result[-dots_from_right:])


def _remove_decimal(s):
    i = s.find('.')
    if i == -1:
        return s, 0
    dot_position = len(s) - s.find('.') - 1
    return s.replace('.', ''), dot_position


def _split_number(n):
    s = n.split('.')
    return Numeric(s[0], s[1] if len(s) > 1 else '0')


def _subtract(input1, input2):
    n1 = _split_number(input1)
    n2 = _split_number(input2)
    is_negative = False
    if not _is_greater_or_equivalent(n1.integer_part, n2.integer_part):
        is_negative = True
        n1, n2 = n2, n1
    _equalize_decimal_digits(n1, n2)
    dec_result = _subtract_from_bigger_number(n1.decimal_part, n2.decimal_part)
    if dec_result.is_negative:
        if n1.integer_part == n2.integer_part:
            is_negative = True
        else:
            n1.integer_part = _subtract_numbers(n1.integer_part, '1')
            dec_result.number = _subtract_numbers('1' + ('0' * len(dec_result.number)), dec_result.number)[1:]
    int_result = _subtract_from_bigger_number(n1.integer_part, n2.integer_part)
    int_result.is_negative = not int_result.is_negative if is_negative else int_result.is_negative
    return _format_result(int_result.number, dec_result.number, int_result.is_negative)


def _subtract_numbers(input1, input2):
    carry = False
    result = ''
    for x in range(0, len(input1)):
        c1pos = len(input1) - x - 1
        c2pos = len(input2) - x - 1
        c1 = ord(input1[c1pos]) - _ZERO_CHAR
        if c2pos < 0:
            c2 = 0
        else:
            c2 = ord(input2[c2pos]) - _ZERO_CHAR
        if carry:
            c1 -= 1
            carry = False
        if c1 < c2:
            c1 += 10
            carry = True
        result = chr(_ZERO_CHAR + c1 - c2) + result
    return result


def _subtract_from_bigger_number(input1, input2):
    # Using `a - b == -1 * (b - a)`, this function swaps numbers to subtract from the bigger number.
    return (
        SignAwareString(_subtract_numbers(input1, input2))
        if _is_greater_or_equivalent(input1, input2)
        else SignAwareString(_subtract_numbers(input2, input1), True)
    )
