#!/usr/bin/env python3
"""
Test independiente de la Máquina Virtual
"""

from main import LexicalAnalyzer, Parser, CodeGenerator, VirtualMachine, Instruction, OpCode

def test_virtual_machine():
    """Prueba de la máquina virtual con código completo"""
    
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
    print("TEST DE LA MÁQUINA VIRTUAL")
    print("=" * 60)
    
    # Pipeline completo
    lexer = LexicalAnalyzer()
    parser = Parser([])
    codegen = CodeGenerator()
    vm = VirtualMachine()
    
    # Análisis léxico
    lexer.analyze(source_code)
    print(f"Tokens: {len(lexer.tokens)}")
    
    # Parsing
    parser.tokens = lexer.tokens
    ast = parser.parse()
    
    if parser.errors:
        print("❌ Errores en parsing - no se puede ejecutar")
        return
    
    # Generación de código
    instructions = codegen.generate(ast)
    print(f"Instrucciones: {len(instructions)}")
    
    # Cargar y ejecutar en VM
    vm.load_instructions(instructions)
    
    print("\nEstado inicial de la VM:")
    print("-" * 30)
    print(f"  Pila: {vm.stack}")
    print(f"  Memoria: {vm.memory}")
    print(f"  Instruction Pointer: {vm.instruction_pointer}")
    
    print("\nEjecutando programa...")
    print("-" * 20)
    
    # Ejecutar con traza
    vm.run()
    
    print("\nEstado final de la VM:")
    print("-" * 30)
    print(f"  Pila: {vm.stack}")
    print(f"  Memoria: {vm.memory}")
    print(f"  Instruction Pointer: {vm.instruction_pointer}")
    print(f"  En ejecución: {vm.running}")
    
    # Análisis de resultados
    print("\nAnálisis de la ejecución:")
    print("-" * 25)
    
    if 'result' in vm.memory:
        print(f"✅ Variable 'result': {vm.memory['result']}")
        expected = 30  # 10 + 20
        if vm.memory['result'] == expected:
            print(f"✅ Resultado correcto: {expected}")
        else:
            print(f"❌ Resultado incorrecto. Esperado: {expected}, Obtenido: {vm.memory['result']}")
    
    if 'x' in vm.memory and 'y' in vm.memory:
        print(f"✅ Variables x={vm.memory['x']}, y={vm.memory['y']}")
    
    if vm.stack:
        print(f"✅ Valor de retorno en pila: {vm.stack[-1]}")
    
    # Estadísticas de ejecución
    print("\nEstadísticas:")
    print(f"  - Instrucciones ejecutadas: {len(instructions)}")
    print(f"  - Variables creadas: {len(vm.memory)}")
    print(f"  - Operaciones en pila: {len(vm.stack)}")

def test_vm_manual():
    """Prueba manual de la VM con instrucciones específicas"""
    
    print("\n" + "=" * 60)
    print("TEST MANUAL DE LA MÁQUINA VIRTUAL")
    print("=" * 60)
    
    # Crear instrucciones manualmente: 5 + 3 = 8
    instructions = [
        Instruction(OpCode.LOAD_CONST, 5),
        Instruction(OpCode.STORE_VAR, 'a'),
        Instruction(OpCode.LOAD_CONST, 3),
        Instruction(OpCode.STORE_VAR, 'b'),
        Instruction(OpCode.LOAD_VAR, 'a'),
        Instruction(OpCode.LOAD_VAR, 'b'),
        Instruction(OpCode.BINARY_ADD),
        Instruction(OpCode.STORE_VAR, 'result'),
    ]
    
    vm = VirtualMachine()
    vm.load_instructions(instructions)
    
    print("Instrucciones manuales: 5 + 3 = 8")
    for i, instr in enumerate(instructions):
        print(f"  {i}: {instr}")
    
    print("\nEjecutando...")
    vm.run()
    
    print(f"\nResultado: {vm.memory.get('result', 'No encontrado')}")
    print(f"Memoria completa: {vm.memory}")

if __name__ == '__main__':
    test_virtual_machine()
    test_vm_manual()
