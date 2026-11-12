
class RegexParser:
    """
    Parses regular expressions and converts them into postfix notation.

    Supported operators:
        |  Union
        *  Kleene star
        () Grouping
        Implicit concatenation
    """

    OPERATORS = {"|", ".", "*"}

    PRECEDENCE = {
        "|": 1,
        ".": 2,
    }

    def __init__(self, expression):
        self.expression = expression.replace(" ", "")

    def tokenize(self):
        """Convert the expression into individual tokens."""

        if not self.expression:
            raise ValueError("Regular expression cannot be empty.")

        return list(self.expression)

    def add_concatenation(self, tokens):
        """Insert explicit concatenation operators."""

        result = []

        for i, token in enumerate(tokens):
            result.append(token)

            if i == len(tokens) - 1:
                continue

            next_token = tokens[i + 1]

            current_ends_expression = (
                token not in {"|", "("}
            )

            next_starts_expression = (
                next_token not in {"|", "*", ")"}
            )

            if current_ends_expression and next_starts_expression:
                result.append(".")

        return result

    def to_postfix(self):
        """Convert infix regular expression into postfix notation."""

        tokens = self.add_concatenation(self.tokenize())

        output = []
        operators = []

        expecting_operand = True
        balance = 0

        for token in tokens:

            if token == "(":
                if not expecting_operand:
                    raise ValueError("Missing operator before '('.")

                operators.append(token)
                balance += 1
                expecting_operand = True

            elif token == ")":
                if expecting_operand:
                    raise ValueError("Empty or incomplete parentheses.")

                while operators and operators[-1] != "(":
                    output.append(operators.pop())

                if not operators:
                    raise ValueError("Unmatched closing parenthesis.")

                operators.pop()
                balance -= 1
                expecting_operand = False

            elif token == "*":
                if expecting_operand:
                    raise ValueError("Kleene star has no preceding expression.")

                output.append(token)

            elif token == "|":
                if expecting_operand:
                    raise ValueError("Union operator is missing its left operand.")

                while (
                    operators
                    and operators[-1] != "("
                    and self.PRECEDENCE[operators[-1]]
                    >= self.PRECEDENCE[token]
                ):
                    output.append(operators.pop())

                operators.append(token)
                expecting_operand = True

            elif token == ".":
                if expecting_operand:
                    raise ValueError("Invalid concatenation.")

                while (
                    operators
                    and operators[-1] != "("
                    and self.PRECEDENCE[operators[-1]]
                    >= self.PRECEDENCE[token]
                ):
                    output.append(operators.pop())

                operators.append(token)
                expecting_operand = True

            else:
                if not expecting_operand:
                    raise ValueError("Missing operator between symbols.")

                output.append(token)
                expecting_operand = False

        if balance != 0:
            raise ValueError("Unmatched opening parenthesis.")

        if expecting_operand:
            raise ValueError("Regular expression ends with an operator.")

        while operators:
            operator = operators.pop()

            if operator == "(":
                raise ValueError("Unmatched opening parenthesis.")

            output.append(operator)

        return output
