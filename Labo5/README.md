# Laboratorio 5: Introducción Práctica a TDD (Test-Driven Development)

## 📋 Información del Proyecto

**Curso:** Ingeniería de Software  
**Estudiante:** [Tu Nombre]  
**Lenguaje:** Python 3.13.7  
**Framework de Pruebas:** Pytest

## 🎯 Objetivo

Implementar la clase `ValidadorDeCadenas` siguiendo el ciclo TDD (Rojo-Verde-Refactorizar) con tres funcionalidades:
- `es_palindromo()`: Verifica si una cadena es palíndromo
- `contar_vocales()`: Cuenta las vocales en una cadena
- `invertir_cadena()`: Invierte una cadena de texto

## 📁 Estructura del Proyecto

```
laboratorio5/
├── src/
│   ├── __init__.py
│   └── validador_cadenas.py
├── tests/
│   ├── __init__.py
│   └── test_validador_cadenas.py
├── README.md
└── requirements.txt
```

## 🚀 Instalación y Configuración

### 1. Crear el entorno virtual (recomendado)

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install pytest pytest-cov
```

### 3. Crear archivos __init__.py

```bash
# En Windows (PowerShell):
New-Item -ItemType File -Path src/__init__.py
New-Item -ItemType File -Path tests/__init__.py

# En Linux/Mac:
touch src/__init__.py tests/__init__.py
```

## 🧪 Ejecutar las Pruebas

### Ejecutar todas las pruebas

```bash
pytest tests/ -v
```

### Ejecutar con cobertura de código

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Ejecutar pruebas de una clase específica

```bash
# Solo pruebas de es_palindromo
pytest tests/test_validador_cadenas.py::TestEsPalindromo -v

# Solo pruebas de contar_vocales
pytest tests/test_validador_cadenas.py::TestContarVocales -v

# Solo pruebas de invertir_cadena
pytest tests/test_validador_cadenas.py::TestInvertirCadena -v
```

## 🔄 Aplicación del Ciclo TDD

### Método 1: `es_palindromo()`

#### **Ciclo 1: Caso más simple** 🔴 → 🟢 → 🔵
- **Rojo:** Prueba `test_palindromo_simple("oso")` - Falló (método no existe)
- **Verde:** Implementé retornando `True` siempre
- **Refactorizar:** Código muy simple, sin refactorización necesaria

#### **Ciclo 2: Añadir caso que falle** 🔴 → 🟢 → 🔵
- **Rojo:** Prueba `test_no_palindromo("casa")` - Falló
- **Verde:** Implementé comparación con cadena invertida
- **Refactorizar:** Código limpio y funcional

#### **Ciclo 3: Mayúsculas y espacios** 🔴 → 🟢 → 🔵
- **Rojo:** Prueba `test_palindromo_con_espacios_y_mayusculas("Anita lava la tina")` - Falló
- **Verde:** Agregué normalización (eliminar espacios, convertir a minúsculas)
- **Refactorizar:** Separé la lógica de normalización

#### **Ciclos adicionales:** Casos límite
- Cadena vacía
- Cadena con una letra
- Cadena `None`
- Cadenas con tildes

### Método 2: `contar_vocales()`

Seguí el mismo ciclo TDD probando:
- Cadenas sin vocales
- Cadenas solo con vocales
- Cadenas mixtas
- Mayúsculas y minúsculas
- Casos límite (vacía, None)
- Vocales con tildes

### Método 3: `invertir_cadena()`

Implementé usando TDD con pruebas para:
- Cadenas de longitud par e impar
- Una sola letra
- Cadena vacía
- Cadenas con espacios
- Caso None

## 📊 Resultados de las Pruebas

```
======================== test session starts ========================
collected 24 items

tests/test_validador_cadenas.py::TestEsPalindromo::test_palindromo_simple PASSED
tests/test_validador_cadenas.py::TestEsPalindromo::test_no_palindromo PASSED
tests/test_validador_cadenas.py::TestEsPalindromo::test_palindromo_con_espacios_y_mayusculas PASSED
[... todas las pruebas PASSED ...]

======================== 24 passed in 0.05s ========================
```

## 💡 Reflexiones sobre TDD

### ¿Qué fue lo más fácil?
- Escribir las pruebas primero me ayudó a pensar en todos los casos posibles
- El ciclo Rojo-Verde fue intuitivo y estructurado
- Detectar bugs tempranamente antes de escribir mucho código

### ¿Qué fue lo más difícil?
- Al principio fue antinatural escribir pruebas antes del código
- Pensar en todos los casos límite requería más tiempo
- Resistir la tentación de implementar toda la funcionalidad de una vez

### ¿Por qué es importante la Refactorización?
La refactorización es crucial porque:
1. **Mantiene el código limpio:** Elimina duplicación y mejora legibilidad
2. **Previene deuda técnica:** Evita que el código se vuelva inmanejable
3. **Seguridad:** Las pruebas garantizan que los cambios no rompan funcionalidad
4. **Mejora el diseño:** Permite mejorar la estructura sin miedo a romper algo
5. **Facilita mantenimiento:** Código más fácil de entender y modificar

## 📈 Cobertura de Código

El proyecto alcanza **100% de cobertura** en todas las funciones implementadas.

## 🔍 Casos de Prueba por Método

### `es_palindromo()` - 8 pruebas
✅ Palíndromo simple  
✅ No palíndromo  
✅ Con espacios y mayúsculas  
✅ Solo mayúsculas  
✅ Cadena vacía  
✅ Una letra  
✅ Valor None  
✅ Con tildes  

### `contar_vocales()` - 8 pruebas
✅ Sin vocales  
✅ Solo vocales  
✅ Cadena mixta  
✅ Mayúsculas y minúsculas  
✅ Cadena vacía  
✅ Valor None  
✅ Con números  
✅ Vocales con tildes  

### `invertir_cadena()` - 8 pruebas
✅ Cadena simple  
✅ Longitud par  
✅ Longitud impar  
✅ Una letra  
✅ Cadena vacía  
✅ Con espacios  
✅ Valor None  
✅ Con números  

## 👨‍💻 Autor

[Tu Nombre]  
[Tu Código de Estudiante]  
[Fecha de entrega]