#!/usr/bin/env python3
"""
Ejecutor simplificado de tests para diagnóstico
"""

import sys
import os

def run_test_module(module_name):
    """Importa y ejecuta un módulo de test"""
    try:
        if module_name == 'test_lexico':
            from test_lexico import test_lexical_analyzer
            test_lexical_analyzer()
        elif module_name == 'test_semantico':
            from test_semantico import test_semantic_analyzer
            test_semantic_analyzer()
        elif module_name == 'test_parser':
            from test_parser import test_parser
            test_parser()
        elif module_name == 'test_codegen':
            from test_codegen import test_code_generator
            test_code_generator()
        elif module_name == 'test_vm':
            from test_vm import test_virtual_machine
            test_virtual_machine()
        elif module_name == 'test_complete_pipeline':
            from test_complete_pipeline import test_complete_pipeline
            test_complete_pipeline()
        else:
            print(f"❌ Módulo desconocido: {module_name}")
            return False
        
        print(f"✅ {module_name} - COMPLETADO")
        return True
        
    except Exception as e:
        print(f"❌ Error en {module_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 DIAGNÓSTICO DE TESTS")
    print("📍 Directorio:", os.getcwd())
    
    tests = [
        ('test_lexico', 'Analizador Léxico'),
        ('test_semantico', 'Analizador Semántico'),
        ('test_parser', 'Parser y Generación AST'),
        ('test_codegen', 'Generador de Código'),
        ('test_vm', 'Máquina Virtual'),
        ('test_complete_pipeline', 'Pipeline Completo'),
    ]
    
    results = []
    for module_name, description in tests:
        print(f"\n{'='*60}")
        print(f"EJECUTANDO: {description}")
        print(f"{'='*60}")
        
        success = run_test_module(module_name)
        results.append((description, success))
    
    # Resumen
    print(f"\n{'='*60}")
    print("📊 RESUMEN")
    print(f"{'='*60}")
    
    passed = sum(1 for _, success in results if success)
    failed = len(results) - passed
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {description}")
    
    print(f"\n📈 ESTADÍSTICAS:")
    print(f"   • Tests ejecutados: {len(results)}")
    print(f"   • Exitosos: {passed}")
    print(f"   • Fallidos: {failed}")
    print(f"   • Tasa de éxito: {(passed/len(results)*100):.1f}%")
    
    return failed == 0

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
