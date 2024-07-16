import unidecode
import urllib.parse
from unicodedata import normalize

class StringUtils:
    '''
    Classe utilitária para manipulação de strings.
    '''

    @staticmethod
    def remover_acentuacao(text):
        '''
        Remove acentuação de uma string e a converte para maiúsculas.

        Parâmetros:
        text (str): A string de entrada com acentuação.

        Retorna:
        str: A string sem acentuação e em maiúsculas.
        '''
        text_without_accents = unidecode.unidecode(text)
        return text_without_accents.upper()

    @staticmethod
    def decodificar_url(url_atual):
        '''
        Decodifica a última parte de uma URL codificada.

        Parâmetros:
        url_atual (str): A URL codificada.

        Retorna:
        str: A última parte decodificada da URL.
        '''
        parts = url_atual.split("/")
        ultima_parte = parts[-1]
        string_codificada = ultima_parte
        consul = urllib.parse.unquote(string_codificada)
        return consul
