#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
STYPUFF Interpreter - Python Version
Interpretador para a linguagem de programação Stypuff
"""

import re
import os
import sys
import shutil
import glob
from enum import Enum
from typing import List, Dict, Any, Union, Optional
from dataclasses import dataclass

# ============================================================================
# ENUMS E TYPES
# ============================================================================

class TokenType(Enum):
    EOF = "EOF"
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    SYMBOL = "SYMBOL"
    OPERATOR = "OPERATOR"
    DOT = "DOT"
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int

# ============================================================================
# TOKENIZER
# ============================================================================

class Tokenizer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.tokens: List[Token] = []
        
    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
                
            c = self.source[self.pos]
            
            if c == '"':
                self.read_string()
            elif c.isdigit():
                self.read_number()
            elif c.isalpha() or c == '_':
                self.read_identifier()
            elif self.is_symbol(c):
                self.read_symbol()
            else:
                self.pos += 1
                self.col += 1
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return self.tokens
    
    def skip_whitespace(self):
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            if self.source[self.pos] == '\n':
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.pos += 1
    
    def read_string(self):
        start_line, start_col = self.line, self.col
        self.pos += 1  # skip opening quote
        self.col += 1
        value = ""
        
        while self.pos < len(self.source) and self.source[self.pos] != '"':
            if self.source[self.pos] == '\\' and self.pos + 1 < len(self.source):
                self.pos += 1
                self.col += 1
                value += self.source[self.pos]
            else:
                value += self.source[self.pos]
            self.pos += 1
            self.col += 1
        
        if self.pos < len(self.source):
            self.pos += 1  # skip closing quote
            self.col += 1
        
        self.tokens.append(Token(TokenType.STRING, value, start_line, start_col))
    
    def read_number(self):
        start_line, start_col = self.line, self.col
        value = ""
        
        while self.pos < len(self.source) and self.source[self.pos].isdigit():
            value += self.source[self.pos]
            self.pos += 1
            self.col += 1
        
        self.tokens.append(Token(TokenType.NUMBER, value, start_line, start_col))
    
    def read_identifier(self):
        start_line, start_col = self.line, self.col
        value = ""
        
        while self.pos < len(self.source) and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
            value += self.source[self.pos]
            self.pos += 1
            self.col += 1
        
        keywords = {"styp", "work", "if", "else", "when", "let", "class", "const", 
                   "func", "on", "import", "export", "set", "assemble"}
        
        token_type = TokenType.KEYWORD if value in keywords else TokenType.IDENTIFIER
        self.tokens.append(Token(token_type, value, start_line, start_col))
    
    def read_symbol(self):
        start_line, start_col = self.line, self.col
        c = self.source[self.pos]
        value = c
        self.pos += 1
        self.col += 1
        
        # Check for two-char operators
        if self.pos < len(self.source):
            two_char = value + self.source[self.pos]
            if two_char in ["==", "!=", "<=", ">=", "##"]:
                self.pos += 1
                self.col += 1
                value = two_char
                self.tokens.append(Token(TokenType.OPERATOR, value, start_line, start_col))
                return
        
        if c in "(){}@$,|[]§":
            self.tokens.append(Token(TokenType.SYMBOL, value, start_line, start_col))
        elif c == '.':
            self.tokens.append(Token(TokenType.DOT, value, start_line, start_col))
        elif c == ':':
            self.tokens.append(Token(TokenType.COLON, value, start_line, start_col))
        elif c == '=':
            self.tokens.append(Token(TokenType.OPERATOR, value, start_line, start_col))
        elif c in "+-*/<>":
            self.tokens.append(Token(TokenType.OPERATOR, value, start_line, start_col))
        else:
            self.tokens.append(Token(TokenType.SYMBOL, value, start_line, start_col))
    
    @staticmethod
    def is_symbol(c: str) -> bool:
        return c in "(){}@$.=,|[]+*-/<>!:;§"

# ============================================================================
# AST NODES
# ============================================================================

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

class CreateStatement(ASTNode):
    def __init__(self, name: str):
        self.name = name

class FaviconStatement(ASTNode):
    def __init__(self, path: str):
        self.path = path

class VariableDeclaration(ASTNode):
    def __init__(self, name: str, value: ASTNode):
        self.name = name
        self.value = value

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, then_branch: List[ASTNode], else_branch: List[ASTNode]):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args

class FunctionDeclaration(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body

class LiteralValue(ASTNode):
    def __init__(self, value: str):
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, op: str, left: ASTNode, right: ASTNode):
        self.op = op
        self.left = left
        self.right = right

class ArrayAccess(ASTNode):
    def __init__(self, array_name: str, index: ASTNode):
        self.array_name = array_name
        self.index = index

class ReferenceExpression(ASTNode):
    def __init__(self, name: str, attribute: Optional[str] = None, args: Optional[List[ASTNode]] = None, kwargs: Optional[Dict[str, ASTNode]] = None):
        self.name = name
        self.attribute = attribute
        self.args = args or []
        self.kwargs = kwargs or {}

class DataListStatement(ASTNode):
    def __init__(self, entries: List[ASTNode]):
        self.entries = entries

class DataEntryStatement(ASTNode):
    def __init__(self, name: str, args: List[ASTNode], kwargs: Dict[str, ASTNode], attribute: Optional[str] = None, attribute_args: Optional[List[ASTNode]] = None):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.attribute = attribute
        self.attribute_args = attribute_args or []

class DataBlockStatement(ASTNode):
    def __init__(self, target: ASTNode, assignments: List[ASTNode]):
        self.target = target
        self.assignments = assignments

class AssignmentStatement(ASTNode):
    def __init__(self, target: ASTNode, value: ASTNode):
        self.target = target
        self.value = value

class ClassStatement(ASTNode):
    def __init__(self, name: str):
        self.name = name

class EventStatement(ASTNode):
    def __init__(self, target: ASTNode, event: ASTNode, body: List[ASTNode]):
        self.target = target
        self.event = event
        self.body = body

# ============================================================================
# PARSER
# ============================================================================

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> Program:
        statements = []
        while not self.is_at_end():
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        if self.check(TokenType.SYMBOL) and self.current().value == "@":
            return self.parse_at_statement()

        if self.check(TokenType.SYMBOL) and self.current().value == "#":
            self.advance()
            return None

        if self.check(TokenType.KEYWORD):
            keyword = self.current().value
            
            if keyword == "styp":
                self.advance()
                self.expect(TokenType.DOT, ".")
                if self.check(TokenType.IDENTIFIER) and self.current().value == "create":
                    self.advance()
                    self.expect(TokenType.SYMBOL, "(")
                    name = self.expect(TokenType.STRING, "expected string").value
                    self.expect(TokenType.SYMBOL, ")")
                    return CreateStatement(name)
                # styp.favicon("path/to/icon") -> copies icon into stypuffDatas/favicon.ico
                if self.check(TokenType.IDENTIFIER) and self.current().value == "favicon":
                    self.advance()
                    self.expect(TokenType.SYMBOL, "(")
                    path = self.expect(TokenType.STRING, "expected string").value
                    self.expect(TokenType.SYMBOL, ")")
                    return FaviconStatement(path)
            
            elif keyword == "work":
                self.advance()
                self.expect(TokenType.SYMBOL, "(")
                name = self.current().value if self.check(TokenType.STRING) else ""
                if self.check(TokenType.STRING):
                    self.advance()
                self.expect(TokenType.SYMBOL, ")")
                return CreateStatement(name)
            
            elif keyword == "let":
                self.advance()
                name = self.expect(TokenType.IDENTIFIER, "expected identifier").value
                self.expect(TokenType.OPERATOR, "=")
                value = self.parse_expression()
                return VariableDeclaration(name, value)
            
            elif keyword == "if":
                self.advance()
                self.expect(TokenType.SYMBOL, "(")
                condition = self.parse_expression()
                self.expect(TokenType.SYMBOL, ")")
                self.expect(TokenType.SYMBOL, "{")
                
                then_branch = []
                while not self.check(TokenType.SYMBOL) or self.current().value != "}":
                    if not self.is_at_end():
                        stmt = self.parse_statement()
                        if stmt:
                            then_branch.append(stmt)
                    else:
                        break
                self.expect(TokenType.SYMBOL, "}")
                
                return IfStatement(condition, then_branch, [])
            
            elif keyword == "func":
                self.advance()
                self.expect(TokenType.SYMBOL, "(")
                params = []
                while not self.check(TokenType.SYMBOL) or self.current().value != ")":
                    params.append(self.expect(TokenType.IDENTIFIER, "expected parameter").value)
                    if self.check(TokenType.SYMBOL) and self.current().value == ",":
                        self.advance()
                self.expect(TokenType.SYMBOL, ")")
                self.expect(TokenType.SYMBOL, "{")
                
                body = []
                while not self.check(TokenType.SYMBOL) or self.current().value != "}":
                    if not self.is_at_end():
                        stmt = self.parse_statement()
                        if stmt:
                            body.append(stmt)
                    else:
                        break
                self.expect(TokenType.SYMBOL, "}")
                
                return FunctionDeclaration("anonymous", params, body)

            elif keyword == "set":
                self.advance()
                target = self.parse_reference_expression()
                if self.check(TokenType.OPERATOR) and self.current().value == "=":
                    self.advance()
                    value = self.parse_expression()
                    return AssignmentStatement(target, value)
                return AssignmentStatement(target, LiteralValue(""))

            elif keyword == "on":
                self.advance()
                target = self.parse_reference_expression()
                self.expect(TokenType.COLON, ":")
                self.expect(TokenType.COLON, ":")
                event = self.parse_reference_expression()
                self.expect(TokenType.SYMBOL, "{")
                body = []
                while not self.check(TokenType.SYMBOL) or self.current().value != "}":
                    if not self.is_at_end():
                        stmt = self.parse_statement()
                        if stmt:
                            body.append(stmt)
                    else:
                        break
                self.expect(TokenType.SYMBOL, "}")
                return EventStatement(target, event, body)

            elif keyword == "class":
                self.advance()
                if self.check(TokenType.SYMBOL) and self.current().value == "$":
                    self.advance()
                    class_name = self.expect(TokenType.IDENTIFIER, "expected class name").value
                    if self.check(TokenType.SYMBOL) and self.current().value == "(":
                        self.advance()
                        while not self.check(TokenType.SYMBOL) or self.current().value != ")":
                            self.parse_expression()
                            if self.check(TokenType.SYMBOL) and self.current().value == ",":
                                self.advance()
                        self.expect(TokenType.SYMBOL, ")")
                    self.expect(TokenType.OPERATOR, "=")
                    value = self.parse_expression()
                    return AssignmentStatement(LiteralValue(class_name), value)
                if self.check(TokenType.SYMBOL) and self.current().value == "(":
                    self.advance()
                    name_expr = self.parse_expression()
                    self.expect(TokenType.SYMBOL, ")")
                    class_name = name_expr.value if isinstance(name_expr, LiteralValue) else ""
                    return ClassStatement(class_name)
                return ClassStatement(self.expect(TokenType.IDENTIFIER, "expected class name").value)

            elif keyword == "const":
                self.advance()
                if self.check(TokenType.SYMBOL) and self.current().value == "(":
                    self.advance()
                    name_expr = self.parse_expression()
                    self.expect(TokenType.SYMBOL, ")")
                    self.expect(TokenType.OPERATOR, "=")
                    value = self.parse_expression()
                    name = name_expr.value if isinstance(name_expr, LiteralValue) else ""
                    return VariableDeclaration(name, value)
                name = self.expect(TokenType.IDENTIFIER, "expected identifier").value
                self.expect(TokenType.OPERATOR, "=")
                value = self.parse_expression()
                return VariableDeclaration(name, value)
        
        if self.check(TokenType.IDENTIFIER):
            name = self.current().value
            self.advance()

            if name == "get":
                if self.check(TokenType.SYMBOL) and self.current().value == "(":
                    self.advance()
                    args = []
                    while not self.check(TokenType.SYMBOL) or self.current().value != ")":
                        args.append(self.parse_expression())
                        if self.check(TokenType.SYMBOL) and self.current().value == ",":
                            self.advance()
                    self.expect(TokenType.SYMBOL, ")")
                    return FunctionCall(name, args)
                if not self.is_at_end():
                    return FunctionCall(name, [self.parse_expression()])
            
            if self.check(TokenType.SYMBOL) and self.current().value == "(":
                self.advance()
                args = []
                while not self.check(TokenType.SYMBOL) or self.current().value != ")":
                    args.append(self.parse_expression())
                    if self.check(TokenType.SYMBOL) and self.current().value == ",":
                        self.advance()
                self.expect(TokenType.SYMBOL, ")")
                return FunctionCall(name, args)

            if self.check(TokenType.SYMBOL) and self.current().value == "@":
                self.advance()
                return FunctionCall(name, [self.parse_reference_expression()])
        
        return None

    def parse_at_statement(self) -> Optional[ASTNode]:
        self.advance()
        if self.check(TokenType.IDENTIFIER) and self.current().value == "datalist":
            self.advance()
            self.expect(TokenType.SYMBOL, "{")
            entries = []
            while not self.check(TokenType.SYMBOL) or self.current().value != "}":
                if self.check(TokenType.SYMBOL) and self.current().value == "§":
                    self.advance()
                    entries.append(self.parse_data_entry())
                elif self.check(TokenType.SYMBOL) and self.current().value == "}":
                    break
                else:
                    self.advance()
            self.expect(TokenType.SYMBOL, "}")
            return DataListStatement(entries)

        if self.check(TokenType.IDENTIFIER) and self.current().value == "data":
            self.advance()
            if self.check(TokenType.SYMBOL) and self.current().value == "(":
                self.advance()
                args = []
                while not self.check(TokenType.SYMBOL) or self.current().value != ")":
                    args.append(self.parse_expression())
                    if self.check(TokenType.SYMBOL) and self.current().value == ",":
                        self.advance()
                self.expect(TokenType.SYMBOL, ")")
            if self.check(TokenType.DOT):
                self.advance()
                attr = self.expect(TokenType.IDENTIFIER, "expected attribute").value
                return AssignmentStatement(ReferenceExpression("data", attr), LiteralValue(""))
            return AssignmentStatement(ReferenceExpression("data"), LiteralValue(""))

        target = self.parse_reference_expression()
        if self.check(TokenType.SYMBOL) and self.current().value == "{":
            self.advance()
            assignments = []
            while not self.check(TokenType.SYMBOL) or self.current().value != "}":
                if self.check(TokenType.SYMBOL) and self.current().value == "}":
                    break
                stmt = self.parse_statement()
                if stmt:
                    assignments.append(stmt)
            self.expect(TokenType.SYMBOL, "}")
            return DataBlockStatement(target, assignments)

        if self.check(TokenType.OPERATOR) and self.current().value == "=":
            self.advance()
            value = self.parse_expression()
            return AssignmentStatement(target, value)

        return None

    def parse_data_entry(self) -> ASTNode:
        name = self.expect(TokenType.IDENTIFIER, "expected data entry name").value
        args = []
        kwargs = {}
        attribute = None
        attribute_args = []

        if self.check(TokenType.SYMBOL) and self.current().value == "(":
            args, kwargs = self.parse_call_arguments()

        if self.check(TokenType.DOT):
            self.advance()
            attribute = self.expect(TokenType.IDENTIFIER, "expected attribute").value
            if self.check(TokenType.SYMBOL) and self.current().value == "(":
                attribute_args, _ = self.parse_call_arguments()

        return DataEntryStatement(name, args, kwargs, attribute, attribute_args)

    def parse_call_arguments(self):
        args = []
        kwargs = {}
        self.expect(TokenType.SYMBOL, "(")
        if self.check(TokenType.SYMBOL) and self.current().value == ")":
            self.expect(TokenType.SYMBOL, ")")
            return args, kwargs

        while True:
            if self.check(TokenType.IDENTIFIER) and self.peek().type == TokenType.OPERATOR and self.peek().value == "=":
                key = self.advance().value
                self.expect(TokenType.OPERATOR, "=")
                kwargs[key] = self.parse_expression()
            else:
                args.append(self.parse_expression())

            if self.check(TokenType.SYMBOL) and self.current().value == ",":
                self.advance()
            else:
                break

        self.expect(TokenType.SYMBOL, ")")
        return args, kwargs

    def parse_reference_expression(self) -> ASTNode:
        if self.check(TokenType.SYMBOL) and self.current().value in ["@", "$"]:
            self.advance()

        name = self.expect(TokenType.IDENTIFIER, "expected identifier").value
        args = []
        kwargs = {}
        attribute = None

        if self.check(TokenType.SYMBOL) and self.current().value == "(":
            args, kwargs = self.parse_call_arguments()

        if self.check(TokenType.DOT):
            self.advance()
            attribute = self.expect(TokenType.IDENTIFIER, "expected attribute").value
            if self.check(TokenType.SYMBOL) and self.current().value == "(":
                args, kwargs = self.parse_call_arguments()

        return ReferenceExpression(name, attribute, args, kwargs)

    def peek(self) -> Token:
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1]
        return self.tokens[-1]

    def parse_expression(self) -> ASTNode:
        return self.parse_comparison()
    
    def parse_comparison(self) -> ASTNode:
        expr = self.parse_additive()
        
        while self.check(TokenType.OPERATOR) and self.current().value in ["==", "!=", "<", ">", "<=", ">="]:
            op = self.current().value
            self.advance()
            right = self.parse_additive()
            expr = BinaryOp(op, expr, right)
        
        return expr
    
    def parse_additive(self) -> ASTNode:
        expr = self.parse_multiplicative()
        
        while self.check(TokenType.OPERATOR) and self.current().value in ["+", "-"]:
            op = self.current().value
            self.advance()
            right = self.parse_multiplicative()
            expr = BinaryOp(op, expr, right)
        
        return expr
    
    def parse_multiplicative(self) -> ASTNode:
        expr = self.parse_primary()
        
        while self.check(TokenType.OPERATOR) and self.current().value in ["*", "/"]:
            op = self.current().value
            self.advance()
            right = self.parse_primary()
            expr = BinaryOp(op, expr, right)
        
        return expr
    
    def parse_primary(self) -> ASTNode:
        if self.check(TokenType.STRING):
            value = self.current().value
            self.advance()
            return LiteralValue(value)
        elif self.check(TokenType.NUMBER):
            value = self.current().value
            self.advance()
            return LiteralValue(value)
        elif self.check(TokenType.IDENTIFIER):
            name = self.current().value
            self.advance()
            
            if self.check(TokenType.SYMBOL) and self.current().value == "[":
                self.advance()
                index = self.parse_expression()
                self.expect(TokenType.SYMBOL, "]")
                return ArrayAccess(name, index)
            else:
                return LiteralValue(name)
        elif self.check(TokenType.SYMBOL) and self.current().value == "(":
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.SYMBOL, ")")
            return expr
        elif self.check(TokenType.SYMBOL) and self.current().value == "@":
            self.advance()
            return self.parse_reference_expression()
        
        return LiteralValue("")
    
    def check(self, token_type: TokenType) -> bool:
        return not self.is_at_end() and self.current().type == token_type
    
    def advance(self) -> Token:
        if not self.is_at_end():
            self.pos += 1
        return self.tokens[self.pos - 1]
    
    def current(self) -> Token:
        return self.tokens[self.pos]
    
    def is_at_end(self) -> bool:
        return self.pos >= len(self.tokens) or self.current().type == TokenType.EOF
    
    def expect(self, token_type: TokenType, message: str) -> Token:
        if not self.check(token_type):
            print(f"Parse error: {message} at line {self.current().line}")
        return self.advance()

# ============================================================================
# LOCAL DATA MANAGER
# ============================================================================

class LocalData:
    def __init__(self):
        self.variables: Dict[str, str] = {}
        self.objects: Dict[str, Dict[str, str]] = {}
        self.arrays: Dict[str, List[str]] = {}
    
    def set_variable(self, name: str, value: str):
        self.variables[name] = value
    
    def get_variable(self, name: str) -> str:
        return self.variables.get(name, "")
    
    def has_variable(self, name: str) -> bool:
        return name in self.variables
    
    def create_data(self, name: str):
        self.objects[name] = {}

    def set_ref(self, key: str, value: str):
        self.variables[key] = value

    def get_ref(self, key: str) -> str:
        return self.variables.get(key, "")
    
    def set_data_field(self, obj_name: str, field: str, value: str):
        if obj_name not in self.objects:
            self.objects[obj_name] = {}
        self.objects[obj_name][field] = value
    
    def get_data_field(self, obj_name: str, field: str) -> str:
        if obj_name in self.objects and field in self.objects[obj_name]:
            return self.objects[obj_name][field]
        return ""
    
    def create_array(self, name: str):
        self.arrays[name] = []
    
    def push_to_array(self, name: str, value: str):
        if name not in self.arrays:
            self.arrays[name] = []
        self.arrays[name].append(value)
    
    def get_array_element(self, name: str, index: int) -> str:
        if name in self.arrays and 0 <= index < len(self.arrays[name]):
            return self.arrays[name][index]
        return ""
    
    def get_array_size(self, name: str) -> int:
        return len(self.arrays.get(name, []))
    
    def print_state(self):
        print("\n=== ESTADO DO SISTEMA ===")
        print("Variáveis:", self.variables)
        print("Objetos:", self.objects)
        print("Arrays:", self.arrays)

# ============================================================================
# INTERPRETER
# ============================================================================

class StypuffEngine:
    def __init__(self):
        self.data = LocalData()
        self.functions: Dict[str, FunctionDeclaration] = {}
    
    def execute(self, source: str):
        tokenizer = Tokenizer(source)
        tokens = tokenizer.tokenize()
        
        parser = Parser(tokens)
        program = parser.parse()
        
        for stmt in program.statements:
            self.execute_statement(stmt)
    
    def execute_statement(self, stmt: ASTNode):
        if isinstance(stmt, CreateStatement):
            print(f"[Stypuff] Criando objeto: {stmt.name}")
            self.data.set_variable(stmt.name, stmt.name)
        
        elif isinstance(stmt, VariableDeclaration):
            value = self.evaluate_expression(stmt.value)
            self.data.set_variable(stmt.name, value)
            print(f"[Stypuff] Variável '{stmt.name}' = {value}")
        
        elif isinstance(stmt, IfStatement):
            cond_value = self.evaluate_expression(stmt.condition)
            if cond_value in ["true", "1", "sim"]:
                for s in stmt.then_branch:
                    self.execute_statement(s)
            elif stmt.else_branch:
                for s in stmt.else_branch:
                    self.execute_statement(s)
        
        elif isinstance(stmt, FunctionCall):
            self.execute_function_call(stmt)

        elif isinstance(stmt, AssignmentStatement):
            value = self.evaluate_expression(stmt.value)
            key = self.make_reference_key(stmt.target)
            self.data.set_ref(key, value)
            print(f"[Stypuff] Dados atribuídos a '{key}' = {value}")

        elif isinstance(stmt, DataListStatement):
            for entry in stmt.entries:
                if isinstance(entry, DataEntryStatement):
                    self.execute_data_entry(entry)

        elif isinstance(stmt, DataBlockStatement):
            for inner in stmt.assignments:
                self.execute_statement(inner)

        elif isinstance(stmt, ClassStatement):
            print(f"[Stypuff] Classe declarada: {stmt.name}")

        elif isinstance(stmt, EventStatement):
            print(f"[Stypuff] Evento registrado para {self.make_reference_key(stmt.target)}")
            for inner in stmt.body:
                self.execute_statement(inner)
        
        elif isinstance(stmt, FunctionDeclaration):
            self.functions[stmt.name] = stmt
            print("[Stypuff] Função declarada")
        elif isinstance(stmt, FaviconStatement):
            src = stmt.path
            # Try relative to current working directory, then in stypuffDatas
            candidates = [src, os.path.join(os.getcwd(), src), os.path.join(os.getcwd(), "stypuffDatas", src)]
            dest_dir = os.path.join(os.getcwd(), "stypuffDatas")
            os.makedirs(dest_dir, exist_ok=True)
            dest = os.path.join(dest_dir, "favicon.ico")
            copied = False
            for c in candidates:
                if os.path.isfile(c):
                    shutil.copyfile(c, dest)
                    print(f"[Stypuff] Favicon copiado de {c} para {dest}")
                    copied = True
                    break
            if not copied:
                print(f"[Stypuff] Aviso: não foi possível localizar o favicon: {src}")
    
    def execute_data_entry(self, entry: DataEntryStatement):
        value = self.evaluate_expression(entry.args[0]) if entry.args else ""
        key = self.make_reference_key(entry)
        self.data.set_ref(key, value)
        print(f"[Stypuff] Entrada de dados '{entry.name}' = {value}")

    def make_reference_key(self, expr: ASTNode) -> str:
        if isinstance(expr, ReferenceExpression):
            parts = [expr.name]
            if expr.attribute:
                parts.append(expr.attribute)
            if expr.args:
                arg_values = [self.evaluate_expression(arg) for arg in expr.args]
                parts.extend(arg_values)
            return "::".join(parts)
        if isinstance(expr, DataEntryStatement):
            parts = [expr.name]
            if expr.attribute:
                parts.append(expr.attribute)
            if expr.attribute_args:
                parts.extend([self.evaluate_expression(arg) for arg in expr.attribute_args])
            return "::".join(parts)
        if isinstance(expr, LiteralValue):
            return expr.value
        return ""

    def execute_function_call(self, call: FunctionCall):
        if call.name == "print" or call.name == "print_ln":
            for arg in call.args:
                print(self.evaluate_expression(arg), end="")
            if call.name == "print_ln":
                print()
        elif call.name == "get":
            if call.args:
                value = self.evaluate_expression(call.args[0])
                if os.path.isfile(value):
                    with open(value, "r", encoding="utf-8") as handle:
                        content = handle.read()
                    self.data.set_ref("get::result", content)
                else:
                    self.data.set_ref("get::result", value)
        else:
            print(f"[Stypuff] Chamando função: {call.name}")
    
    def evaluate_expression(self, expr: ASTNode) -> str:
        if isinstance(expr, LiteralValue):
            if self.data.has_variable(expr.value):
                return self.data.get_variable(expr.value)
            return expr.value
        
        elif isinstance(expr, BinaryOp):
            return self.evaluate_binary_op(expr)
        
        elif isinstance(expr, ArrayAccess):
            try:
                index = int(self.evaluate_expression(expr.index))
                return self.data.get_array_element(expr.array_name, index)
            except:
                return ""

        elif isinstance(expr, ReferenceExpression):
            key = self.make_reference_key(expr)
            if self.data.get_ref(key):
                return self.data.get_ref(key)
            if expr.kwargs.get("url"):
                return self.evaluate_expression(expr.kwargs["url"])
            if expr.attribute and not expr.args and not expr.kwargs:
                return expr.attribute
            if expr.attribute and expr.args:
                return expr.attribute
            return expr.name

        elif isinstance(expr, LiteralValue):
            return expr.value
        
        return ""
    
    def evaluate_binary_op(self, op: BinaryOp) -> str:
        left = self.evaluate_expression(op.left)
        right = self.evaluate_expression(op.right)
        
        # Operações aritméticas
        try:
            l_val = float(left)
            r_val = float(right)
            
            if op.op == "+":
                return str(int(l_val + r_val))
            elif op.op == "-":
                return str(int(l_val - r_val))
            elif op.op == "*":
                return str(int(l_val * r_val))
            elif op.op == "/":
                if r_val == 0:
                    return "ERROR: Division by zero"
                return str(int(l_val / r_val))
        except:
            pass
        
        # Comparações
        if op.op == "==":
            return "true" if left == right else "false"
        elif op.op == "!=":
            return "true" if left != right else "false"
        
        try:
            l_val = int(left)
            r_val = int(right)
            if op.op == "<":
                return "true" if l_val < r_val else "false"
            elif op.op == ">":
                return "true" if l_val > r_val else "false"
            elif op.op == "<=":
                return "true" if l_val <= r_val else "false"
            elif op.op == ">=":
                return "true" if l_val >= r_val else "false"
        except:
            pass
        
        # Concatenação
        if op.op == "+":
            return left + right
        
        return ""

# ============================================================================
# MAIN
# ============================================================================

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if argv:
        target = argv[0]
        if target == "-":
            source = sys.stdin.read()
        else:
            if not os.path.exists(target):
                print(f"Arquivo não encontrado: {target}")
                return 1
            with open(target, "r", encoding="utf-8") as handle:
                source = handle.read()

        if source.strip():
            engine = StypuffEngine()
            engine.execute(source)
            return 0
        return 0

    if not sys.stdin.isatty():
        source = sys.stdin.read()
        if source.strip():
            engine = StypuffEngine()
            engine.execute(source)
            return 0

    print("╔════════════════════════════════════════════════════════════╗")
    print("║           STYPUFF Programming Language v1.0              ║")
    print("║                  Python Interpreter                      ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    
    # TESTE 1: Hello World
    print("\n--- TESTE 1: Olá Mundo ---")
    code1 = """
    styp.create("helloApp")
    let greeting = "Olá, Mundo!"
    """
    engine = StypuffEngine()
    engine.execute(code1)
    
    # TESTE 2: Operações Aritméticas
    print("\n--- TESTE 2: Operações Aritméticas ---")
    code2 = """
    styp.create("calculator")
    let num1 = 10
    let num2 = 5
    let soma = num1 + num2
    let subtracao = num1 - num2
    let multiplicacao = num1 * num2
    let divisao = num1 / num2
    """
    engine2 = StypuffEngine()
    engine2.execute(code2)
    engine2.data.print_state()
    
    # TESTE 3: Condicionais
    print("\n--- TESTE 3: Condicionais ---")
    code3 = """
    styp.create("ifExample")
    let idade = 18
    if(idade == 18) {
        print("Você tem 18 anos!")
    }
    """
    engine3 = StypuffEngine()
    engine3.execute(code3)
    
    # TESTE 4: Dados Complexos
    print("\n--- TESTE 4: Dados Complexos ---")
    engine4 = StypuffEngine()
    engine4.data.create_data("player")
    engine4.data.set_data_field("player", "name", "Herói")
    engine4.data.set_data_field("player", "level", "10")
    engine4.data.set_data_field("player", "health", "100")
    print("Player Name:", engine4.data.get_data_field("player", "name"))
    print("Player Level:", engine4.data.get_data_field("player", "level"))
    print("Player Health:", engine4.data.get_data_field("player", "health"))
    
    # TESTE 5: Arrays
    print("\n--- TESTE 5: Arrays ---")
    engine5 = StypuffEngine()
    engine5.data.create_array("numeros")
    engine5.data.push_to_array("numeros", "10")
    engine5.data.push_to_array("numeros", "20")
    engine5.data.push_to_array("numeros", "30")
    print("Array[0]:", engine5.data.get_array_element("numeros", 0))
    print("Array[1]:", engine5.data.get_array_element("numeros", 1))
    print("Array[2]:", engine5.data.get_array_element("numeros", 2))
    print("Tamanho do Array:", engine5.data.get_array_size("numeros"))
    
    print("\n╔════════════════════════════════════════════════════════════╗")
    print("║                  Testes Concluídos!                      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
