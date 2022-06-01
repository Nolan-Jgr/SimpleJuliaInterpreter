##################
# CS 4308 Section 03
# Spring 2022
# Author: Nolan Jaeger
# Instructor: Sharon Perry
# Julia Interpreter
# Deliverable P1 Scanner
##################
import string


# Defines class scan

class scan:

    # scans text from file and sets point to beginning character

    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.char = None
        self.__next__()

    # Method to move pointer to the next character

    def __next__(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.char = self.text[self.pos]
        else:
            self.char = None

    # Reads in each character / grouping of characters
    # and assigns it to the proper token. Each token is added to a list

    def startScan(self):
        Tokens = []
        while self.char is not None:
            if self.char in LETTER:
                Word = ""
                while self.char in LETTER:
                    Word += str(self.char)
                    self.__next__()
                if Word in KEYWORD:
                    Tokens.append(Tok('KEYWORD', Word))
                else:
                    Tokens.append(Tok('IDENT', Word))
            elif self.char in NUM:
                Tokens.append(self.number())
            elif self.char == '(':
                Tokens.append(Tok('LEFTPAR', self.char))
                self.__next__()
            elif self.char == ')':
                Tokens.append(Tok('RIGHTPAR', self.char))
                self.__next__()
            elif self.char == '=':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('EQUALS', '=='))
                    self.__next__()
                else:
                    Tokens.append(Tok('ASSIGN', self.text[self.pos - 1]))
            elif self.char == '<':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('LESSEQ', '<='))
                    self.__next__()
                else:
                    Tokens.append(Tok('LESSTHAN', self.text[self.pos - 1]))
            elif self.char == '>':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('GREATEQ', '<='))
                    self.__next__()
                else:
                    Tokens.append(Tok('GREATTHAN', self.text[self.pos - 1]))
            elif self.char == '~':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('NOTEQ', '~='))
                    self.__next__()
                else:
                    print("Invalid Character Error: " + self.text[self.pos - 1])
                    break
            elif self.char == '+':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('PLUSEQ', '+='))
                    self.__next__()
                else:
                    Tokens.append(Tok('ADD', self.text[self.pos - 1]))
            elif self.char == '-':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('MINUSEQ', '-='))
                    self.__next__()
                else:
                    Tokens.append(Tok('SUB', self.text[self.pos - 1]))
            elif self.char == '*':
                self.__next__()
                if self.char == '=':
                    Tokens.append(Tok('MULTEQ', '*='))
                    self.__next__()
                else:
                    Tokens.append(Tok('MULT', self.text[self.pos - 1]))
            elif self.char == '/':
                self.__next__()
                if self.char == '/':
                    while self.char != '\n':
                        self.__next__()
                    self.__next__()
                else:
                    if self.char == '=':
                        Tokens.append(Tok('DIVEQ', '/='))
                        self.__next__()
                    else:
                        Tokens.append(Tok('GREATTHAN', self.text[self.pos - 1]))
            elif self.char in ' \t\n':
                self.__next__()
            else:
                Tokens.append(Error("Illegal Character Error", self.text[self.pos]))
                self.__next__()

        return Tokens  # Returns a list of tokens

    #   This is a function that will decide if the number is an integer or a floating point number

    def number(self):
        numDot = 0
        numStr = ""
        while str(self.char) in NUM:
            numStr += str(self.char)
            self.__next__()
            if str(self.char) in NUM and numDot == 1:
                continue
            if numDot == 1:
                break
            if self.char == '.':
                numStr += str(self.char)
                numDot += 1
                self.__next__()

        if numDot == 1:
            return Tok('FLOAT', float(numStr))
        else:
            return Tok('INT', int(numStr))


#   scans the characters in a text file


def start(text):
    reader = scan(text)
    Tokens = reader.startScan()
    return Tokens


# possible number
NUM = '0123456789'

# possible letter
alpha = string.ascii_lowercase
LETTER = list(alpha)
alpha = string.ascii_uppercase
LETTER += list(alpha)

# possible keyword
KEYWORD = ("function", "print", "while", "do", "if", "then", "else", "end", "repeat", "until")


#   TOKEN

class Tok:
    def __init__(self, type, val):
        self.type = type
        self.val = val

    def __repr__(self):
        if self.val:
            return "{" + str(self.type) + " : " + str(self.val) + "}"
        else:
            return "{" + str(self.type) + "}"


#   ERROR

class Error:
    def __init__(self, errName, info):
        self.errName = errName
        self.info = info

    def __repr__(self):
        return str(self.errName) + ": " + str(self.info)
