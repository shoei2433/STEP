#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multiply(line, index):
    token = {'type': "MULTIPLY"}
    return token, index + 1


def read_divide(line, index):
    token = {'type': "DIVIDE"}
    return token, index + 1

def read_parentheses_left(line, index):
    token = {'type': "PARENTHESES_LEFT"}
    return token, index + 1

def read_parentheses_right(line, index):
    token = {'type': "PARENTHESES_RIGHT"}
    return token, index + 1

def read_abs(line, index):
    token = {'type': "ABS"}
    return token, index + 1

def read_int(line, index):
    token = {'type': "INT"}
    return token, index + 1

def read_round(line, index):
    token = {'type': "ROUND"}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        elif line[index] == '(':
            (token, index) = read_parentheses_left(line, index)
        elif line[index] == ')':
            (token, index) = read_parentheses_right(line, index)
        elif line[index] == 'a' and line[index + 1] == 'b' and line[index + 2] == 's':
            index += 2
            (token, index) = read_abs(line, index)
        elif line[index] == 'i' and line[index + 1] == 'n' and line[index + 2] == 't':
            index += 2
            (token, index) = read_int(line, index)    
        elif line[index] == 'r' and line[index + 1] == 'o' and line[index + 2] == 'u' and line[index + 3] == 'n' and line[index + 4] == 'd':
            index += 4
            (token, index) = read_round(line, index)   
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

###################################################################
# factor = number or (expression) or abs(expression) or ...
# term = factor * factor or factor / factor or ...
# expression = term + term or term - term or ...
###################################################################

# detect factor: number or () or abs()
def detect_factor(tokens, index):
    if tokens[index]['type'] == "NUMBER":
        token = tokens[index]
    elif tokens[index]['type'] == "PARENTHESES_LEFT":
        # find ()
        tokens_in_parentheses, index = find_parentheses(tokens, index + 1)
        # evaluate ()
        num = evaluate(tokens_in_parentheses)
        token  = {'type' : "NUMBER", 'number' : num }
    elif tokens[index]['type'] == "ABS":
        index += 1
        # find ()
        tokens_in_parentheses, index = find_parentheses(tokens, index + 1)
        # evaluate ()
        num = evaluate(tokens_in_parentheses)
        # abs
        if num < 0:
            num = - num
        token  = {'type' : "NUMBER", 'number' : num }
    elif tokens[index]['type'] == "INT":
        index += 1
        # find ()
        tokens_in_parentheses, index = find_parentheses(tokens, index + 1)
        # evaluate ()
        num = evaluate(tokens_in_parentheses)
        # int
        num = num // 1 
        token  = {'type' : "NUMBER", 'number' : num }
    elif tokens[index]['type'] == "ROUND":
        index += 1
        # find ()
        tokens_in_parentheses, index = find_parentheses(tokens, index + 1)
        # evaluate ()
        num = evaluate(tokens_in_parentheses)
        # round
        if num % 1 < 0.5:
            num = num // 1 
        else:
            num = num // 1 + 1
        token  = {'type' : "NUMBER", 'number' : num }
    return token, index + 1

# evaluate factor
def evaluate_factor(token): 
    return token['number']

# term -> factor * factor or factor / factor
def break_term_into_factors(tokens):
    tokens_new = []
    index = 0
    while index < len(tokens):
        if (tokens[index]['type'] == "MULTIPLY" or tokens[index]['type'] == "DIVIDE"):
            # append the token directly if it is multiply or divide
            token = tokens[index]
            index += 1
        else: 
            # else, calculate the term
            token, index  = detect_factor(tokens, index)
            num = evaluate_factor(token)
            token = {'type' : "NUMBER", 'number' : num }
        tokens_new.append(token)
    return tokens_new

# evaluate term
def evaluate_term(tokens):
    tokens_new = break_term_into_factors(tokens)
    ans = 1 
    tokens_new.insert(0, {'type': 'MULTIPLY'}) # Insert a dummy '*' token
    index = 1
    while index < len(tokens_new):
        if tokens_new[index]['type'] == 'NUMBER':
            if tokens_new[index - 1]['type'] == 'MULTIPLY':
                ans *= tokens_new[index]['number']
            elif tokens_new[index - 1]['type'] == 'DIVIDE':
                ans /= tokens_new[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return ans

# expression -> term + term or term - term
def break_expression_into_terms(tokens):
    index = 0
    tokens_new = []
    while index < len(tokens):
        if (tokens[index]['type'] == "PLUS" or tokens[index]['type'] == "MINUS"):
            # append the token directly if it is + or -
            token = tokens[index]
            index += 1
        else: 
            # else, evaluate the term
            tokens_in_term = []
            while index < len(tokens) and (tokens[index]['type'] != "PLUS" and tokens[index]['type'] != "MINUS"):
                if (tokens[index]['type'] == "MULTIPLY" or tokens[index]['type'] == "DIVIDE"):
                    # keep * and / in the term
                    token = tokens[index]
                    index += 1
                else:
                    # evaluate the factor between * and / in the term
                    token, index  = detect_factor(tokens, index)
                tokens_in_term.append(token)
            # evaluate the term
            num = evaluate_term(tokens_in_term)
            token = {'type' : "NUMBER", 'number' : num }
        tokens_new.append(token)
    return tokens_new

# evaluate expression
def evaluate_expression(tokens):
    tokens_new = break_expression_into_terms(tokens)
    ans = 0
    tokens_new.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens_new):
        if tokens_new[index]['type'] == 'NUMBER':
            if tokens_new[index - 1]['type'] == 'PLUS':
                ans += tokens_new[index]['number']
            elif tokens_new[index - 1]['type'] == 'MINUS':
                ans -= tokens_new[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return ans

# evaluate tokens 
def evaluate(tokens):
    ans = evaluate_expression(tokens)
    return ans

# to extract all the tokens inside this target parentheses
def find_parentheses(tokens, index):
    tokens_in_parentheses = []
    other_parentheses = 0
    while tokens[index]['type'] != "PARENTHESES_RIGHT" or other_parentheses != 0:
        # we have to close this function when we meet the corresponding parentheses_right
        ## in case there are some other parentheses
        if tokens[index]['type'] == "PARENTHESES_LEFT":
            other_parentheses += 1
        if tokens[index]['type'] == "PARENTHESES_RIGHT":
            other_parentheses -= 1
        # put all the terms inside the PARENTHESES in the list
        tokens_in_parentheses.append(tokens[index])
        index += 1
    return tokens_in_parentheses, index


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    # plus, minus
    test("1+2")

    # decimal
    test("1.0+2.1-3")

    # multiply, divide
    test("3.0*3")
    test("10*10/10")
    test("3/5/10")
    test("1+2/3+4*5")
    test("1.0/2.0")
    test("0/2.0")
    test("1/2.0")

    # parentheses
    test("1+(2+3)")
    test("1*(2+3)")
    test("(1+2)*(2+3)")
    test("((1+2)*(2+3))*4")
    test("((1+2)/(2+3))*4")
    test("((1+2)/((2)+3))/4")
    test("(((1)))")

    # abs
    test("abs(1)")
    test("abs(-1)")

    # int
    test("int(0.1)")

    # round
    test("round(0.1)")
    test("round(0.51)")
    
    # others
    test("abs(-1)*int(1.1)")
    test("abs(int(round(-0.51)))+abs(-1)*int(1.1)")

    # round(0.5) should be 0.000000 ???
    test("round(0.5)") 

    print("==== Test finished! ====\n")


run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens_new = evaluate(tokens)
    answer = evaluate(tokens_new)
    print("answer = %f\n" % answer)
