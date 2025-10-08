# test_validador_cadenas.py
from validador_cadenas import ValidadorDeCadenas

def test_palindromo_palabra_simple():
    """Prueba 1: 'oso' es palíndromo"""
    validador = ValidadorDeCadenas()
    resultado = validador.esPalindromo("oso")
    assert resultado == True

def test_palabra_no_palindromo():
    """Prueba 2: 'casa' NO es palíndromo"""
    validador = ValidadorDeCadenas()
    resultado = validador.esPalindromo("casa")
    assert resultado == False

def test_palindromo_con_espacios_y_mayusculas():
    """
    Prueba 3: Frases con espacios y mayúsculas
    'Anita lava la tina' debe ser palíndromo ignorando espacios y mayúsculas
    Esta prueba FALLARÁ porque nuestro código actual no elimina espacios
    """
    validador = ValidadorDeCadenas()
    resultado = validador.esPalindromo("Anita lava la tina")
    assert resultado == True


def test_invertir_cadena_simple():
    """
    Prueba 1: Invertir 'hola' debe dar 'aloh'
    FALLARÁ porque el método no existe
    """
    validador = ValidadorDeCadenas()
    resultado = validador.invertirCadena("hola")
    assert resultado == "aloh"

def test_invertir_cadena_diferente():
    """Prueba 2: Invertir 'Python' debe dar 'nohtyP'"""
    validador = ValidadorDeCadenas()
    resultado = validador.invertirCadena("Python")
    assert resultado == "nohtyP"