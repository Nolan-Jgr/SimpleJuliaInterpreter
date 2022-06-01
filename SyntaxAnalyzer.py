##################
# CS 4308 Section 03
# Spring 2022
# Author: Nolan Jaeger
# Instructor: Sharon Perry
# Julia Interpreter
# Deliverable P2 Parser
##################


# Node class to create various node types for parse tree
# each node has a default parent, None, and an empty list of children

class Node:
    def __init__(self, tok):
        self.children = []
        self.parent = None
        self.tok = tok
        if self.children is not None:
            for child in self.children:
                self.add(child)

    def add(self, node):
        node.parent = self
        assert isinstance(node, Node)
        self.children.append(node)

    def __repr__(self):
        return self.tok

    # display method to print all nodes of the parse tree

    @staticmethod
    def disp(root):
        if root is None:
            return
        q = [root]
        level = 5
        while len(q) != 0:
            n = len(q)
            while n > 0:
                p = q.pop(0)
                print(" " * level + str(p.tok), end='')
                for i in range(len(p.children)):
                    q.append(p.children[i])
                n -= 1
            print()
            level -= 1


# Parser class

class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.__next__()

    def __next__(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.tok = self.tokens[self.index]
        return self.tok

    # arithmetic -> ident | int | arithmetic_op arithmetic

    try:
        def arithmetic_expression(self):
            # ident
            if self.tok.type == "IDENT":
                root = Node(self.tok.val)
                return root
            # int
            elif self.tok.type == "INT":
                root = Node(str(self.tok.val))
                return root
            # arithmetic op
            elif self.tok.type in arithmetic_op:
                root = Node(self.tok.type)
                self.__next__()
                # arithmetic
                node = self.arithmetic_expression()
                root.add(node)
                return root
            else:
                raise SyntaxError("illegal syntax error")

        # bool -> relative arithmetic arithmetic

        def bool_expression(self):
            # relative
            if self.tok.type not in relative_op:
                raise SyntaxError("expected relative operator")
            root = Node(self.tok.val)
            self.__next__()
            # arithmetic
            leftNode = self.arithmetic_expression()
            root.add(leftNode)
            self.__next__()
            # arithmetic
            rightNode = self.arithmetic_expression()
            root.add(rightNode)
            return root

        # print -> print ( arithmetic )

        def print_statement(self):
            # print
            root = Node("<print>")
            self.__next__()
            # (
            if self.tok.type != "LEFTPAR":
                raise SyntaxError("expected LEFTPAR")
            self.__next__()
            # arithmetic
            node = self.arithmetic_expression()
            root.add(node)
            self.__next__()
            # )
            if self.tok.type != "RIGHTPAR":
                raise SyntaxError("expected RIGHTPAR")
            return root

        # repeat -> repeat block until bool

        def repeat_statement(self):
            # repeat
            root = Node("<repeat>")
            self.__next__()
            # block
            node1 = self.block()
            root.add(node1)
            # until
            if self.tok.val != "until":
                raise SyntaxError("expected KEYWORD : until")
            node2 = Node("<until>")
            root.add(node2)
            self.__next__()
            # bool
            node3 = self.bool_expression()
            node2.add(node3)
            return root

        # assign -> id assign arithmetic

        def assign_statement(self):
            # id
            leftNode = Node(self.tok.val)
            self.__next__()
            # assign
            if self.tok.type not in assign_op:
                raise SyntaxError("expected assignment operator")
            root = Node(self.tok.val)
            self.__next__()
            root.add(leftNode)
            # arithmetic
            rightNode = self.arithmetic_expression()
            root.add(rightNode)
            return root

        # while -> while bool do block end

        def while_statement(self):
            # while
            root = Node("<while>")
            self.__next__()
            # bool
            newNode = self.bool_expression()
            root.add(newNode)
            # do
            self.__next__()
            if self.tok.val != "do":
                raise SyntaxError("expected KEYWORD : do")
            newNode = Node(self.tok.val)
            root.add(newNode)
            self.__next__()
            # block
            node = self.block()
            newNode.add(node)
            # end
            if self.tok.val != "end":
                raise SyntaxError("expected KEYWORD : end")
            endNode = Node(self.tok.val)
            root.add(endNode)
            return root

        # if -> if bool then block else block end

        def if_statement(self):
            # if
            root = Node("<if>")
            self.__next__()
            # bool
            newNode = self.bool_expression()
            root.add(newNode)
            self.__next__()
            # then
            if self.tok.val != "then":
                raise SyntaxError("expected KEYWORD : then")
            newNode = Node("<then>")
            root.add(newNode)
            self.__next__()
            # block
            node = self.block()
            newNode.add(node)
            # else
            if self.tok.val != "else":
                raise SyntaxError("expected KEYWORD : else")
            newNode = Node("<else>")
            root.add(newNode)
            self.__next__()
            # block
            node = self.block()
            newNode.add(node)
            # end
            if self.tok.val != "end":
                raise SyntaxError("expected KEYWORD : end")
            endNode = Node("<" + self.tok.val + ">")
            root.add(endNode)
            return root

        # block -> statement | statement block
        # statement -> if, while, assign, repeat, print

        def block(self):
            node = Node("<block>")
            # identifies what kind of statement
            while self.tok.val != "end" and self.tok.val != "else" and self.tok.val != "until":
                if self.tok.type == 'KEYWORD':
                    if self.tok.val == "print":
                        newNode = self.print_statement()
                        node.add(newNode)
                    elif self.tok.val == "while":
                        newNode = self.while_statement()
                        node.add(newNode)
                    elif self.tok.val == "if":
                        newNode = self.if_statement()
                        node.add(newNode)
                    elif self.tok.val == "repeat":
                        newNode = self.repeat_statement()
                        node.add(newNode)
                elif self.tok.type == 'IDENT':
                    newNode = self.assign_statement()
                    node.add(newNode)
                else:
                    raise SyntaxError("illegal syntax error")
                self.__next__()
            return node

        # program -> function id () block end

        def program(self):
            # function
            if self.tok.type != 'KEYWORD' or self.tok.val != 'function':
                raise SyntaxError("expected KEYWORD : function")
            root = Node("<" + self.tok.val + ">")
            self.__next__()
            # id
            if self.tok.type != 'IDENT':
                raise SyntaxError("expected IDENT")
            newNode = Node(self.tok.val)
            root.add(newNode)
            self.__next__()
            # (
            if self.tok.type != "LEFTPAR":
                raise SyntaxError("expected LEFTPAR")
            self.__next__()
            # )
            if self.tok.type != "RIGHTPAR":
                raise SyntaxError("expected RIGHTPAR")
            self.__next__()
            # block
            blk = self.block()
            root.add(blk)
            self.__next__()
            # end
            if self.tok.type != 'KEYWORD' or self.tok.val != 'end':
                raise SyntaxError("expected KEYWORD : end")
            newNode = Node(self.tok.val)
            root.add(newNode)

            return root

    except Exception as e:
        print(e)

    except SyntaxError as e:
        print(e)


##############################
# global lists of operators for specified statement

arithmetic_op = ["ADD", "SUB", "MULT", "DIV"]
relative_op = ["LESSEQ", "LESSTHAN", "GREATEQ", "GREATTHAN", "EQUALS", "NOTEQ"]
assign_op = ["ASSIGN", "PLUSEQ", "MINUSEQ", "MULTEQ", "DIVEQ"]
##############################
