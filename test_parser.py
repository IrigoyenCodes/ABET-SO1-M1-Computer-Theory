#!/usr/bin/env python3
"""
Test independiente del Parser (Generador AST)
"""

from main import LexicalAnalyzer, Parser

def test_parser():
    """Prueba del parser con código válido"""
    
    # Código de prueba simple y válido
    source_code = '''
int main() {
    int x = 10;
    int y = 20;
    int result = x + y;
    return 0;
}
'''
    
    print("=" * 60)
    print("TEST DEL PARSER - GENERACIÓN AST")
    print("=" * 60)
    
    # Inicializar componentes
    lexer = LexicalAnalyzer()
    parser = Parser([])
    
    # Análisis léxico
    lexer.analyze(source_code)
    print(f"Tokens generados: {len(lexer.tokens)}")
    
    # Parsing
    parser.tokens = lexer.tokens
    ast = parser.parse()
    
    # Mostrar resultados del parsing
    print(f"Errores de parsing: {len(parser.errors)}")
    
    if parser.errors:
        print("\nErrores encontrados:")
        for error in parser.errors:
            print(f"  - {error}")
    else:
        print("✅ Parsing completado exitosamente")
        
        # Mostrar estructura del AST
        print(f"\nEstructura del AST:")
        print(f"  Nodo raíz: {ast.type}")
        print(f"  Total de hijos: {len(ast.children)}")
        
        # Función recursiva para mostrar el árbol
        def print_ast(node, level=0):
            indent = "  " * level
            if hasattr(node, 'value') and node.value:
                print(f"{indent}- {node.type}: {node.value}")
            else:
                print(f"{indent}- {node.type}")
            
            for child in node.children:
                print_ast(child, level + 1)
        
        print("\nÁrbol completo:")
        print_ast(ast)
        
        # Estadísticas del AST
        def count_nodes(node):
            count = 1
            for child in node.children:
                count += count_nodes(child)
            return count
        
        total_nodes = count_nodes(ast)
        print("\nEstadísticas del AST:")
        print(f"  - Total de nodos: {total_nodes}")
        print(f"  - Profundidad máxima: {max_depth(ast)}")

def max_depth(node):
    """Calcula la profundidad máxima del AST"""
    if not node.children:
        return 1
    return 1 + max(max_depth(child) for child in node.children)

if __name__ == '__main__':
    test_parser()
