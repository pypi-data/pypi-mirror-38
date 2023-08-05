class Query:

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Term(Query):

    def __init__(self, *values):
        self.values = values

    def __str__(self):
        return parenthesize(' OR '.join(quote(value) for value in self.values))


class Field(Query):

    def __init__(self, field, *values):
        self.field = field
        self.term = Term(*values)

    def __str__(self):
        return '{}:{}'.format(self.field, self.term)


class Range(Query):

    def __init__(self, field, upper_bound, lower_bound):
        self.field = field
        self.upper_bound = Term(upper_bound)
        self.lower_bound = Term(lower_bound)

    def __str__(self):
        return '{}:[{} TO {}]'.format(self.field,
                                      self.upper_bound,
                                      self.lower_bound)


class And(Query):

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __str__(self):
        return '({} AND {})'.format(self.left_operand, self.right_operand)


class Or(Query):

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __str__(self):
        return '({} OR {})'.format(self.left_operand, self.right_operand)


class Not(Query):

    def __init__(self, operand):
        self.operand

    def __str__(self):
        return '(NOT {})'.format(self.operand)


def quote(value):
    if ' ' in value:
        return '"{}"'.format(value)
    else:
        return value


def parenthesize(value):
    return '({})'.format(value)
