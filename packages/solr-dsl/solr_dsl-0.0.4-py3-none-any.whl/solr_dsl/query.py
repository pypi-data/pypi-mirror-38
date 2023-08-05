class Query:

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __invert__(self):
        return Not(self)


class Term(Query):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        if ' ' in self.value:
            return self.value
        else:
            return f'"{self.value}"'


class Field(Query):

    def __init__(self, field, value):
        self.field = field
        self.term = Term(value)

    def __str__(self):
        return f'{self.field}:{self.term}'


class Range(Query):

    def __init__(self, field, upper_bound, lower_bound):
        self.field = field
        self.upper_bound = Term(upper_bound)
        self.lower_bound = Term(lower_bound)

    def __str__(self):
        return f'{self.field}:[{self.upper_bound} TO {self.lower_bound}]'


class And(Query):

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __str__(self):
        return f'({self.left_operand} AND {self.right_operand})'


class Or(Query):

    def __init__(self, left_operand, right_operand):
        self.left_operand = left_operand
        self.right_operand = right_operand

    def __str__(self):
        return f'({self.left_operand} OR {self.right_operand})'


class Not(Query):

    def __init__(self, operand):
        self.operand

    def __str__(self):
        return f'(NOT {self.operand})'
