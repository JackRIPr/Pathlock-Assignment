# Evaluate Expression:
#You have to write a program which takes Mathematical expression as an input, 
#evaluate the expression and provide  the result in output. You can write the solution 
#in any programming language. The program should consider the  associativity and 
#precision of the operators. 
#Constraint: 
#You must write your own logic of the calculation. 
#You can use any data structure. 

def evaluate_expression(expression):
    def precedence(op):
        if op in ('+', '-'):
            return 1
        if op in ('*', '/'):
            return 2
        return 0

    def apply_operator(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(left // right)  # Integer division

    def is_digit(c):
        return c.isdigit()

    operators, values = [], []
    i = 0

    while i < len(expression):
        if expression[i] == ' ':
            i += 1
            continue
        if is_digit(expression[i]):
            value = 0
            while i < len(expression) and is_digit(expression[i]):
                value = value * 10 + int(expression[i])
                i += 1
            values.append(value)
            i -= 1
        elif expression[i] == '(':
            operators.append(expression[i])
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operator(operators, values)
            operators.pop()  # Pop the '('
        else:
            while (operators and precedence(operators[-1]) >= precedence(expression[i])):
                apply_operator(operators, values)
            operators.append(expression[i])
        i += 1

    while operators:
        apply_operator(operators, values)

    return values[0]

# Example usage
expression1 = "25+5-(4*5-5)"
expression2 = "24-8+9*2-10/5"
print(evaluate_expression(expression1))  # Output: 15
print(evaluate_expression(expression2))  # Output: 32
