import pytest
from src.validador_cadenas import ValidadorDeCadenas


class TestEsPalindromo:
    """Pruebas para el método esPalindromo siguiendo TDD"""
    
    def setup_method(self):
        """Se ejecuta antes de cada prueba"""
        self.validador = ValidadorDeCadenas()
    
    # CICLO 1: Caso más simple
    def test_palindromo_simple(self):
        """Prueba con un palíndromo simple: 'oso'"""
        assert self.validador.es_palindromo("oso") == True
    
    # CICLO 2: Caso que falle
    def test_no_palindromo(self):
        """Prueba con una palabra que NO es palíndromo: 'casa'"""
        assert self.validador.es_palindromo("casa") == False
    
    # CICLO 3: Mayúsculas, minúsculas y espacios
    def test_palindromo_con_espacios_y_mayusculas(self):
        """Prueba con frase palíndroma: 'Anita lava la tina'"""
        assert self.validador.es_palindromo("Anita lava la tina") == True
    
    def test_palindromo_mayusculas(self):
        """Prueba con mayúsculas: 'Oso'"""
        assert self.validador.es_palindromo("Oso") == True
    
    # Casos límite
    def test_cadena_vacia(self):
        """Prueba con cadena vacía"""
        assert self.validador.es_palindromo("") == True
    
    def test_una_letra(self):
        """Prueba con una sola letra"""
        assert self.validador.es_palindromo("a") == True
    
    def test_cadena_none(self):
        """Prueba con None - debe lanzar excepción o retornar False"""
        assert self.validador.es_palindromo(None) == False
    
    def test_palindromo_con_tildes(self):
        """Prueba con tildes"""
        assert self.validador.es_palindromo("Anilina") == True


class TestContarVocales:
    """Pruebas para el método contarVocales siguiendo TDD"""
    
    def setup_method(self):
        self.validador = ValidadorDeCadenas()
    
    def test_cadena_sin_vocales(self):
        """Prueba con cadena sin vocales"""
        assert self.validador.contar_vocales("xyz") == 0
    
    def test_cadena_solo_vocales(self):
        """Prueba con solo vocales"""
        assert self.validador.contar_vocales("aeiou") == 5
    
    def test_cadena_mixta(self):
        """Prueba con cadena mixta"""
        assert self.validador.contar_vocales("Hola Mundo") == 4
    
    def test_vocales_mayusculas_minusculas(self):
        """Prueba con vocales en mayúsculas y minúsculas"""
        assert self.validador.contar_vocales("AEIOUaeiou") == 10
    
    def test_cadena_vacia(self):
        """Prueba con cadena vacía"""
        assert self.validador.contar_vocales("") == 0
    
    def test_cadena_none(self):
        """Prueba con None"""
        assert self.validador.contar_vocales(None) == 0
    
    def test_cadena_con_numeros(self):
        """Prueba con números y caracteres especiales"""
        assert self.validador.contar_vocales("Hola123!@#") == 2
    
    def test_vocales_con_tildes(self):
        """Prueba con vocales acentuadas"""
        assert self.validador.contar_vocales("áéíóú") == 5


class TestInvertirCadena:
    """Pruebas para el método invertirCadena siguiendo TDD"""
    
    def setup_method(self):
        self.validador = ValidadorDeCadenas()
    
    def test_invertir_cadena_simple(self):
        """Prueba con cadena simple"""
        assert self.validador.invertir_cadena("hola") == "aloh"
    
    def test_invertir_cadena_par(self):
        """Prueba con cadena de longitud par"""
        assert self.validador.invertir_cadena("casa") == "asac"
    
    def test_invertir_cadena_impar(self):
        """Prueba con cadena de longitud impar"""
        assert self.validador.invertir_cadena("mundo") == "odnum"
    
    def test_invertir_una_letra(self):
        """Prueba con una sola letra"""
        assert self.validador.invertir_cadena("a") == "a"
    
    def test_invertir_cadena_vacia(self):
        """Prueba con cadena vacía"""
        assert self.validador.invertir_cadena("") == ""
    
    def test_invertir_cadena_con_espacios(self):
        """Prueba con espacios"""
        assert self.validador.invertir_cadena("hola mundo") == "odnum aloh"
    
    def test_invertir_cadena_none(self):
        """Prueba con None"""
        assert self.validador.invertir_cadena(None) == ""
    
    def test_invertir_cadena_con_numeros(self):
        """Prueba con números"""
        assert self.validador.invertir_cadena("abc123") == "321cba"