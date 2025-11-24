
**Autor:** Santiago Patricio Irigoyen Vazquez  
**Matrícula:** 180259  
**Fecha:** Noviembre 2025

---

## Resumen

El presente documento expone la investigación, diseño e implementación de un analizador semántico como componente fundamental en la construcción de compiladores. Se describen los elementos necesarios para su implementación, se presenta el algoritmo general de análisis, se detalla la integración con el analizador sintáctico y se evalúan los resultados obtenidos mediante casos de prueba representativos. El analizador desarrollado permite detectar errores lógicos como variables no declaradas, duplicidad de identificadores e incompatibilidades de tipos, garantizando la coherencia semántica del código fuente.

---

## 1. Introducción

Un analizador semántico es una herramienta fundamental en la construcción de compiladores, encargada de verificar el sentido lógico de los enunciados en un programa fuente, yendo más allá de la corrección sintáctica. Mientras que el analizador sintáctico confirma que el código cumple con las reglas gramaticales del lenguaje, el analizador semántico se enfoca en validar que las construcciones tengan coherencia lógica y significado válido.

Su objetivo principal es garantizar que las declaraciones, tipos y operaciones sean coherentes según las reglas del lenguaje de programación, permitiendo detectar errores como:

- Variables utilizadas sin declaración previa
- Duplicidad de identificadores en el mismo ámbito
- Incompatibilidad de tipos en operaciones y asignaciones
- Llamadas a funciones con argumentos incorrectos
- Uso de variables fuera de su ámbito de visibilidad

El análisis semántico se posiciona como la tercera fase del proceso de compilación, después del análisis léxico y sintáctico, y antes de la generación de código intermedio. Esta ubicación estratégica permite detectar errores lógicos en etapas tempranas del proceso de compilación, evitando la generación de código incorrecto o la propagación de errores a fases posteriores.

---

## 2. Marco Teórico

### 2.1 ¿Qué es un analizador semántico?

El analizador semántico es un componente del compilador que comprueba que cada elemento del programa respete las reglas semánticas del lenguaje. A diferencia del análisis sintáctico, que verifica la estructura gramatical, el análisis semántico evalúa el significado y la coherencia lógica de las construcciones del programa.

Las verificaciones principales que realiza un analizador semántico incluyen:

**Declaración previa de variables:** Asegura que toda variable o función sea declarada antes de su primer uso, evitando referencias a identificadores inexistentes.

**Compatibilidad de tipos:** Verifica que las operaciones se realicen entre tipos de datos compatibles, por ejemplo, que no se intenten sumar cadenas de texto con números enteros sin conversión explícita.

**Correspondencia de argumentos:** Valida que las llamadas a funciones incluyan el número correcto de argumentos y que estos sean del tipo esperado.

**Gestión de ámbitos:** Controla la visibilidad de variables locales y globales, asegurando que cada identificador se utilice dentro de su ámbito válido.

**Prevención de duplicados:** Detecta cuando un identificador se declara múltiples veces dentro del mismo ámbito, lo cual generaría ambigüedad.

### 2.2 Importancia en el proceso de compilación

El análisis semántico constituye un puente crítico entre la verificación estructural (sintaxis) y la generación de código. Sin esta fase, errores lógicos pasarían desapercibidos hasta la ejecución del programa, donde podrían causar comportamientos inesperados, fallos críticos o vulnerabilidades de seguridad.

La detección temprana de errores semánticos:

- Reduce el tiempo de depuración
- Mejora la calidad del código generado
- Facilita la optimización en fases posteriores
- Proporciona mensajes de error más informativos al programador

---

## 3. Elementos Necesarios para Implementar un Analizador Semántico

Para construir un analizador semántico funcional, son indispensables los siguientes componentes estructurales:

### 3.1 Tabla de Símbolos

La tabla de símbolos es una estructura de datos que almacena información sobre todos los identificadores presentes en el programa. Para cada símbolo, se registra:

- **Nombre:** El identificador único de la variable, función o constante
- **Tipo:** El tipo de dato asociado (int, float, string, etc.)
- **Ámbito:** El contexto en el que el símbolo es válido (global, local, función específica)
- **Ubicación:** Línea y columna donde fue declarado, útil para reportar errores
- **Atributos adicionales:** Valor inicial, modificadores (const, static), etc.

La tabla de símbolos permite el seguimiento y la validación de declaraciones y usos a lo largo del programa, facilitando la detección de errores como referencias a variables no declaradas o redeclaraciones.

### 3.2 Gestión de Ámbitos

La gestión de ámbitos (scopes) diferencia las variables locales de las globales y evita conflictos por duplicidad de nombres. Un sistema de ámbitos jerárquico permite:

- **Ámbito global:** Variables accesibles desde cualquier parte del programa
- **Ámbitos locales:** Variables limitadas a bloques específicos (funciones, estructuras de control)
- **Ámbitos anidados:** Bloques dentro de otros bloques, con reglas de visibilidad específicas

La búsqueda de símbolos sigue un orden jerárquico: primero se busca en el ámbito actual, luego en ámbitos padre sucesivos hasta llegar al ámbito global.

### 3.3 Chequeo de Tipos

El chequeo de tipos verifica la compatibilidad de operaciones y asignaciones entre distintos tipos de datos. Esto incluye:

- **Verificación en operaciones aritméticas:** Asegurar que operandos sean numéricos
- **Validación de asignaciones:** Confirmar compatibilidad entre el tipo del valor y el tipo de la variable
- **Conversiones implícitas:** Gestionar promociones automáticas de tipos (int → float)
- **Operaciones lógicas:** Verificar que las condiciones evalúen a valores booleanos

### 3.4 Registro de Errores

El sistema de registro almacena y reporta todos los errores encontrados con detalle de ubicación. Cada error incluye:

- **Mensaje descriptivo:** Explicación clara del problema detectado
- **Ubicación:** Línea y columna en el código fuente
- **Tipo de error:** Clasificación (variable no declarada, tipo incompatible, etc.)
- **Sugerencias:** Posibles soluciones o correcciones

### 3.5 Verificación de Declaraciones y Usos

Este componente confirma que toda variable o función usada esté previamente declarada y que no exista duplicidad dentro del mismo ámbito. Mantiene un registro de:

- Qué identificadores han sido declarados
- En qué ámbito fueron declarados
- Si han sido utilizados antes de su declaración
- Si existen múltiples declaraciones del mismo identificador

---

## 4. Metodología y Flujo de Ejecución

### 4.1 Descripción del Proceso

El proceso de análisis semántico sigue un flujo sistemático que parte de la salida del analizador sintáctico (típicamente un árbol de sintaxis abstracta o AST) y lo enriquece con información semántica validada. El flujo se estructura en las siguientes etapas:

#### Fase 1: Inicialización

Al comenzar el análisis semántico, se inicializan las estructuras de datos necesarias:

```python
# Creación de la tabla de símbolos vacía
symbol_table = {}

# Establecimiento del ámbito global como punto de partida
current_scope = 'global'
scopes = {'global': {}}

# Lista para almacenar errores detectados
errors = []
```

Esta fase prepara el entorno para el análisis, estableciendo el contexto inicial desde el cual se procesará el árbol de sintaxis.

#### Fase 2: Recorrido del Árbol de Sintaxis

El analizador recorre el AST de manera recursiva, procesando cada nodo según su tipo:

**Nodos de declaración:** Se agregan nuevos símbolos a la tabla, verificando que no existan duplicados en el ámbito actual.

**Nodos de uso de variables:** Se verifica que el identificador exista en la tabla de símbolos (en el ámbito actual o en ámbitos padre).

**Nodos de operaciones:** Se valida la compatibilidad de tipos entre los operandos involucrados.

**Nodos de control de flujo:** Se gestionan cambios de ámbito cuando se entra o sale de bloques.

#### Fase 3: Ingreso y Salida de Ámbitos

Cuando el análisis encuentra estructuras que definen nuevos ámbitos (funciones, bloques if/while, etc.), se actualiza la estructura de la tabla de símbolos:

**Ingreso a nuevo ámbito:**

```python
def enter_scope(scope_name):
    current_scope = scope_name
    if scope_name not in scopes:
        scopes[scope_name] = {}
```

**Salida de ámbito:**

```python
def exit_scope():
    current_scope = 'global'  # O al ámbito padre correspondiente
```

Esta gestión permite que variables con el mismo nombre coexistan en diferentes ámbitos sin generar conflictos.

#### Fase 4: Registro de Errores

Durante todo el proceso, cuando se detecta una violación de las reglas semánticas, se documenta el error:

```python
errors.append({
    'type': 'semantic_error',
    'message': 'Variable "x" no declarada',
    'line': 15,
    'column': 8,
    'severity': 'error'
})
```

Los errores se almacenan sin detener el análisis, permitiendo detectar múltiples problemas en una sola pasada.

#### Fase 5: Reporte Final

Al finalizar el recorrido completo del árbol, se genera un reporte que incluye:

- Lista detallada de todos los errores encontrados
- Advertencias sobre posibles problemas (variables declaradas pero no usadas, conversiones implícitas de tipo)
- Estadísticas del análisis (número de símbolos procesados, errores por categoría)
- Tabla de símbolos final con todos los identificadores válidos

### 4.2 Diagrama de Flujo

```
┌─────────────────────────────────┐
│   Inicio del Análisis Semántico │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Inicialización:                │
│  - Tabla de símbolos            │
│  - Ámbito global                │
│  - Lista de errores             │
└───────────────┬─────────────────┘
                │
                ▼
┌─────────────────────────────────┐
│  Recibir AST del analizador     │
│  sintáctico                     │
└───────────────┬─────────────────┘
                │
                ▼
        ┌───────────────┐
        │ Para cada nodo│
        │   en el AST   │
        └───────┬───────┘
                │
                ▼
        ┌───────────────────────┐
        │ ¿Tipo de nodo?        │
        └───┬───────────────┬───┘
            │               │
    ┌───────▼───────┐   ┌──▼──────────┐
    │ Declaración   │   │ Uso de      │
    │               │   │ variable    │
    └───────┬───────┘   └──┬──────────┘
            │               │
            ▼               ▼
    ┌───────────────┐   ┌──────────────┐
    │ ¿Ya existe en │   │ ¿Existe en   │
    │ ámbito actual?│   │ tabla?       │
    └───┬───────┬───┘   └──┬───────┬───┘
        │ Sí    │ No        │ Sí    │ No
        ▼       ▼           ▼       ▼
    ┌───────┐ ┌────────┐ ┌─────┐ ┌──────┐
    │Error: │ │Agregar │ │ OK  │ │Error:│
    │Duplic.│ │símbolo │ │     │ │No    │
    │       │ │        │ │     │ │decl. │
    └───────┘ └────────┘ └─────┘ └──────┘
            │               │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────┐
            │ ¿Operación?   │
            └───────┬───────┘
                    │
                    ▼
            ┌───────────────────┐
            │ Verificar tipos   │
            │ compatibles       │
            └───────┬───────────┘
                    │
                    ▼
            ┌───────────────────┐
            │ ¿Cambio de ámbito?│
            └───┬───────────┬───┘
                │ Entrada   │ Salida
                ▼           ▼
        ┌───────────┐   ┌──────────┐
        │enter_scope│   │exit_scope│
        └───────────┘   └──────────┘
                │           │
                └─────┬─────┘
                      │
                      ▼
            ┌─────────────────────┐
            │ ¿Más nodos?         │
            └─────┬───────────┬───┘
                  │ Sí        │ No
                  └───────┐   │
                          │   │
                          ▼   ▼
                    ┌─────────────────┐
                    │ Generar reporte │
                    │ de errores      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Fin del análisis│
                    └─────────────────┘
```

---

## 5. Algoritmo del Analizador Semántico

El algoritmo general del analizador semántico se estructura como un recorrido sistemático del árbol de sintaxis abstracta, aplicando reglas de validación en cada nodo:

```python
# Pseudocódigo del algoritmo principal
para cada nodo en el árbol de sintaxis:
    
    # Manejo de declaraciones de variables
    si nodo es declaración de variable:
        si variable ya está en tabla de símbolos del ámbito actual:
            reportar error de variable duplicada
            registrar ubicación (línea, columna)
        sino:
            añadir variable a la tabla de símbolos
            almacenar tipo, ámbito y ubicación
    
    # Verificación de uso de variables
    si nodo es uso de variable:
        si variable no está en tabla de símbolos de ámbito actual:
            si variable no está en tabla de símbolos global:
                reportar error de variable no declarada
                registrar ubicación (línea, columna)
            sino:
                marcar como uso válido de variable global
        sino:
            marcar como uso válido de variable local
    
    # Validación de operaciones
    si nodo es operación entre variables:
        obtener tipo de operando izquierdo
        obtener tipo de operando derecho
        si tipos no son compatibles:
            si no existe conversión implícita válida:
                reportar error de incompatibilidad de tipos
                registrar tipos involucrados y ubicación
            sino:
                generar advertencia de conversión implícita
    
    # Gestión de ámbitos
    si nodo es entrada a un nuevo ámbito:
        crear nueva tabla de símbolos para el ámbito
        establecer ámbito actual como padre del nuevo ámbito
        activar nuevo ámbito
    
    si nodo es salida de un ámbito:
        restaurar ámbito padre como ámbito actual
        opcionalmente: eliminar tabla de símbolos del ámbito saliente
    
    # Validación de llamadas a funciones
    si nodo es llamada a función:
        si función no está declarada:
            reportar error de función no declarada
        sino:
            verificar número de argumentos
            verificar tipos de argumentos
            si hay discrepancia:
                reportar error con detalles

# Al finalizar el recorrido
generar reporte consolidado de errores
retornar tabla de símbolos completa
retornar lista de advertencias
```

### 5.1 Reglas de Verificación Detalladas

**Regla 1: Declaración antes de uso**

```
Para toda variable v utilizada en línea L:
    ∃ declaración de v en línea D donde D < L
    Y v está en ámbito visible desde L
```

**Regla 2: Unicidad en ámbito**

```
Para todo ámbito S:
    No existen dos declaraciones de la misma variable v en S
```

**Regla 3: Compatibilidad de tipos**

```
Para toda operación O(a, b):
    tipo(a) compatible con tipo(b) según reglas del lenguaje
    O tipo(a) convertible a tipo(b) implícitamente
```

---

## 6. Implementación del Analizador Semántico

### 6.1 Estructura de la Clase Principal

Se presenta la implementación completa del analizador semántico en Python, estructurada como una clase con métodos especializados:

```python
class SemanticAnalyzer:
    """
    Analizador semántico para verificar la coherencia lógica
    de programas a partir de su árbol de sintaxis abstracta.
    """
    
    def __init__(self):
        """
        Inicializa el analizador con estructuras vacías.
        """
        # Tabla de símbolos general (no usada directamente)
        self.symbol_table = {}
        
        # Ámbito activo actual
        self.current_scope = 'global'
        
        # Diccionario de ámbitos con sus tablas de símbolos
        self.scopes = {'global': {}}
        
        # Lista de errores detectados
        self.errors = []
        
        # Contador de advertencias
        self.warnings = []

    def enter_scope(self, scope_name):
        """
        Ingresa a un nuevo ámbito, creando su tabla de símbolos
        si no existe.
        
        Args:
            scope_name (str): Nombre identificador del nuevo ámbito
        """
        self.current_scope = scope_name
        if scope_name not in self.scopes:
            self.scopes[scope_name] = {}
        print(f"Entrando al ámbito: {scope_name}")

    def exit_scope(self):
        """
        Sale del ámbito actual y regresa al ámbito global.
        En una implementación más robusta, debería regresar
        al ámbito padre en lugar de siempre al global.
        """
        print(f"Saliendo del ámbito: {self.current_scope}")
        self.current_scope = 'global'

    def add_symbol(self, name, symbol_type, line, column):
        """
        Añade un símbolo a la tabla del ámbito actual.
        Verifica que no exista duplicado en el mismo ámbito.
        
        Args:
            name (str): Nombre del identificador
            symbol_type (str): Tipo de dato del símbolo
            line (int): Número de línea donde se declara
            column (int): Número de columna donde se declara
            
        Returns:
            bool: True si se agregó exitosamente, False si ya existía
        """
        # Verificar duplicados en el ámbito actual
        if name in self.scopes[self.current_scope]:
            self.errors.append({
                'type': 'duplicate_declaration',
                'message': f'Variable "{name}" ya ha sido declarada en este ámbito',
                'line': line,
                'column': column,
                'severity': 'error'
            })
            return False
        
        # Agregar el símbolo al ámbito actual
        self.scopes[self.current_scope][name] = {
            'type': symbol_type,
            'declared_at': (line, column),
            'used': False  # Para detectar variables no utilizadas
        }
        print(f"Símbolo '{name}' agregado: tipo={symbol_type}, línea={line}")
        return True

    def check_variable(self, name, line, column):
        """
        Verifica si una variable ha sido declarada antes de su uso.
        Busca primero en el ámbito actual, luego en el global.
        
        Args:
            name (str): Nombre de la variable a verificar
            line (int): Línea donde se usa la variable
            column (int): Columna donde se usa la variable
            
        Returns:
            bool: True si la variable está declarada, False si no
        """
        # Búsqueda en ámbito actual
        if name in self.scopes[self.current_scope]:
            # Marcar la variable como usada
            self.scopes[self.current_scope][name]['used'] = True
            return True
        
        # Búsqueda en ámbito global
        if name in self.scopes['global']:
            self.scopes['global'][name]['used'] = True
            return True
        
        # Variable no encontrada - reportar error
        self.errors.append({
            'type': 'undeclared_variable',
            'message': f'Variable "{name}" no declarada',
            'line': line,
            'column': column,
            'severity': 'error'
        })
        return False

    def check_type(self, name, expected_type, line, column):
        """
        Verifica la compatibilidad de tipos para una variable.
        
        Args:
            name (str): Nombre de la variable
            expected_type (str): Tipo esperado en el contexto
            line (int): Línea donde ocurre la verificación
            column (int): Columna donde ocurre la verificación
            
        Returns:
            bool: True si los tipos son compatibles, False si no
        """
        # Buscar el símbolo en ámbito actual o global
        found = (self.scopes[self.current_scope].get(name) or 
                 self.scopes['global'].get(name))
        
        if not found:
            # Variable no declarada (ya debería haber sido detectado)
            return False
        
        actual_type = found['type']
        
        # Verificar compatibilidad exacta
        if actual_type != expected_type:
            # Verificar si hay conversión implícita válida
            if self._is_implicit_conversion_valid(actual_type, expected_type):
                self.warnings.append({
                    'type': 'implicit_conversion',
                    'message': f'Conversión implícita de {actual_type} a {expected_type} para "{name}"',
                    'line': line,
                    'column': column,
                    'severity': 'warning'
                })
                return True
            else:
                self.errors.append({
                    'type': 'type_mismatch',
                    'message': f'Tipo incompatible para "{name}" - se esperaba {expected_type}, se encontró {actual_type}',
                    'line': line,
                    'column': column,
                    'severity': 'error'
                })
                return False
        
        return True

    def _is_implicit_conversion_valid(self, from_type, to_type):
        """
        Determina si existe una conversión implícita válida entre dos tipos.
        
        Args:
            from_type (str): Tipo origen
            to_type (str): Tipo destino
            
        Returns:
            bool: True si la conversión es válida
        """
        # Reglas de conversión implícita comunes
        conversions = {
            ('int', 'float'): True,
            ('int', 'double'): True,
            ('float', 'double'): True,
            ('char', 'int'): True,
        }
        return conversions.get((from_type, to_type), False)

    def get_error_report(self):
        """
        Genera un reporte formateado de todos los errores detectados.
        
        Returns:
            str: Reporte de errores en formato legible
        """
        if not self.errors and not self.warnings:
            return "✓ Análisis semántico completado sin errores"
        
        report = []
        report.append("=" * 60)
        report.append("REPORTE DE ANÁLISIS SEMÁNTICO")
        report.append("=" * 60)
        
        if self.errors:
            report.append(f"\n❌ ERRORES DETECTADOS ({len(self.errors)}):")
            report.append("-" * 60)
            for i, error in enumerate(self.errors, 1):
                report.append(f"\n{i}. {error['type'].upper()}")
                report.append(f"   Mensaje: {error['message']}")
                report.append(f"   Ubicación: Línea {error['line']}, Columna {error['column']}")
        
        if self.warnings:
            report.append(f"\n⚠️  ADVERTENCIAS ({len(self.warnings)}):")
            report.append("-" * 60)
            for i, warning in enumerate(self.warnings, 1):
                report.append(f"\n{i}. {warning['type'].upper()}")
                report.append(f"   Mensaje: {warning['message']}")
                report.append(f"   Ubicación: Línea {warning['line']}, Columna {warning['column']}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)

    def get_symbol_table_report(self):
        """
        Genera un reporte de la tabla de símbolos.
        
        Returns:
            str: Tabla de símbolos formateada
        """
        report = []
        report.append("=" * 60)
        report.append("TABLA DE SÍMBOLOS")
        report.append("=" * 60)
        
        for scope_name, symbols in self.scopes.items():
            if symbols:
                report.append(f"\nÁmbito: {scope_name}")
                report.append("-" * 60)
                report.append(f"{'Variable':<15} {'Tipo':<10} {'Declarada en':<20} {'Usada':<10}")
                report.append("-" * 60)
                for name, info in symbols.items():
                    line, col = info['declared_at']
                    used = "Sí" if info.get('used', False) else "No"
                    report.append(f"{name:<15} {info['type']:<10} Línea {line}, Col {col:<8} {used:<10}")
        
        report.append("\n" + "=" * 60)
        return "\n".join(report)
```

### 6.2 Ejemplo de Uso del Analizador

```python
# Crear instancia del analizador
analyzer = SemanticAnalyzer()

# Simular declaraciones y usos
analyzer.add_symbol('x', 'int', 1, 5)
analyzer.add_symbol('y', 'float', 2, 8)

# Verificar uso de variables
analyzer.check_variable('x', 3, 10)  # Válido
analyzer.check_variable('z', 3, 15)  # Error: no declarada

# Verificar tipos
analyzer.check_type('x', 'int', 4, 5)    # Válido
analyzer.check_type('y', 'int', 4, 10)   # Advertencia: conversión

# Generar reportes
print(analyzer.get_error_report())
print(analyzer.get_symbol_table_report())
```

---

## 7. Integración del Analizador Sintáctico con el Semántico

### 7.1 Flujo de Integración

El analizador semántico se integra con el analizador sintáctico de la siguiente manera:

```
┌──────────────────────┐
│   Código Fuente      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Analizador Léxico    │
│ (Genera tokens)      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Analizador Sintáctico│
│ (Genera AST)         │
└──────────┬───────────┘
           │
           │ AST + Información de tipos
           ▼
┌──────────────────────┐
│ Analizador Semántico │
│ - Tabla de símbolos  │
│ - Chequeo de tipos   │
│ - Gestión de ámbitos │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Código Intermedio    │
│ (Si no hay errores)  │
└──────────────────────┘
```

### 7.2 Interfaz de Comunicación

El analizador sintáctico proporciona al analizador semántico:

1. **Árbol de Sintaxis Abstracta (AST):** Estructura que representa las construcciones del programa
2. **Información de nodos:** Tipo de nodo (declaración, expresión, operación, etc.)
3. **Metadatos:** Línea y columna de cada elemento para reportar errores

### 7.3 Código de Integración

```python
def integrate_syntactic_semantic_analysis(source_code):
    """
    Función que integra el análisis sintáctico con el semántico.
    
    Args:
        source_code (str): Código fuente a analizar
        
    Returns:
        dict: Resultados del análisis completo
    """
    # Fase 1: Análisis Léxico
    lexer = LexicalAnalyzer()
    tokens = lexer.tokenize(source_code)
    
    if lexer.has_errors():
        return {
            'success': False,
            'phase': 'lexical',
            'errors': lexer.get_errors()
        }
    
    # Fase 2: Análisis Sintáctico
    parser = SyntacticAnalyzer()
    ast = parser.parse(tokens)
    
    if parser.has_errors():
        return {
            'success': False,
            'phase': 'syntactic',
            'errors': parser.get_errors
```

---
# Conclusiones

El análisis semántico constituye una fase fundamental dentro de los procesos de compilación. Facilita la transición del árbol de sintaxis abstracta al código intermedio, validando que las construcciones del programa tengan coherencia lógica más allá de su correcta estructura gramatical.

Esta modularidad no solo simplifica el diseño del compilador, sino que también mejora notablemente su robustez y capacidad de detectar errores en etapas tempranas. A través de tablas de símbolos, gestión de ámbitos y verificación de tipos, se logra una validación exhaustiva y precisa, permitiendo detectar errores semánticos que podrían causar fallos en tiempo de ejecución.

Además, la separación clara entre la gestión de declaraciones, tipos, ámbitos y operaciones permite una adaptación sencilla a los requisitos de diferentes lenguajes de programación y facilita el mantenimiento del compilador.

---
# USO DE LA IA 
Durante el desarrollo del analizador semántico, la inteligencia artificial desempeñó un papel estratégico en varios aspectos clave. Se empleó IA para generar rápidamente la estructura inicial del código en Python, asegurando la correcta división modular de la tabla de símbolos, gestión de ámbitos y verificación de tipos.

La IA facilitó la validación y depuración de algoritmos para el reconocimiento de patrones semánticos y detección de errores como variables no declaradas, tipos incompatibles y declaraciones duplicadas, optimizando la eficiencia del análisis y mejorando la precisión en la identificación de problemas semánticos complejos.

Asimismo, se recurrió a IA para generar ejemplos de casos de prueba diversos que abarcan declaraciones, operaciones, ámbitos anidados, funciones y manejo de errores, permitiendo asegurar la robustez del programa y su capacidad de detectar múltiples tipos de errores semánticos.

---
## REFERENCIAS

1. Aho, A. V., Lam, M. S., Sethi, R., Ullman, J. D. (2007). _Compilers: Principles, Techniques, Tools_ (2nd ed.). Pearson/Addison Wesley.
2. Python Software Foundation. (s.f.). _Classes and Objects_. Python 3.11.5 documentation.
3. Runestone Academy. (s.f.). _Trees: Semantic Analysis_. Interactive Python Documentation.
4. Wikipedia. (s.f.). _Análisis semántico (informática)_. Enciclopedia libre.
5. Cooper, K., & Torczon, L. (2011). _Engineering a Compiler_ (2nd ed.). Morgan Kaufmann.
6. Grune, D., van Reeuwijk, K., Bal, H. E., Jacobs, C. J., & Langendoen, K. (2012). _Modern Compiler Design_ (2nd ed.). Springer.