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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

# Calculate "multiply" and "divide" first. (after removing parentheses)
def evaluate_each_term(tokens):
    terms = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            num = tokens[index]['number']
            while index + 1  < len(tokens) and (tokens[index + 1]['type'] == "MULTIPLY" or tokens[index + 1]['type'] == "DIVIDE"):
                # the following tokens are included in the same term.
                if tokens[index + 1]['type'] == "MULTIPLY":
                    # multipied by the next number
                    num = num * tokens[index + 2]['number']
                    index += 2
                else: 
                    # divided by the next number
                    num = num / tokens[index + 2]['number']
                    index += 2
            term = {'type': "NUMBER", 'number': num}
        else: term = tokens[index]
        terms.append(term)
        index += 1
    return terms


# evaluate tokens after removing parentheses
def evaluate(tokens):
    # Calculate "multiply" and "divide" first.
    tokens_new = evaluate_each_term(tokens)
    # Then "plus" and "minus".
    answer = 0
    tokens_new.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens_new):
        if tokens_new[index]['type'] == 'NUMBER':
            if tokens_new[index - 1]['type'] == 'PLUS':
                answer += tokens_new[index]['number']
            elif tokens_new[index - 1]['type'] == 'MINUS':
                answer -= tokens_new[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


# to extract all the tokens inside this target parentheses
def find_parentheses(tokens, index):
    tokens_in_parentheses = []
    index += 1
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


def evaluate_with_parentheses(tokens):
    tokens_without_parentheses = []
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == "PARENTHESES_LEFT":
            # if there is a left parenthesis, extract all the tokens inside the parentheses, calculate them, and make a new term
            tokens_in_parentheses, index = find_parentheses(tokens, index)
            # in case there are some other parentheses inside the target parentheses, we use evaluate_with_parentheses() recursively.
            num = evaluate_with_parentheses(tokens_in_parentheses)
            term = {'type' : "NUMBER", 'number' : num }
            tokens_without_parentheses.append(term)
        else: 
            # if the token is outside any parentheses, just put it in the list.
            tokens_without_parentheses.append(tokens[index])
        index += 1
    # Evaluate the list after removing all parentheses.
    ans = evaluate(tokens_without_parentheses) 
    return ans 


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate_with_parentheses(tokens)
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

    print("==== Test finished! ====\n")


run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens_new = evaluate_each_term(tokens)
    answer = evaluate(tokens_new)
    print("answer = %f\n" % answer)
