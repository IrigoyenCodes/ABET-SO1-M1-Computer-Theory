#!/usr/bin/env python3
"""
Debug del Parser para encontrar problemas en el AST
"""

from main import LexicalAnalyzer, Parser

def debug_parser():
    """Debug del parser con trazas detalladas"""
    
    # Código simple de prueba
    source_code = '''
int main() {
    int x = 10;
    return 0;
}
'''
    
    print("=" * 60)
    print("DEBUG DEL PARSER")
    print("=" * 60)
    
    # Análisis léxico
    lexer = LexicalAnalyzer()
    lexer.analyze(source_code)
    
    print(f"Tokens generados: {len(lexer.tokens)}")
    print("\nPrimeros 10 tokens:")
    for i, token in enumerate(lexer.tokens[:10]):
        print(f"  {i}: {token['type']:12} | {token['value']:10} | L:{token['line']}, C:{token['column']}")
    
    # Parsing con debug
    parser = Parser(lexer.tokens)
    
    print(f"\nParser inicializado:")
    print(f"  - Total tokens: {len(parser.tokens)}")
    print(f"  - Position: {parser.position}")
    print(f"  - Current token: {parser.current_token}")
    
    # Intentar parsear
    ast = parser.parse()
    
    print(f"\nResultado del parsing:")
    print(f"  - AST type: {ast.type}")
    print(f"  - AST children: {len(ast.children)}")
    print(f"  - Parser errors: {len(parser.errors)}")
    
    if parser.errors:
        print("\nErrores del parser:")
        for error in parser.errors:
            print(f"  - {error}")
    
    # Mostrar estructura del AST
    print(f"\nEstructura detallada del AST:")
    def print_ast_detailed(node, level=0):
        indent = "  " * level
        node_info = f"{node.type}"
        if hasattr(node, 'value') and node.value:
            node_info += f": {node.value}"
        if hasattr(node, 'line') and hasattr(node, 'column'):
            node_info += f" (L:{node.line}, C:{node.column})"
        print(f"{indent}- {node_info}")
        
        for i, child in enumerate(node.children):
            print(f"{indent}  Child {i}:")
            print_ast_detailed(child, level + 2)
    
    print_ast_detailed(ast)

if __name__ == '__main__':
    debug_parser()
