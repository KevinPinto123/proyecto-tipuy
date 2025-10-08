# validador_cadenas.py

class ValidadorDeCadenas:
    """
    Clase para validar y analizar cadenas de texto.
    """
    
    def esPalindromo(self, cadena):
        """
        Verifica si una cadena es un palíndromo.
        Ignora espacios y diferencias entre mayúsculas/minúsculas.
        
        Args:
            cadena (str): La cadena a verificar
            
        Returns:
            bool: True si es palíndromo, False si no lo es
        """
        # Procesar: minúsculas y sin espacios
        cadena_limpia = cadena.lower().replace(" ", "")
        
        # Comparar con su versión invertida
        return cadena_limpia == cadena_limpia[::-1]
    
    # validador_cadenas.py
    
  #  def invertirCadena(self, cadena):
   #     """Por ahora devolvemos 'aloh' para pasar la prueba"""
 #       return "aloh"
    
    def invertirCadena(self, cadena):
        """
        Invierte una cadena de texto.
        Args:
        cadena (str): La cadena a invertir
        Returns:
        str: La cadena invertida
        """
        return cadena[::-1]