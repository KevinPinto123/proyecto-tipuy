class ValidadorDeCadenas:
    """
    Clase de utilidad para validar y analizar cadenas de texto.
    Implementada siguiendo el ciclo TDD (Rojo-Verde-Refactorizar).
    """
    
    def es_palindromo(self, cadena):
        """
        Verifica si una cadena es un palíndromo.
        
        Un palíndromo se lee igual de izquierda a derecha que de derecha a izquierda,
        ignorando mayúsculas/minúsculas y espacios.
        
        Args:
            cadena (str): La cadena a verificar
            
        Returns:
            bool: True si es palíndromo, False en caso contrario
            
        Examples:
            >>> validador = ValidadorDeCadenas()
            >>> validador.es_palindromo("oso")
            True
            >>> validador.es_palindromo("Anita lava la tina")
            True
            >>> validador.es_palindromo("casa")
            False
        """
        # Manejar casos especiales
        if cadena is None:
            return False
        
        # Normalizar la cadena: eliminar espacios y convertir a minúsculas
        cadena_normalizada = cadena.replace(" ", "").lower()
        
        # Comparar la cadena con su versión invertida
        return cadena_normalizada == cadena_normalizada[::-1]
    
    def contar_vocales(self, cadena):
        """
        Cuenta el número de vocales en una cadena.
        
        Considera vocales: a, e, i, o, u (mayúsculas y minúsculas)
        También cuenta vocales acentuadas: á, é, í, ó, ú
        
        Args:
            cadena (str): La cadena a analizar
            
        Returns:
            int: Número de vocales encontradas
            
        Examples:
            >>> validador = ValidadorDeCadenas()
            >>> validador.contar_vocales("Hola Mundo")
            4
            >>> validador.contar_vocales("aeiou")
            5
        """
        # Manejar casos especiales
        if cadena is None:
            return 0
        
        # Definir las vocales (con y sin tilde)
        vocales = "aeiouAEIOUáéíóúÁÉÍÓÚ"
        
        # Contar vocales
        contador = 0
        for caracter in cadena:
            if caracter in vocales:
                contador += 1
        
        return contador
    
    def invertir_cadena(self, cadena):
        """
        Invierte una cadena de texto.
        
        Args:
            cadena (str): La cadena a invertir
            
        Returns:
            str: La cadena invertida
            
        Examples:
            >>> validador = ValidadorDeCadenas()
            >>> validador.invertir_cadena("hola")
            'aloh'
            >>> validador.invertir_cadena("mundo")
            'odnum'
        """
        # Manejar casos especiales
        if cadena is None:
            return ""
        
        # Invertir la cadena usando slicing
        return cadena[::-1]