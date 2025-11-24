import re

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
    
    def add_symbol(self, name, symbol_type, line, column):
        """Añade un símbolo a la tabla de símbolos"""
        if name in self.scopes[self.current_scope]:
            self.errors.append({
                'message': f'Variable "{name}" ya ha sido declarada en este ámbito',
                'line': line,
                'column': column
            })
            return False
        
        self.scopes[self.current_scope][name] = {
            'type': symbol_type,
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
                # Verificar si es una declaración (el token anterior es un tipo de dato)
                is_declaration = (i > 0 and 
                                 tokens[i-1]['type'] == 'KEYWORD' and 
                                 tokens[i-1]['value'] in ['int', 'float', 'char', 'double', 'void'])
                
                if not is_declaration:
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
            
            # Verificar asignaciones
            if token['type'] == 'OPERATOR' and token['value'] == '=':
                if i > 0 and tokens[i-1]['type'] == 'IDENTIFIER':
                    var_name = tokens[i-1]['value']
                    var_info = self.lookup_symbol(var_name)
                    
                    if var_info:
                        expected_type = var_info['type']
                        
                        # Buscar el valor asignado
                        j = i + 1
                        while j < len(tokens) and tokens[j]['type'] not in ['DELIMITER', 'OPERATOR']:
                            if tokens[j]['type'] in ['INTEGER', 'FLOAT']:
                                value_type = 'int' if tokens[j]['type'] == 'INTEGER' else 'float'
                                if expected_type != value_type:
                                    self.errors.append({
                                        'message': f'Incompatibilidad de tipos: no se puede asignar {value_type} a {expected_type}',
                                        'line': tokens[i]['line'],
                                        'column': tokens[i]['column']
                                    })
                            j += 1
            
            i += 1
    
    def analyze(self, tokens):
        """Realiza el análisis semántico"""
        # Primera pasada: recolectar declaraciones
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            # Detectar declaración de variables
            if (token['type'] == 'KEYWORD' and 
                token['value'] in ['int', 'float', 'char', 'double']):
                var_type = token['value']
                
                # Buscar el identificador después del tipo
                j = i + 1
                while j < len(tokens) and tokens[j]['type'] != 'DELIMITER':
                    if tokens[j]['type'] == 'IDENTIFIER':
                        self.add_symbol(
                            tokens[j]['value'],
                            var_type,
                            tokens[j]['line'],
                            tokens[j]['column']
                        )
                    j += 1
                
                i = j
            else:
                i += 1
        
        # Segunda pasada: verificar uso de variables
        self.check_undeclared_variables(tokens)
        
        # Tercera pasada: verificar compatibilidad de tipos
        self.check_type_compatibility(tokens)
        
        return self.errors


if __name__ == '__main__':
    # Ejemplo de uso del analizador léxico y semántico
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    
    # Código de ejemplo corregido
    sample_code = '''
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
            printf("La suma es: %d\n", suma);
            printf("El resultado es: %.2f\n", resultado);
        }
        
        return 0;
    }
    
    // Variables globales (sin duplicados)
    int contador_global = 0;
    float valor_global = 0.0f;
    '''
    
    # Análisis léxico
    print("=" * 60)
    print("ANÁLISIS LÉXICO")
    print("=" * 60)
    lexer.analyze(sample_code)
    
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