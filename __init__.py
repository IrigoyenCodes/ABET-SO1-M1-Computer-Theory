"""
Test suite for the lexical and semantic analyzer.

This package contains comprehensive tests for all components of the compiler:
- Lexical analysis tests
- Parser tests  
- Semantic analysis tests
- Code generation tests
- Virtual machine tests
- Integration tests
"""

__version__ = "1.0.0"
__author__ = "Santiago Patricio Irigoyen Vazquez"

"""
LIMITACIONES DEL PROGRAMA:

El analizador léxico y compilador presenta limitaciones significativas debido a su naturaleza educativa: 
soporta solo un subconjunto muy reducido de C sin punteros, arreglos ni structs; implementa un parser 
simplista con gramática incompleta y recuperación de errores básica; el análisis semántico no verifica 
tipos complejos ni ámbitos anidados; la generación de bytecode es primitiva sin optimización; la máquina 
virtual ejecuta solo operaciones aritméticas básicas; y la arquitectura monolítica en un solo archivo 
dificulta el mantenimiento y escalabilidad. Aunque excelente como demostración conceptual de compilación, 
es inadecuado para análisis de código C real o producción industrial.
"""
