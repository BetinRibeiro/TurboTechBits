import random
import string

def gerar_senha(tamanho=8):
    """
    Gera uma senha aleatória com o tamanho especificado.

    Parâmetros:
    tamanho (int): O tamanho da senha a ser gerada.

    Retorna:
    str: A senha gerada.

    A função utiliza letras maiúsculas, letras minúsculas, dígitos e símbolos de pontuação
    para criar uma senha aleatória. O tamanho mínimo da senha é 4.

    Exemplo de uso:
    >>> gerar_senha(12)
    'aB3!rK$pL9z'
    """
    # Define os caracteres que podem ser usados na senha
    caracteres = string.ascii_letters + string.digits + string.punctuation

    # Garante que o tamanho especificado é pelo menos 4
    tamanho = max(tamanho, 4)

    # Gera a senha aleatoriamente
    senha = ''.join(random.choice(caracteres) for _ in range(tamanho))

    return senha
