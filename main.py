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
        return not (self._is_declaration(tokens, index) or 
                   self._is_function_definition(tokens, index))
    
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
        
        while i < len(tokens) and tokens[i]['type'] not in ['DELIMITER']:
            if tokens[i]['type'] == 'IDENTIFIER':
                if self._is_function_definition(tokens, i):
                    break
                else:
                    self._add_variable(tokens[i], var_type)
            i += 1
        
        return i
    
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
    print(sample_code)
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