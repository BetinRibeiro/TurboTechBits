def calcular_media_movel_exponencial(lista, periodo):
    """
    Calcula a Média Móvel Exponencial (MME ou EMA - Exponential Moving Average)
    para uma lista de valores, considerando um determinado período.

    Args:
    - lista (list): Lista de valores para calcular a média móvel exponencial.
    - periodo (int): Número de períodos a serem considerados para o cálculo da média móvel.

    Returns:
    - ema (list): Lista com os valores da média móvel exponencial correspondentes.

    A função calcula a Média Móvel Exponencial para cada elemento da lista de valores
    com base no período fornecido. Utiliza a fórmula da EMA:
    EMA = (ValorAtual - EMA_anterior) * alpha + EMA_anterior
    onde alpha = 2 / (periodo + 1).

    Exemplo de uso:
    >>> calcular_media_movel_exponencial([10, 15, 20, 25, 30], 3)
    [10.0, 12.5, 16.25, 21.125, 26.0625]
    """

    if len(lista) <= 0:
        return []

    ema = []
    alpha = 2 / (periodo + 1)
    ema_anterior = lista[0]  # Define o valor inicial da EMA como o primeiro valor da lista

    for valor in lista:
        # Cálculo da Média Móvel Exponencial para cada elemento da lista
        ema_anterior = alpha * (valor - ema_anterior) + ema_anterior
        ema.append(ema_anterior)

    return ema
