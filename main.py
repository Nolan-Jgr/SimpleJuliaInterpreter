#################
# CS 4308 Section 03
# Spring 2022
# Author: Nolan Jaeger
# Instructor: Sharon Perry
# Julia Interpreter
#################
import os
from typing import TextIO

import Scanner

# Gets file name from user
from SyntaxAnalyzer import SyntaxAnalyzer

fname = input("Enter File name: ")

# List of assignment operators
assign_ops = ['=', '+=', '-=', '*=', "/="]


# defines how an assignment statements works NOTE: only supports single variable assignment
def assign_stmnt(param):
    global variable
    global ref
    ref = param.children[0].tok
    if param.tok == '=':
        variable = int(param.children[1].tok)
    elif param.tok == '+=':
        variable += int(param.children[1].tok)
    elif param.tok == '-=':
        variable -= int(param.children[1].tok)
    elif param.tok == '*=':
        variable *= int(param.children[1].tok)
    elif param.tok == '/=':
        variable /= int(param.children[1].tok)
    else:
        raise Exception("Illegal assignment operator")


# defines how a print statement works and checks to see if a variable is referenced
def print_stmnt(params):
    if params == ref:
        print(variable)
    else:
        print(params)


# defines the do section of a while loop
def do(param):
    if param.children[0].tok in assign_ops:
        assign_stmnt(param.children[0])
    elif param.children[0].tok == '<print>':
        print_stmnt(variable)
    elif param.children[0].tok == '<while>':
        while_stmnt(param.children[0])
    elif param.children[0].tok == '<if>':
        if_stmnt(param.children[0])
    elif param.children[0].tok == '<repeat>':
        repeat_stmnt(param.children[0])
    else:
        raise Exception("Statement not supported")


# defines a while statement
def while_stmnt(param):
    global flag
    flag = True
    while flag:
        if param.children[0].tok == '<':
            if variable < int(param.children[0].children[1].tok):
                do(param.children[1].children[0])
            else:
                flag = False
        elif param.children[0].tok == '<=':
            if variable <= int(param.children[0].children[1].tok):
                do(param.children[1].children[0])
            else:
                flag = False
        elif param.children[0].tok == '>':
            if variable > int(param.children[0].children[1].tok):
                do(param.children[1].children[0])
            else:
                flag = False
        elif param.children[0].tok == '>=':
            if variable >= int(param.children[0].children[1].tok):
                do(param.children[1].children[0])
            else:
                flag = False
        elif param.children[0].tok == '==':
            if variable == int(param.children[0].children[1].tok):
                do(param.children[1].children[0])
            else:
                flag = False
        elif param.children[0].tok == '~=':
            if variable != int(param.children[0].children[1].tok):
                do(param.children[1].children[0])
            else:
                flag = False


# defines the then section of an if statement
def then(param):
    if param.children[0].tok in assign_ops:
        assign_stmnt(param.children[0])
    elif param.children[0].tok == '<print>':
        print_stmnt(param.children[0].children[0].tok)
    elif param.children[0].tok == '<while>':
        while_stmnt(param.children[0])
    elif param.children[0].tok == '<if>':
        if_stmnt(param.children[0])
    elif param.children[0].tok == '<repeat>':
        repeat_stmnt(param.children[0])
    else:
        raise Exception("Statement not supported")


# defines the else section of the if statement
def else_stmnt(param):
    if param.children[0].tok in assign_ops:
        assign_stmnt(param.children[0])
    elif param.children[0].tok == '<print>':
        print_stmnt(param.children[0].children[0].tok)
    elif param.children[0].tok == '<while>':
        while_stmnt(param.children[0])
    elif param.children[0].tok == '<if>':
        if_stmnt(param.children[0])
    elif param.children[0].tok == '<repeat>':
        repeat_stmnt(param.children[0])
    else:
        raise Exception("Statement not supported")


# defines an if statement
def if_stmnt(param):
    if param.children[0].tok == '<':
        if variable < int(param.children[0].children[1].tok):
            then(param.children[1].children[0])
        else:
            else_stmnt(param.children[2].children[0])
    elif param.children[0].tok == '<=':
        if variable <= int(param.children[0].children[1].tok):
            then(param.children[1].children[0])
        else:
            else_stmnt(param.children[2].children[0])
    elif param.children[0].tok == '>':
        if variable > int(param.children[0].children[1].tok):
            then(param.children[1].children[0])
        else:
            else_stmnt(param.children[2].children[0])
    elif param.children[0].tok == '>=':
        if variable >= int(param.children[0].children[1].tok):
            then(param.children[1].children[0])
        else:
            else_stmnt(param.children[2].children[0])
    elif param.children[0].tok == '==':
        if variable == int(param.children[0].children[1].tok):
            then(param.children[1].children[0])
        else:
            else_stmnt(param.children[2].children[0])
    elif param.children[0].tok == '~=':
        if variable != int(param.children[0].children[1].tok):
            then(param.children[1].children[0])
        else:
            else_stmnt(param.children[2].children[0])
    else:
        raise Exception("Illegal boolean operator")


def repeat_stmnt(param):
    global flag
    flag = True
    if param.children[0].children[0].tok in assign_ops:
        assign_stmnt(param.children[0].children[0])
    elif param.children[0].children[0] == '<print>':
        print_stmnt(param.children[0].children[0].tok)
    elif param.children[0].children[0] == '<while>':
        while_stmnt(param.children[0].children[0])
    elif param.children[0].children[0] == '<if>':
        if_stmnt(param.children[0].children[0])
    elif param.children[0].children[0] == '<repeat>':
        repeat_stmnt(param.children[0].children[0])
    else:
        raise Exception("Statement not supported")
    if param.children[1].children[0].tok == '<':
        if param.children[1].children[0].children[0].tok == ref:
            if variable < int(param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
        else:
            if int(param.children[1].children[0].children[0].tok) < int(
                    param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
    elif param.children[1].children[0].tok == '<=':
        if param.children[1].children[0].children[0].tok == ref:
            if variable <= int(param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
        else:
            if int(param.children[1].children[0].children[0].tok) <= int(
                    param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
    elif param.children[1].children[0].tok == '>':
        if param.children[1].children[0].children[0].tok == ref:
            if variable > int(param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
        else:
            if int(param.children[1].children[0].children[0].tok) > int(
                    param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
    elif param.children[1].children[0].tok == '>=':
        if param.children[1].children[0].children[0].tok == ref:
            if variable >= int(param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
        else:
            if int(param.children[1].children[0].children[0].tok) >= int(
                    param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
    elif param.children[1].children[0].tok == '==':
        if param.children[1].children[0].children[0].tok == ref:
            if variable == int(param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
        else:
            if int(param.children[1].children[0].children[0].tok) < int(
                    param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
    elif param.children[1].children[0].tok == '~=':
        if param.children[1].children[0].children[0].tok == ref:
            if variable != int(param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)
        else:
            if int(param.children[1].children[0].children[0].tok) < int(
                    param.children[1].children[0].children[1].tok):
                pass
            else:
                repeat_stmnt(param)


try:

    file = open(fname, "r")
    text = file.read()

    tokens = Scanner.start(text)
    """for tok in tokens:
        print(tok)"""
    tree = SyntaxAnalyzer(tokens).program()
    # tree.disp(tree)

    for x in tree.children:
        for y in x.children:
            # print(y)
            if y.tok in assign_ops:
                assign_stmnt(y)
            elif y.tok == '<print>':
                print_stmnt(y.children[0].tok)
            elif y.tok == '<while>':
                while_stmnt(y)
            elif y.tok == '<if>':
                if_stmnt(y)
            elif y.tok == '<repeat>':
                repeat_stmnt(y)
            else:
                raise Exception("Statement not supported")

    file.close()
# Exception Handling
except Exception as e:
    print(e)

except FileNotFoundError as e:
    print(e)
