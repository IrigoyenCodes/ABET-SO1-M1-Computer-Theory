#!/usr/bin/env python3
"""
Test independiente del Analizador Semántico
"""

from main import LexicalAnalyzer, SemanticAnalyzer

def test_semantic_analyzer():
    """Prueba del analizador semántico con código válido"""
    
    # Código de prueba sin errores semánticos
    source_code = '''
int main() {
    int numero = 10;
    float precio = 99.99;
    int suma = 0;
    int temporal = 100;
    
    suma = numero + temporal;
    
    return 0;
}
'''
    
    print("=" * 60)
    print("TEST DEL ANALIZADOR SEMÁNTICO")
    print("=" * 60)
    
    # Inicializar analizadores
    lexer = LexicalAnalyzer()
    semantic = SemanticAnalyzer()
    
    # Análisis léxico
    lexer.analyze(source_code)
    print(f"Tokens generados: {len(lexer.tokens)}")
    
    # Análisis semántico
    semantic_errors = semantic.analyze(lexer.tokens)
    
    # Mostrar tabla de símbolos
    print("\nTabla de símbolos construida:")
    print("-" * 60)
    print(f"{'Ámbito':<10} | {'Variable':<15} | {'Tipo':<8} | {'Ubicación':<15}")
    print("-" * 60)
    
    for scope, symbols in semantic.scopes.items():
        if symbols:  # Solo mostrar ámbitos con símbolos
            for name, info in symbols.items():
                line, col = info['declared_at']
                location = f"Línea {line}, Col {col}"
                print(f"{scope:<10} | {name:<15} | {info['type']:<8} | {location:<15}")
    
    # Mostrar errores semánticos
    print(f"\nErrores semánticos encontrados: {len(semantic_errors)}")
    
    if semantic_errors:
        print("\nDetalles de errores:")
        for error in semantic_errors:
            print(f"  - Línea {error['line']}, Columna {error['column']}: {error['message']}")
    else:
        print("✅ No se encontraron errores semánticos")
    
    # Estadísticas del análisis
    print("Estadísticas del análisis:")
    print("-" * 30)
    print(f"Variables declaradas: {sum(len(symbols) for symbols in semantic.scopes.values())}")
    print(f"Ámbitos creados: {len([scope for scope in semantic.scopes.keys() if semantic.scopes[scope]])}")
    print("Tipos soportados: int, float, char, bool")

if __name__ == '__main__':
    test_semantic_analyzer()
