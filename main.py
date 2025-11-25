#!/usr/bin/env python3
"""
Lexical and Semantic Analyzer for C-like Language

This module implements a comprehensive lexical analyzer (tokenizer) and semantic analyzer
for a subset of the C programming language. The analyzer supports basic data types,
control structures, and comprehensive error reporting.

Author: Santiago Patricio Irigoyen Vazquez
Course: Computer Theory - SO1-M1
Date: November 2025

Usage:
    python main.py                    # Run with built-in example
    python tests.py                    # Run test suite
    python main.py <file.c>            # Analyze specific file
"""

import re
import sys
import os
from enum import Enum

# AST Node Types
class NodeType(Enum):
    PROGRAM = "program"
    FUNCTION = "function"
    PARAMETER = "parameter"
    DECLARATION = "declaration"
    ASSIGNMENT = "assignment"
    IF_STATEMENT = "if_statement"
    WHILE_STATEMENT = "while_statement"
    FOR_STATEMENT = "for_statement"
    RETURN_STATEMENT = "return_statement"
    BINARY_EXPRESSION = "binary_expression"
    UNARY_EXPRESSION = "unary_expression"
    FUNCTION_CALL = "function_call"
    IDENTIFIER = "identifier"
    LITERAL = "literal"

# AST Node Class
class ASTNode:
    def __init__(self, node_type, value=None, children=None, line=0, column=0):
        self.type = node_type
        self.value = value
        self.children = children if children is not None else []
        self.line = line
        self.column = column
    
    def add_child(self, node):
        self.children.append(node)
        return node
    
    def __repr__(self):
        return f"ASTNode({self.type}, {self.value}, {len(self.children)} children)"

# Bytecode Instructions
class OpCode(Enum):
    LOAD_CONST = "LOAD_CONST"
    LOAD_VAR = "LOAD_VAR"
    STORE_VAR = "STORE_VAR"
    BINARY_ADD = "BINARY_ADD"
    BINARY_SUB = "BINARY_SUB"
    BINARY_MUL = "BINARY_MUL"
    BINARY_DIV = "BINARY_DIV"
    BINARY_CMP = "BINARY_CMP"
    JUMP_IF_FALSE = "JUMP_IF_FALSE"
    JUMP = "JUMP"
    CALL = "CALL"
    RETURN = "RETURN"
    PRINT = "PRINT"

class Instruction:
    def __init__(self, opcode, operand=None, line=0):
        self.opcode = opcode
        self.operand = operand
        self.line = line
    
    def __repr__(self):
        return f"Instruction({self.opcode}, {self.operand})"

class LexicalAnalyzer:
    def __init__(self):
        self.keywords = [
            'int', 'float', 'char', 'double', 'void', 'if', 'else', 'while',
            'for', 'return', 'break', 'continue', 'switch', 'case', 'default',
            'struct', 'typedef', 'const', 'static', 'do', 'goto'
        ]
        
        self.operators = [
            '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
            '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '++', '--',
            '+=', '-=', '*=', '/='
        ]
        
        self.delimiters = ['(', ')', '{', '}', '[', ']', ';', ',', '.']
        self.tokens = []
        self.errors = []
    
    @staticmethod
    def is_letter(char):
        return bool(re.match(r'[a-zA-Z_]', char))
    
    @staticmethod
    def is_digit(char):
        return bool(re.match(r'[0-9]', char))
    
    @staticmethod
    def is_whitespace(char):
        return bool(re.match(r'\s', char))
    
    def analyze(self, input_text):
        self.tokens = []
        self.errors = []
        i = 0
        line = 1
        column = 1

        while i < len(input_text):
            char = input_text[i]

            if self.is_whitespace(char):
                if char == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                i += 1
                continue

            if char == '/' and i + 1 < len(input_text) and input_text[i + 1] == '/':
                comment = ''
                start_col = column
                while i < len(input_text) and input_text[i] != '\n':
                    comment += input_text[i]
                    i += 1
                    column += 1
                self.tokens.append({
                    'type': 'COMMENT',
                    'value': comment,
                    'line': line,
                    'column': start_col
                })
                continue

            if char == '/' and i + 1 < len(input_text) and input_text[i + 1] == '*':
                comment = ''
                start_col = column
                start_line = line
                while i < len(input_text):
                    if input_text[i] == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                    comment += input_text[i]
                    if input_text[i] == '*' and i + 1 < len(input_text) and input_text[i + 1] == '/':
                        comment += input_text[i + 1]
                        i += 2
                        column += 1
                        break
                    i += 1
                self.tokens.append({
                    'type': 'COMMENT',
                    'value': comment,
                    'line': start_line,
                    'column': start_col
                })
                continue

            if self.is_letter(char):
                word = ''
                start_col = column
                while i < len(input_text) and (self.is_letter(input_text[i]) or self.is_digit(input_text[i])):
                    word += input_text[i]
                    i += 1
                    column += 1
                token_type = 'KEYWORD' if word in self.keywords else 'IDENTIFIER'
                self.tokens.append({
                    'type': token_type,
                    'value': word,
                    'line': line,
                    'column': start_col
                })
                continue

            if self.is_digit(char):
                number = ''
                start_col = column
                is_float = False
                while i < len(input_text) and (self.is_digit(input_text[i]) or input_text[i] == '.'):
                    if input_text[i] == '.':
                        if is_float:
                            self.errors.append({
                                'message': 'Número inválido: múltiples puntos decimales',
                                'line': line,
                                'column': start_col
                            })
                            break
                        is_float = True
                    number += input_text[i]
                    i += 1
                    column += 1
                self.tokens.append({
                    'type': 'FLOAT' if is_float else 'INTEGER',
                    'value': number,
                    'line': line,
                    'column': start_col
                })
                continue

            if char == '"':
                string = '"'
                start_col = column
                i += 1
                column += 1
                closed = False
                while i < len(input_text):
                    string += input_text[i]
                    if input_text[i] == '"' and (i == 0 or input_text[i - 1] != '\\'):
                        closed = True
                        i += 1
                        column += 1
                        break
                    if input_text[i] == '\n':
                        line += 1
                        column = 1
                    else:
                        column += 1
                    i += 1
                if not closed:
                    self.errors.append({
                        'message': 'Cadena no cerrada',
                        'line': line,
                        'column': start_col
                    })
                self.tokens.append({
                    'type': 'STRING',
                    'value': string,
                    'line': line,
                    'column': start_col
                })
                continue

            if char == "'":
                char_lit = "'"
                start_col = column
                i += 1
                column += 1
                closed = False
                while i < len(input_text) and len(char_lit) < 4:
                    char_lit += input_text[i]
                    if input_text[i] == "'":
                        closed = True
                        i += 1
                        column += 1
                        break
                    column += 1
                    i += 1
                if not closed or len(char_lit) > 3:
                    self.errors.append({
                        'message': 'Carácter inválido',
                        'line': line,
                        'column': start_col
                    })
                self.tokens.append({
                    'type': 'CHAR',
                    'value': char_lit,
                    'line': line,
                    'column': start_col
                })
                continue

            operator_found = False
            for length in [2, 1]:
                substr = input_text[i:i+length]
                if substr in self.operators:
                    self.tokens.append({
                        'type': 'OPERATOR',
                        'value': substr,
                        'line': line,
                        'column': column
                    })
                    i += length
                    column += length
                    operator_found = True
                    break
            if operator_found:
                continue

            if char in self.delimiters:
                self.tokens.append({
                    'type': 'DELIMITER',
                    'value': char,
                    'line': line,
                    'column': column
                })
                i += 1
                column += 1
                continue

            self.errors.append({
                'message': f"Carácter desconocido: '{char}'",
                'line': line,
                'column': column
            })
            i += 1
            column += 1



class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
        self.current_scope = 'global'
        self.scopes = {'global': {}}
        self.errors = []
    
    def enter_scope(self, scope_name):
        """Crea un nuevo ámbito de alcance"""
        self.current_scope = scope_name
        if scope_name not in self.scopes:
            self.scopes[scope_name] = {}
    
    def exit_scope(self):
        """Regresa al ámbito global"""
        self.current_scope = 'global'
    
    def add_symbol(self, name, var_type, line, column):
        """Add a symbol to the current scope"""
        current_scope_symbols = self.scopes[self.current_scope]
        
        # Check if symbol already exists in current scope
        if name in current_scope_symbols:
            self.errors.append({
                'message': f'Variable "{name}" ya ha sido declarada en este ámbito',
                'line': line,
                'column': column
            })
        else:
            current_scope_symbols[name] = {
                'type': var_type,
                'declared_at': (line, column)
            }
            return True
    
    def lookup_symbol(self, name):
        """Busca un símbolo en la tabla de símbolos"""
        # Primero busca en el ámbito actual
        if name in self.scopes[self.current_scope]:
            return self.scopes[self.current_scope][name]
        
        # Luego busca en el ámbito global
        if name in self.scopes['global']:
            return self.scopes['global'][name]
        
        return None
    
    def check_undeclared_variables(self, tokens):
        """Verifica que todas las variables usadas estén declaradas"""
        for i, token in enumerate(tokens):
            if token['type'] == 'IDENTIFIER':
                if self._should_check_variable(tokens, i):
                    self._validate_variable_declaration(token)
    
    def _should_check_variable(self, tokens, index):
        """Check if identifier should be validated for declaration"""
        # Don't check if it's a declaration
        if self._is_declaration(tokens, index):
            return False
        # Don't check if it's a function definition
        if self._is_function_definition(tokens, index):
            return False
        # Don't check if it's the left side of assignment (variable being assigned to)
        if (index < len(tokens) - 1 and 
            tokens[index + 1]['type'] == 'OPERATOR' and 
            tokens[index + 1]['value'] == '='):
            return False
        # Otherwise, it's usage and should be checked
        return True
    
    def _is_declaration(self, tokens, index):
        """Check if identifier is part of a declaration"""
        return (index > 0 and 
                tokens[index-1]['type'] == 'KEYWORD' and 
                tokens[index-1]['value'] in ['int', 'float', 'char', 'double', 'void'])
    
    def _is_function_definition(self, tokens, index):
        """Check if identifier is a function definition"""
        return (index < len(tokens) - 1 and 
                tokens[index+1]['type'] == 'DELIMITER' and 
                tokens[index+1]['value'] == '(')
    
    def _validate_variable_declaration(self, token):
        """Validate that variable is declared"""
        symbol = self.lookup_symbol(token['value'])
        if symbol is None:
            self.errors.append({
                'message': f'Variable no declarada: {token["value"]}',
                'line': token['line'],
                'column': token['column']
            })
    
    def check_type_compatibility(self, tokens):
        """Verifica la compatibilidad de tipos en operaciones"""
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if self._is_assignment_operator(token):
                self._check_assignment_compatibility(tokens, i)
            
            i += 1
    
    def _is_assignment_operator(self, token):
        """Check if token is an assignment operator"""
        return token['type'] == 'OPERATOR' and token['value'] == '='
    
    def _check_assignment_compatibility(self, tokens, i):
        """Check type compatibility for assignment at position i"""
        if i <= 0 or tokens[i-1]['type'] != 'IDENTIFIER':
            return
        
        var_name = tokens[i-1]['value']
        var_info = self.lookup_symbol(var_name)
        
        if not var_info:
            return
        
        expected_type = var_info['type']
        value_tokens = self._get_assignment_value(tokens, i + 1)
        
        for value_token in value_tokens:
            self._validate_value_type(value_token, expected_type, tokens[i])
    
    def _get_assignment_value(self, tokens, start_idx):
        """Extract value tokens from assignment"""
        value_tokens = []
        j = start_idx
        
        while j < len(tokens) and tokens[j]['type'] not in ['DELIMITER', 'OPERATOR']:
            if tokens[j]['type'] in ['INTEGER', 'FLOAT', 'STRING']:
                value_tokens.append(tokens[j])
            j += 1
        
        return value_tokens
    
    def _validate_value_type(self, value_token, expected_type, error_token):
        """Validate if value token is compatible with expected type"""
        if value_token['type'] in ['INTEGER', 'FLOAT']:
            self._check_numeric_type(value_token, expected_type, error_token)
        elif value_token['type'] == 'STRING':
            self._check_string_type(expected_type, error_token)
    
    def _check_numeric_type(self, value_token, expected_type, error_token):
        """Check numeric type compatibility"""
        value_type = 'int' if value_token['type'] == 'INTEGER' else 'float'
        
        # Allow implicit conversion from int to float
        if expected_type != value_type and not (expected_type == 'float' and value_type == 'int'):
            self.errors.append({
                'message': f'Incompatibilidad de tipos: no se puede asignar {value_type} a {expected_type}',
                'line': error_token['line'],
                'column': error_token['column']
            })
    
    def _check_string_type(self, expected_type, error_token):
        """Check string type compatibility"""
        if expected_type != 'char':
            self.errors.append({
                'message': f'Incompatibilidad de tipos: no se puede asignar string a {expected_type}',
                'line': error_token['line'],
                'column': error_token['column']
            })
    
    def analyze(self, tokens):
        """Realiza el análisis semántico"""
        # Primera pasada: recolectar declaraciones
        self._collect_declarations(tokens)
        
        # Segunda pasada: verificar uso de variables
        self.check_undeclared_variables(tokens)
        
        # Tercera pasada: verificar compatibilidad de tipos
        self.check_type_compatibility(tokens)
        
        return self.errors
    
    def _collect_declarations(self, tokens):
        """Collect variable declarations from tokens"""
        i = 0
        while i < len(tokens):
            if self._is_type_keyword(tokens[i]):
                i = self._process_declaration(tokens, i)
            else:
                i += 1
    
    def _is_type_keyword(self, token):
        """Check if token is a type keyword"""
        return (token['type'] == 'KEYWORD' and 
                token['value'] in ['int', 'float', 'char', 'double', 'void'])
    
    def _process_declaration(self, tokens, start_index):
        """Process a variable declaration starting at start_index"""
        var_type = tokens[start_index]['value']
        i = start_index + 1
        
        # Process only until we hit a semicolon
        while i < len(tokens) and not self._is_semicolon(tokens[i]):
            if tokens[i]['type'] == 'IDENTIFIER':
                if self._is_function_definition(tokens, i):
                    break
                else:
                    i = self._process_variable_declaration(tokens, i, var_type)
                    break
            i += 1
        
        return i
    
    def _is_semicolon(self, token):
        """Check if token is a semicolon"""
        return token['type'] == 'DELIMITER' and token['value'] == ';'
    
    def _process_variable_declaration(self, tokens, index, var_type):
        """Process a single variable declaration"""
        self._add_variable(tokens[index], var_type)
        
        # Move to next token after identifier
        i = index + 1
        
        # Skip assignment expression if present
        i = self._skip_assignment_expression(tokens, i)
        
        return i
    
    def _skip_assignment_expression(self, tokens, start_index):
        """Skip assignment expression and return end index"""
        i = start_index
        
        # Check if there's an assignment operator
        if i < len(tokens) and self._is_assignment_operator(tokens[i]):
            i += 1  # Skip '='
            
            # Skip the entire expression until semicolon
            while i < len(tokens) and not self._is_semicolon(tokens[i]):
                i += 1
        
        return i
    
    def _is_assignment_operator(self, token):
        """Check if token is assignment operator"""
        return token['type'] == 'OPERATOR' and token['value'] == '='
    
    def _is_function_definition(self, tokens, index):
        """Check if identifier at index is a function definition"""
        return (index < len(tokens) - 1 and 
                tokens[index + 1]['type'] == 'DELIMITER' and 
                tokens[index + 1]['value'] == '(')
    
    def _add_variable(self, token, var_type):
        """Add variable to current scope"""
        current_scope_symbols = self.scopes[self.current_scope]
        var_name = token['value']
        
        if var_name in current_scope_symbols:
            self.errors.append({
                'message': f'Variable "{var_name}" ya ha sido declarada en este ámbito',
                'line': token['line'],
                'column': token['column']
            })
        else:
            current_scope_symbols[var_name] = {
                'type': var_type,
                'declared_at': (token['line'], token['column'])
            }
    
    

# Parser/AST Generator
class Parser:
    def __init__(self, tokens=None):
        self.tokens = tokens or []
        self.position = 0
        self.current_token = None
        self.errors = []
        if self.tokens:
            self.current_token = self.tokens[0]
    
    def advance(self):
        """Move to next token"""
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
    
    def peek(self, offset=1):
        """Look ahead at token without consuming"""
        peek_pos = self.position + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def expect(self, token_type, value=None):
        """Expect a specific token type and optionally value"""
        if (self.current_token and 
            self.current_token['type'] == token_type and
            (value is None or self.current_token['value'] == value)):
            token = self.current_token
            self.advance()
            return token
        else:
            self.errors.append({
                'message': f"Expected {token_type} {f'({value})' if value else ''}, got {self.current_token['type'] if self.current_token else 'EOF'}",
                'line': self.current_token['line'] if self.current_token else 0,
                'column': self.current_token['column'] if self.current_token else 0
            })
            return None
    
    def parse(self):
        """Parse tokens into AST"""
        program = ASTNode(NodeType.PROGRAM)
        
        while self.current_token:
            if self.current_token['type'] == 'KEYWORD' and self.current_token['value'] in ['int', 'float', 'char', 'void']:
                func = self.parse_function()
                if func:
                    program.add_child(func)
            else:
                self.advance()
        
        return program
    
    def parse_function(self):
        """Parse function definition"""
        return_type = self.current_token
        self.advance()
        
        func_name = self.expect('IDENTIFIER')
        if not func_name:
            return None
        
        self.expect('DELIMITER', '(')
        self.expect('DELIMITER', ')')
        
        self.expect('DELIMITER', '{')
        
        func_node = ASTNode(NodeType.FUNCTION, func_name['value'], 
                          line=func_name['line'], column=func_name['column'])
        func_node.add_child(ASTNode(NodeType.LITERAL, return_type['value']))
        
        # Parse function body
        while self.current_token and self.current_token['value'] != '}':
            stmt = self.parse_statement()
            if stmt:
                func_node.add_child(stmt)
        
        self.expect('DELIMITER', '}')
        return func_node
    
    def parse_statement(self):
        """Parse statement"""
        if self.current_token['type'] == 'KEYWORD':
            if self.current_token['value'] == 'int' or self.current_token['value'] == 'float':
                return self.parse_declaration()
            elif self.current_token['value'] == 'if':
                return self.parse_if_statement()
            elif self.current_token['value'] == 'while':
                return self.parse_while_statement()
            elif self.current_token['value'] == 'return':
                return self.parse_return_statement()
        elif self.current_token['type'] == 'IDENTIFIER':
            return self.parse_assignment_or_call()
        
        self.advance()
        return None
    
    def parse_declaration(self):
        """Parse variable declaration"""
        var_type = self.current_token
        self.advance()
        
        var_name = self.expect('IDENTIFIER')
        if not var_name:
            return None
        
        decl_node = ASTNode(NodeType.DECLARATION, var_type['value'],
                          line=var_type['line'], column=var_type['column'])
        decl_node.add_child(ASTNode(NodeType.IDENTIFIER, var_name['value']))
        
        # Check for initialization
        if self.current_token and self.current_token['value'] == '=':
            self.advance()
            expr = self.parse_expression()
            if expr:
                decl_node.add_child(expr)
        
        self.expect('DELIMITER', ';')
        return decl_node
    
    def parse_assignment_or_call(self):
        """Parse assignment or function call"""
        var_name = self.current_token
        self.advance()
        
        if self.current_token and self.current_token['value'] == '=':
            # Assignment
            self.advance()
            expr = self.parse_expression()
            
            assign_node = ASTNode(NodeType.ASSIGNMENT, var_name['value'],
                                 line=var_name['line'], column=var_name['column'])
            assign_node.add_child(ASTNode(NodeType.IDENTIFIER, var_name['value']))
            if expr:
                assign_node.add_child(expr)
            
            self.expect('DELIMITER', ';')
            return assign_node
        elif self.current_token and self.current_token['value'] == '(':
            # Function call
            self.advance()
            self.expect('DELIMITER', ')')
            
            call_node = ASTNode(NodeType.FUNCTION_CALL, var_name['value'],
                               line=var_name['line'], column=var_name['column'])
            self.expect('DELIMITER', ';')
            return call_node
        
        return None
    
    def parse_if_statement(self):
        """Parse if statement"""
        self.expect('KEYWORD', 'if')
        self.expect('DELIMITER', '(')
        condition = self.parse_expression()
        self.expect('DELIMITER', ')')
        self.expect('DELIMITER', '{')
        
        if_node = ASTNode(NodeType.IF_STATEMENT)
        if condition:
            if_node.add_child(condition)
        
        # Parse if body
        while self.current_token and self.current_token['value'] != '}':
            stmt = self.parse_statement()
            if stmt:
                if_node.add_child(stmt)
        
        self.expect('DELIMITER', '}')
        return if_node
    
    def parse_while_statement(self):
        """Parse while statement"""
        self.expect('KEYWORD', 'while')
        self.expect('DELIMITER', '(')
        condition = self.parse_expression()
        self.expect('DELIMITER', ')')
        self.expect('DELIMITER', '{')
        
        while_node = ASTNode(NodeType.WHILE_STATEMENT)
        if condition:
            while_node.add_child(condition)
        
        # Parse while body
        while self.current_token and self.current_token['value'] != '}':
            stmt = self.parse_statement()
            if stmt:
                while_node.add_child(stmt)
        
        self.expect('DELIMITER', '}')
        return while_node
    
    def parse_return_statement(self):
        """Parse return statement"""
        self.expect('KEYWORD', 'return')
        
        return_node = ASTNode(NodeType.RETURN_STATEMENT)
        if self.current_token and self.current_token['value'] != ';':
            expr = self.parse_expression()
            if expr:
                return_node.add_child(expr)
        
        self.expect('DELIMITER', ';')
        return return_node
    
    def parse_expression(self):
        """Parse expression (simplified)"""
        left = self.parse_term()
        
        while (self.current_token and 
               self.current_token['type'] == 'OPERATOR' and
               self.current_token['value'] in ['+', '-', '>', '<', '==', '!=']):
            op = self.current_token
            self.advance()
            right = self.parse_term()
            
            bin_expr = ASTNode(NodeType.BINARY_EXPRESSION, op['value'],
                             line=op['line'], column=op['column'])
            bin_expr.add_child(left)
            bin_expr.add_child(right)
            left = bin_expr
        
        return left
    
    def parse_term(self):
        """Parse term (simplified)"""
        if self.current_token and self.current_token['type'] == 'INTEGER':
            token = self.current_token
            self.advance()
            return ASTNode(NodeType.LITERAL, int(token['value']),
                         line=token['line'], column=token['column'])
        elif self.current_token and self.current_token['type'] == 'FLOAT':
            token = self.current_token
            self.advance()
            return ASTNode(NodeType.LITERAL, float(token['value']),
                         line=token['line'], column=token['column'])
        elif self.current_token and self.current_token['type'] == 'IDENTIFIER':
            token = self.current_token
            self.advance()
            return ASTNode(NodeType.IDENTIFIER, token['value'],
                         line=token['line'], column=token['column'])
        elif self.current_token and self.current_token['value'] == '(':
            self.advance()
            expr = self.parse_expression()
            self.expect('DELIMITER', ')')
            return expr
        
        return None


# Virtual Machine/Interpreter
class VirtualMachine:
    def __init__(self):
        self.stack = []
        self.memory = {}
        self.instruction_pointer = 0
        self.instructions = []
        self.running = False
    
    def load_instructions(self, instructions):
        """Load bytecode instructions"""
        self.instructions = instructions
        self.instruction_pointer = 0
    
    def run(self):
        """Execute all instructions"""
        self.running = True
        while self.running and self.instruction_pointer < len(self.instructions):
            self.execute_instruction()
    
    def execute_instruction(self):
        """Execute single instruction"""
        instr = self.instructions[self.instruction_pointer]
        
        # Handle stack operations
        if self._handle_stack_ops(instr):
            return
        
        # Handle arithmetic operations
        if self._handle_arithmetic_ops(instr):
            return
        
        # Handle control flow operations
        if self._handle_control_flow_ops(instr):
            return
        
        # Handle other operations
        self._handle_other_ops(instr)
        
        self.instruction_pointer += 1
    
    def _handle_stack_ops(self, instr):
        """Handle stack-based operations"""
        if instr.opcode == OpCode.LOAD_CONST:
            self.stack.append(instr.operand)
            return True
        elif instr.opcode == OpCode.LOAD_VAR:
            var_name = instr.operand
            if var_name in self.memory:
                self.stack.append(self.memory[var_name])
            else:
                print(f"Runtime Error: Undefined variable '{var_name}'")
                self.running = False
            return True
        elif instr.opcode == OpCode.STORE_VAR:
            var_name = instr.operand
            if self.stack:
                self.memory[var_name] = self.stack.pop()
            return True
        return False
    
    def _handle_arithmetic_ops(self, instr):
        """Handle arithmetic operations"""
        if len(self.stack) < 2:
            return False
        
        if instr.opcode == OpCode.BINARY_ADD:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a + b)
            return True
        elif instr.opcode == OpCode.BINARY_SUB:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a - b)
            return True
        elif instr.opcode == OpCode.BINARY_MUL:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(a * b)
            return True
        elif instr.opcode == OpCode.BINARY_DIV:
            b = self.stack.pop()
            a = self.stack.pop()
            if b != 0:
                self.stack.append(a / b)
            else:
                print("Runtime Error: Division by zero")
                self.running = False
            return True
        elif instr.opcode == OpCode.BINARY_CMP:
            b = self.stack.pop()
            a = self.stack.pop()
            self.stack.append(1 if a > b else 0)
            return True
        return False
    
    def _handle_control_flow_ops(self, instr):
        """Handle control flow operations"""
        if instr.opcode == OpCode.JUMP_IF_FALSE:
            if self.stack and self.stack.pop() == 0:
                self.instruction_pointer = instr.operand
                return True
        elif instr.opcode == OpCode.JUMP:
            self.instruction_pointer = instr.operand
            return True
        return False
    
    def _handle_other_ops(self, instr):
        """Handle other operations"""
        if instr.opcode == OpCode.PRINT:
            if self.stack:
                value = self.stack.pop()
                print(value)
        elif instr.opcode == OpCode.RETURN:
            self.running = False
    
    def print_state(self):
        """Debug: Print VM state"""
        print(f"IP: {self.instruction_pointer}")
        print(f"Stack: {self.stack}")
        print(f"Memory: {self.memory}")


# Code Generator
class CodeGenerator:
    def __init__(self):
        self.instructions = []
        self.label_counter = 0
    
    def generate(self, ast):
        """Generate bytecode from AST"""
        self.instructions = []
        self.generate_node(ast)
        return self.instructions
    
    def generate_node(self, node):
        """Generate bytecode for AST node"""
        if node.type == NodeType.PROGRAM:
            for child in node.children:
                self.generate_node(child)
        elif node.type == NodeType.FUNCTION:
            # Generate function body (skip return type for now)
            for child in node.children[1:]:  # Skip return type
                self.generate_node(child)
        elif node.type == NodeType.DECLARATION:
            if len(node.children) > 1:  # Has initialization
                # Generate expression first
                self.generate_node(node.children[1])  
                # Store result in variable
                self.instructions.append(Instruction(OpCode.STORE_VAR, node.children[0].value))
        elif node.type == NodeType.ASSIGNMENT:
            # Generate expression
            self.generate_node(node.children[1])  
            # Store result in variable
            self.instructions.append(Instruction(OpCode.STORE_VAR, node.children[0].value))
        elif node.type == NodeType.BINARY_EXPRESSION:
            # Generate left operand
            self.generate_node(node.children[0])
            # Generate right operand  
            self.generate_node(node.children[1])
            
            # Apply operation
            if node.value == '+':
                self.instructions.append(Instruction(OpCode.BINARY_ADD))
            elif node.value == '-':
                self.instructions.append(Instruction(OpCode.BINARY_SUB))
            elif node.value == '*':
                self.instructions.append(Instruction(OpCode.BINARY_MUL))
            elif node.value == '/':
                self.instructions.append(Instruction(OpCode.BINARY_DIV))
            elif node.value in ['>', '<', '>=', '<=', '==', '!=']:
                self.instructions.append(Instruction(OpCode.BINARY_CMP, node.value))
        elif node.type == NodeType.LITERAL:
            # Load constant onto stack
            self.instructions.append(Instruction(OpCode.LOAD_CONST, node.value))
        elif node.type == NodeType.IDENTIFIER:
            # Load variable onto stack
            self.instructions.append(Instruction(OpCode.LOAD_VAR, node.value))
        elif node.type == NodeType.IF_STATEMENT:
            # Generate condition
            self.generate_node(node.children[0])
            
            # Jump if false
            false_label = self.new_label()
            self.instructions.append(Instruction(OpCode.JUMP_IF_FALSE, false_label))
            
            # Generate if body
            for child in node.children[1:]:
                self.generate_node(child)
            
            # Set label for after if
            self.set_label(false_label)
        elif node.type == NodeType.WHILE_STATEMENT:
            start_label = self.new_label()
            self.set_label(start_label)
            
            # Generate condition
            self.generate_node(node.children[0])
            
            # Jump if false (exit loop)
            end_label = self.new_label()
            self.instructions.append(Instruction(OpCode.JUMP_IF_FALSE, end_label))
            
            # Generate while body
            for child in node.children[1:]:
                self.generate_node(child)
            
            # Jump back to start
            self.instructions.append(Instruction(OpCode.JUMP, start_label))
            
            # Set end label
            self.set_label(end_label)
        elif node.type == NodeType.RETURN_STATEMENT:
            if node.children:
                # Generate return expression
                self.generate_node(node.children[0])
            else:
                # Return 0 by default
                self.instructions.append(Instruction(OpCode.LOAD_CONST, 0))
            self.instructions.append(Instruction(OpCode.RETURN))
    
    def new_label(self):
        """Create new label"""
        label = len(self.instructions)
        return label
    
    def set_label(self, label):
        """Set label at current position"""
        pass  # Labels are just instruction indices in this simple implementation


if __name__ == '__main__':
    import sys
    import os
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        # Analyze file from command line
        filename = sys.argv[1]
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                source_code = f.read()
            print(f"\nAnalyzing file: {filename}")
        else:
            print(f"Error: File '{filename}' not found.")
            sys.exit(1)
    else:
        # Use built-in example
        source_code = '''
int main() {
    // Declaraciones únicas de variables
    int numero = 10;
    float precio = 99.99f;  // 'f' para indicar que es float
    char letra = 'A';
    int suma;  // Declaración de suma antes de usarla
    
    // Conversión explícita para la suma de tipos diferentes
    float resultado = (float)numero + precio;
    
    if (numero > 5) {
        int temporal = 100;
        suma = numero + temporal;  // Ahora suma está declarada
        
        // Mostrar resultados
        printf("La suma es: %d\\n", suma);
        printf("El resultado es: %.2f\\n", resultado);
    }
    
    return 0;
}

// Variables globales (sin duplicados)
int contador_global = 0;
float valor_global = 0.0f;
'''
    
    # Initialize analyzers
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    parser = Parser([])
    codegen = CodeGenerator()
    vm = VirtualMachine()
    
    # Análisis léxico
    print("=" * 60)
    print("ANÁLISIS LÉXICO")
    print("=" * 60)
    lexer.analyze(source_code)
    
    # Mostrar tokens
    print("\nTokens encontrados:")
    for token in lexer.tokens:
        print(f"{token['type']:12} | {token['value']:10} | Línea: {token['line']:3}, Columna: {token['column']:3}")
    
    # Mostrar errores léxicos si los hay
    if lexer.errors:
        print("\nErrores léxicos encontrados:")
        for error in lexer.errors:
            print(f"Línea {error['line']}, Columna {error['column']}: {error['message']}")
    
    # Análisis semántico
    print("\n" + "=" * 60)
    print("ANÁLISIS SEMÁNTICO")
    print("=" * 60)
    
    semantic_errors = semantic.analyze(lexer.tokens)
    
    # Mostrar tabla de símbolos
    print("\nTabla de símbolos:")
    print("-" * 50)
    print(f"{'Ámbito':<10} | {'Nombre':<15} | {'Tipo':<10} | Declarado en")
    print("-" * 50)
    for scope, symbols in semantic.scopes.items():
        if symbols:  # Solo mostrar ámbitos con símbolos
            for name, info in symbols.items():
                line, col = info['declared_at']
                print(f"{scope:<10} | {name:<15} | {info['type']:<10} | Línea {line}, Columna {col}")
    
    # Mostrar errores semánticos si los hay
    if semantic_errors:
        print("\nErrores semánticos encontrados:")
        for error in semantic_errors:
            print(f"Línea {error['line']}, Columna {error['column']}: {error['message']}")
    else:
        print("\nNo se encontraron errores semánticos.")
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("RESUMEN DEL ANÁLISIS")
    print("=" * 60)
    print(f"\nTotal de tokens encontrados: {len(lexer.tokens)}")
    print(f"Errores léxicos encontrados: {len(lexer.errors)}")
    print(f"Errores semánticos encontrados: {len(semantic_errors)}")
    
    # Mostrar el código analizado
    print("\n" + "=" * 60)
    print("CÓDIGO ANALIZADO")
    print("=" * 60)
    print(source_code)
    print("-" * 60)
    
    # Mostrar los primeros 10 tokens como ejemplo
    print("\nPrimeros 10 tokens como ejemplo:")
    print("-" * 60)
    for token in lexer.tokens[:10]:
        print(f"{token['type']:12} | {token['value']:20} | Línea {token['line']}, Col {token['column']}")
    
    if lexer.errors or semantic_errors:
        total_errores = len(lexer.errors) + len(semantic_errors)
        print(f"\nTotal de errores encontrados: {total_errores}")
    else:
        print("\n¡Análisis completado sin errores!")
        
        # PARSING - Generate AST
        print("\n" + "=" * 60)
        print("PARSING - ÁRBOL DE SINTAXIS ABSTRACTA")
        print("=" * 60)
        
        parser = Parser(lexer.tokens)
        ast = parser.parse()
        
        if parser.errors:
            print("\nErrores de parsing encontrados:")
            for error in parser.errors:
                print(f"Línea {error['line']}, Columna {error['column']}: {error['message']}")
        else:
            print("Parsing completado exitosamente")
            print(f"AST Root: {ast}")
            print(f"Total de nodos: {len(ast.children)}")
        
        # CODE GENERATION - Generate Bytecode
        print("\n" + "=" * 60)
        print("GENERACIÓN DE CÓDIGO - BYTECODE")
        print("=" * 60)
        
        if not parser.errors:
            instructions = codegen.generate(ast)
            print("Generacion de codigo completada")
            print(f"Total de instrucciones: {len(instructions)}")
            
            print("\nBytecode generado:")
            for i, instr in enumerate(instructions):
                print(f"  {i:3d}: {instr}")
            
            # VIRTUAL MACHINE - Execute
            print("\n" + "=" * 60)
            print("MÁQUINA VIRTUAL - EJECUCIÓN")
            print("=" * 60)
            
            vm.load_instructions(instructions)
            print("Ejecutando programa...")
            vm.run()
            
            print("\nEstado final de la VM:")
            vm.print_state()