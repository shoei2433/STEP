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

###################################################
def read_multiply(line, index):
    token = {'type': "MULTIPLY"}
    return token, index + 1


def read_divide(line, index):
    token = {'type': "DIVIDE"}
    return token, index + 1
###################################################

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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens

##########################################################

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
                    # devided by the next number
                    num = num / tokens[index + 2]['number']
                    index += 2
            term = {'type': "NUMBER", 'number': num}
        else: term = tokens[index]
        terms.append(term)
        index += 1
    return terms
##########################################################


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer



def test(line):
    tokens = tokenize(line)
    tokens_new = evaluate_each_term(tokens)
    actual_answer = evaluate(tokens_new)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("3.0*3")
    test("10*10/10")
    test("3/5/10")
    test("1+2/3+4*5")
    test("1.0/2.0")
    test("0/2.0")
    test("1/2.0")
    test("1/2.0")
    print("==== Test finished! ====\n")


run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    tokens_new = evaluate_each_term(tokens)
    answer = evaluate(tokens_new)
    print("answer = %f\n" % answer)
