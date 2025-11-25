#!/usr/bin/env python3
"""
Test independiente del Analizador Léxico
"""

from main import LexicalAnalyzer

def test_lexical_analyzer():
    """Prueba del analizador léxico con código de ejemplo"""
    
    # Código de prueba sin errores
    source_code = '''
int main() {
    int numero = 10;
    float precio = 99.99;
    char letra = 'A';
    int suma = 0;
    
    if (numero > 5) {
        suma = numero + 100;
    }
    
    return 0;
}
'''
    
    print("=" * 60)
    print("TEST DEL ANALIZADOR LÉXICO")
    print("=" * 60)
    
    # Inicializar el analizador léxico
    lexer = LexicalAnalyzer()
    
    # Realizar análisis léxico
    lexer.analyze(source_code)
    
    # Mostrar resultados
    print(f"\nTotal de tokens encontrados: {len(lexer.tokens)}")
    print(f"Errores léxicos: {len(lexer.errors)}")
    
    print("\nTokens generados:")
    print("-" * 50)
    for i, token in enumerate(lexer.tokens[:15]):  # Mostrar primeros 15
        print(f"{i:2d}: {token['type']:12} | {token['value']:15} | Línea: {token['line']:2}, Col: {token['column']:2}")
    
    if len(lexer.tokens) > 15:
        print(f"... y {len(lexer.tokens) - 15} tokens más")
    
    # Mostrar errores si hay
    if lexer.errors:
        print("\nErrores léxicos encontrados:")
        for error in lexer.errors:
            print(f"  - {error}")
    else:
        print("\n✅ No se encontraron errores léxicos")
    
    # Estadísticas por tipo de token
    token_types = {}
    for token in lexer.tokens:
        token_types[token['type']] = token_types.get(token['type'], 0) + 1
    
    print("\nEstadísticas de tokens:")
    print("-" * 30)
    for token_type, count in sorted(token_types.items()):
        print(f"{token_type:15}: {count:3d}")

if __name__ == '__main__':
    test_lexical_analyzer()
