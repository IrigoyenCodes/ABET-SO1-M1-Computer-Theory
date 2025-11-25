#!/usr/bin/env python3
"""
Test independiente del Generador de Código
"""

from main import LexicalAnalyzer, Parser, CodeGenerator

def test_code_generation():
    """Prueba del generador de código con AST válido"""
    
    # Código de prueba simple
    source_code = '''
int main() {
    int x = 10;
    int y = 20;
    int result = x + y;
    return 0;
}
'''
    
    print("=" * 60)
    print("TEST DEL GENERADOR DE CÓDIGO")
    print("=" * 60)
    
    # Pipeline hasta AST
    lexer = LexicalAnalyzer()
    codegen = CodeGenerator()
    
    # Análisis léxico
    lexer.analyze(source_code)
    print(f"Tokens generados: {len(lexer.tokens)}")
    
    # Parsing con tokens correctos
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    
    if parser.errors:
        print("❌ No se puede generar código debido a errores de parsing")
        for error in parser.errors:
            print(f"  - {error}")
        return
    
    print(f"✅ AST construido correctamente")
    print(f"   - Tipo: {ast.type}")
    print(f"   - Hijos: {len(ast.children)}")
    print(f"   - Errores: {len(parser.errors)}")
    
    # Generación de código
    instructions = codegen.generate(ast)
    
    print(f"\nInstrucciones generadas: {len(instructions)}")
    
    # Mostrar bytecode generado
    print("\nBytecode (Three-Address Code):")
    print("-" * 40)
    for i, instr in enumerate(instructions):
        if instr.operand:
            print(f"  {i:2d}: {instr.opcode:<15} {instr.operand}")
        else:
            print(f"  {i:2d}: {instr.opcode:<15}")
    
    # Análisis de las instrucciones generadas
    opcodes = {}
    for instr in instructions:
        opcodes[instr.opcode] = opcodes.get(instr.opcode, 0) + 1
    
    print("\nDistribución de instrucciones:")
    print("-" * 25)
    for opcode, count in sorted(opcodes.items(), key=lambda x: str(x[0])):
        print(f"{str(opcode):<15}: {count:2d}")
    
    # Explicación del código generado
    print("\nExplicación del código generado:")
    print("-" * 35)
    print("1. LOAD_CONST: Carga constantes en la pila")
    print("2. STORE_VAR: Almacena valores en variables")
    print("3. LOAD_VAR: Carga variables en la pila")
    print("4. BINARY_ADD: Realiza operación de suma")
    print("5. RETURN: Retorna valor de la función")

if __name__ == '__main__':
    test_code_generation()
