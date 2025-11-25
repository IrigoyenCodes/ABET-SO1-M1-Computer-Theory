#!/usr/bin/env python3
"""
Debug del CodeGenerator para encontrar problemas en la generación TAC
"""

from main import LexicalAnalyzer, Parser, CodeGenerator

def debug_codegen():
    """Debug del generador de código con trazas detalladas"""
    
    # Código simple de prueba
    source_code = '''
int main() {
    int x = 10;
    return 0;
}
'''
    
    print("=" * 60)
    print("DEBUG DEL CODE GENERATOR")
    print("=" * 60)
    
    # Pipeline hasta AST
    lexer = LexicalAnalyzer()
    parser = Parser([])
    codegen = CodeGenerator()
    
    lexer.analyze(source_code)
    print(f"Tokens: {len(lexer.tokens)}")
    
    parser.tokens = lexer.tokens
    ast = parser.parse()
    print(f"AST construido: {ast.type} con {len(ast.children)} hijos")
    
    # Debug del CodeGenerator
    print(f"\nIniciando generación de código...")
    print(f"CodeGenerator.instructions inicial: {len(codegen.instructions)}")
    
    # Agregar debug al método generate
    original_generate = codegen.generate
    
    def debug_generate(ast):
        print(f"  - generate() llamado con AST: {ast.type}")
        result = original_generate(ast)
        print(f"  - generate() completó con {len(result)} instrucciones")
        return result
    
    codegen.generate = debug_generate
    
    # Generar código
    instructions = codegen.generate(ast)
    
    print(f"\nResultados:")
    print(f"  - Instrucciones generadas: {len(instructions)}")
    
    if instructions:
        print(f"\nInstrucciones detalladas:")
        for i, instr in enumerate(instructions):
            print(f"  {i}: {instr}")
    else:
        print(f"  - No se generaron instrucciones")
    
    # Verificar nodos del AST manualmente
    print(f"\nRecorrido manual del AST:")
    def traverse_ast(node, level=0):
        indent = "  " * level
        print(f"{indent}- Nodo: {node.type} (value: {getattr(node, 'value', None)})")
        print(f"{indent}  Children: {len(node.children)}")
        
        for i, child in enumerate(node.children):
            print(f"{indent}  Child {i}:")
            traverse_ast(child, level + 2)
    
    traverse_ast(ast)

if __name__ == '__main__':
    debug_codegen()
