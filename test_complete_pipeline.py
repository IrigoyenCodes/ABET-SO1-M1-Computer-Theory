#!/usr/bin/env python3
"""
Test completo del pipeline de compilación con código válido
"""

from main import LexicalAnalyzer, Parser, SemanticAnalyzer, CodeGenerator, VirtualMachine

def test_complete_pipeline():
    """Prueba completa del pipeline con código sin errores"""
    
    # Código de prueba completamente válido
    source_code = '''
int main() {
    int x = 10;
    int y = 20;
    int result = x + y;
    
    if (result > 15) {
        int temp = 5;
        result = result + temp;
    }
    
    return result;
}
'''
    
    print("=" * 80)
    print("TEST COMPLETO DEL PIPELINE DE COMPILACIÓN")
    print("=" * 80)
    
    # Inicializar todos los componentes
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    codegen = CodeGenerator()
    vm = VirtualMachine()
    
    print("\n1. ANÁLISIS LÉXICO")
    print("-" * 40)
    lexer.analyze(source_code)
    print(f"✅ Tokens generados: {len(lexer.tokens)}")
    print(f"✅ Errores léxicos: {len(lexer.errors)}")
    
    print("\n2. ANÁLISIS SEMÁNTICO")
    print("-" * 40)
    semantic_errors = semantic.analyze(lexer.tokens)
    print(f"✅ Variables declaradas: {sum(len(symbols) for symbols in semantic.scopes.values())}")
    print(f"✅ Errores semánticos: {len(semantic_errors)}")
    
    if semantic_errors:
        print("❌ Errores semánticos detectados:")
        for error in semantic_errors:
            print(f"   - {error}")
        return
    
    print("\n3. PARSING (AST)")
    print("-" * 40)
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    print(f"✅ AST construido: {ast.type}")
    print(f"✅ Nodos totales: {count_nodes(ast)}")
    print(f"✅ Errores parsing: {len(parser.errors)}")
    
    if parser.errors:
        print("❌ Errores de parsing detectados:")
        for error in parser.errors:
            print(f"   - {error}")
        return
    
    print("\n4. GENERACIÓN DE CÓDIGO")
    print("-" * 40)
    instructions = codegen.generate(ast)
    print(f"✅ Instrucciones TAC: {len(instructions)}")
    
    print("\n5. EJECUCIÓN EN MÁQUINA VIRTUAL")
    print("-" * 40)
    vm.load_instructions(instructions)
    vm.run()
    print(f"✅ Ejecución completada")
    print(f"✅ Variables en memoria: {len(vm.memory)}")
    print(f"✅ Estado final VM: {vm.memory}")
    
    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE LA COMPILACIÓN")
    print("=" * 80)
    
    print(f"📊 ESTADÍSTICAS:")
    print(f"   • Tokens procesados: {len(lexer.tokens)}")
    print(f"   • Variables declaradas: {sum(len(symbols) for symbols in semantic.scopes.values())}")
    print(f"   • Nodos AST: {count_nodes(ast)}")
    print(f"   • Instrucciones TAC: {len(instructions)}")
    print(f"   • Variables en ejecución: {len(vm.memory)}")
    
    print(f"\n🔍 RESULTADOS:")
    if 'result' in vm.memory:
        print(f"   • Resultado final: {vm.memory['result']}")
    if 'x' in vm.memory and 'y' in vm.memory:
        print(f"   • x = {vm.memory['x']}, y = {vm.memory['y']}")
    if vm.stack:
        print(f"   • Valor de retorno: {vm.stack[-1]}")
    
    print(f"\n✅ PIPELINE COMPLETADO EXITOSAMENTE")
    
    # Mostrar el bytecode generado
    print(f"\n📝 BYTECODE GENERADO:")
    print("-" * 50)
    for i, instr in enumerate(instructions):
        if instr.operand:
            print(f"  {i:2d}: {instr.opcode:<15} {instr.operand}")
        else:
            print(f"  {i:2d}: {instr.opcode:<15}")

def count_nodes(node):
    """Cuenta recursivamente los nodos del AST"""
    count = 1
    for child in node.children:
        count += count_nodes(child)
    return count

def test_simple_math():
    """Prueba simple de operaciones matemáticas"""
    
    print(f"\n{'='*80}")
    print("TEST SIMPLE: OPERACIONES MATEMÁTICAS")
    print("=" * 80)
    
    source_code = '''
int main() {
    int a = 5;
    int b = 3;
    int c = a + b;
    return c;
}
'''
    
    # Pipeline completo
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    codegen = CodeGenerator()
    vm = VirtualMachine()
    
    # Ejecutar pipeline
    lexer.analyze(source_code)
    semantic.analyze(lexer.tokens)
    
    parser = Parser(lexer.tokens)
    ast = parser.parse()
    instructions = codegen.generate(ast)
    vm.load_instructions(instructions)
    vm.run()
    
    print(f"Código: 5 + 3 = {vm.memory.get('c', 'ERROR')}")
    print(f"Memoria: {vm.memory}")
    print(f"Retorno: {vm.stack[-1] if vm.stack else 'EMPTY'}")

if __name__ == '__main__':
    test_complete_pipeline()
    test_simple_math()
