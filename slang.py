#!/usr/bin/python

import sys
import string
import sexpdata as sex

class Func(object):
    args = []
    func = []

vars = {}
line = ''
last = ''

reserved = set(['+', '-', '*', '/', '<', '>', 'is', 'not', 'and', 'or', 'if', 'while', 'set', 'print', 'def', 'nth', 'len', 'debug'])

functions = {}

def value_of(n):
    if n == '':
        return 0
    if n[0] in string.digits:
        return float(n)
    if n[0] == "'":
        return n
    if n in functions:
        return functions[n]
    return vars[n]

def parse(s):
    if type(s) is float or type(s) is int:
        return s
    if type(s) is str:
        return s
    if type(s) is sex.Symbol:
        return value_of(s.value())
    if len(s) is 0:
        return None
    elem = s[0]
    if type(elem) is list:
        return [parse(e) for e in s]
    if type(elem) is float or type(elem) is int or type(elem) is str:
        return s
    if type(elem) is sex.Symbol:
        if elem.value() in reserved:
            if elem.value() is '+':
                ret = None
                if type(parse(s[1])) is float or type(parse(s[1])) is int:
                    ret = 0
                elif type(parse(s[1])) is str:
                    ret = ''
                elif type(parse(s[1])) is list:
                    ret = []
                for e in s[1:]:
                    if type(ret) is list and (type(e) is float or type(e) is int or type(e) is str):
                        ret.append(e)
                    else:
                        ret += parse(e)
                return ret
            if elem.value() is '-':
                ret = parse(s[1])
                for e in s[2:]:
                    ret -= parse(e)
                return ret
            if elem.value() == 'set':
                if type(s[1]) is sex.Symbol:
                    vars[s[1].value()] = parse(s[2])
                    return vars[s[1].value()]
                return None
            if elem.value() is '*':
                ret = parse(s[1])
                for e in s[2:]:
                    ret *= parse(e)
                return ret
            if elem.value() == 'if':
                if parse(s[1]) != 0:
                    return parse(s[2])
                return parse(s[3])
            if elem.value() == 'while':
                if parse(s[1]):
                    parse(s[2])
                    return parse(s)
                return None
            if elem.value() == 'is':
                return parse(s[1]) == parse(s[2])
            if elem.value() == 'not':
                return parse(s[1]) != parse(s[2])
            if elem.value() == '<':
                return parse(s[1]) < parse(s[2])
            if elem.value() == '>':
                return parse(s[1]) > parse(s[2])
            if elem.value() == 'and':
                if parse(s[1]) != 0 and parse(s[2]) != 0:
                    return 1
                return 0
            if elem.value() == 'or':
                if parse(s[1]) != 0 or parse(s[2]) != 0:
                    return 1
                return 0
            if elem.value() == 'print':
                print parse(s[1])
                return None
            if elem.value() == 'def':
                fun = Func()
                fun.args = [e.value() for e in s[2]]
                fun.func = s[3]
                vars[s[1].value()] = fun
                functions[s[1].value()] = fun
                return None
            if elem.value() == 'nth':
                l = parse(s[1])
                return parse(l[parse(s[2])])
            if elem.value() == 'len':
                return len(parse(s[1]))
            if elem.value() == 'debug':
                print vars, functions
                return None

        if isinstance(value_of(elem.value()), Func):
            return parse_fun(value_of(elem.value()), s[1])

def parse_fun(function, args):
    global vars
    tempvars = vars
    funvars = {function.args[i]: parse(args[i]) for i in range(len(args))}
    vars = funvars
    ret = parse(function.func)
    vars = tempvars
    return ret

                

while line != 'quit':
    if len(sys.argv) > 1:
        f = open(sys.argv[1])
        program = ''
        for line in f.read().split('\n'):
            if len(line) > 0 and line[0] != ';':
                program += line
        sexpr = sex.loads(program)
        parse(sexpr)
        exit()
    line = raw_input('>>')
    if line == '!!':
        line = last
    sexpr = sex.loads(line)
    print parse(sexpr)
    last = line

