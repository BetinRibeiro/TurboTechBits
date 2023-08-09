def retorno_pagina(nome_controlador):
    """
    Função para obter o nome do controlador de retorno de uma página anterior.

    Esta função recebe o nome de um controlador de página atual e retorna o nome do controlador
    de página anterior, de acordo com um dicionário de mapeamento.

    Args:
        nome_controlador (str): O nome do controlador da página atual.

    Returns:
        str: O nome do controlador da página anterior.
    """
    # Dicionário de mapeamento para controladores de página
    dicionario = {
        "pagina3": "pagina2",
        "pagina2": "pagina1",
        "pagina1": "pagina0",
        # Adicione mais mapeamentos conforme necessário
    }
    
    # Obtém o nome do controlador de página anterior do dicionário
    retorno = dicionario.get(nome_controlador)
    
    return retorno
