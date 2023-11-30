def calcular_soma_registros(empresa_id, tipo, status):
    """
    Calcula a soma dos valores dos registros financeiros de uma empresa
    com base no tipo e status especificados.

    Args:
    - empresa_id (int): ID da empresa cujos registros financeiros serão analisados.
    - tipo (str): Tipo de registro financeiro a ser considerado.
    - status (bool): Status de liquidação dos registros financeiros (True para liquidado, False para não liquidado).

    Returns:
    - soma_total (float): Soma total dos valores dos registros financeiros encontrados.

    Esta função consulta a tabela de registros financeiros de uma empresa,
    filtrando-os pelo ID da empresa, tipo de registro e status de liquidação.
    Em seguida, calcula a soma dos valores desses registros e a retorna.

    Exemplo de uso:
    >>> calcular_soma_registros(123, 'Despesa', True)
    1500.0
    """

    # Consulta os registros financeiros da empresa com o tipo e status especificados
    registros = db((db.registro_financeiro.empresa == empresa_id) &
                   (db.registro_financeiro.tipo == tipo) &
                   (db.registro_financeiro.liquidado == status)).select(db.registro_financeiro.valor)

    # Calcula a soma dos valores dos registros encontrados
    soma_total = sum(registro.valor for registro in registros)

    return soma_total

from datetime import datetime, timedelta
import calendar

def calcular_mes_referencia(meses):
    """
    Calcula o mês de referência com base no número de meses fornecido.

    Parâmetros:
    meses (int): O número de meses a serem deslocados. Positivo para meses no futuro, negativo para meses no passado.

    Retorna:
    tuple: Uma tupla contendo duas datas - a primeira data do mês de referência e a última data do mês de referência.

    A função utiliza a biblioteca `datetime` para manipular datas e a função `calendar.monthrange()`
    para obter o último dia do mês de referência. O parâmetro `meses` define o deslocamento
    em relação ao mês atual.

    Exemplo de uso:
    >>> calcular_mes_referencia(2)
    (datetime.date(2023, 11, 1), datetime.date(2023, 11, 30))
    >>> calcular_mes_referencia(-1)
    (datetime.date(2023, 8, 1), datetime.date(2023, 8, 31))
    """
    # Obtém a data atual
    data_atual = datetime.now()
    
    # Calcula o mês de referência
    mes_referencia = data_atual + timedelta(days=30 * meses)
    
    # Define o primeiro dia do mês de referência
    primeiro_dia = mes_referencia.replace(day=1)
    
    # Obtém o último dia do mês de referência
    ultimo_dia = datetime(
        mes_referencia.year,
        mes_referencia.month,
        calendar.monthrange(mes_referencia.year, mes_referencia.month)[1]
    )
    
    return primeiro_dia, ultimo_dia


def calcular_soma_registros_mes(empresa_id, mes, tipo, status):
    """
    Calcula a soma dos valores dos registros financeiros de uma empresa
    para um determinado mês, considerando o tipo e status especificados.

    Args:
    - empresa_id (int): ID da empresa cujos registros financeiros serão analisados.
    - mes (str): Mês de referência para calcular a soma dos registros (por extenso ou numérico).
    - tipo (str): Tipo de registro financeiro a ser considerado.
    - status (bool): Status de liquidação dos registros financeiros (True para liquidado, False para não liquidado).

    Returns:
    - soma_total (float): Soma total dos valores dos registros financeiros encontrados para o mês especificado.

    Esta função calcula o intervalo de datas para o mês de referência,
    consulta a tabela de registros financeiros da empresa para o intervalo de datas do mês,
    filtrando-os pelo ID da empresa, tipo de registro, status de liquidação e data de pagamento.
    Em seguida, calcula a soma dos valores desses registros e a retorna.

    Exemplo de uso:
    >>> calcular_soma_registros_mes(123, 'Janeiro', 'Despesa', True)
    1500.0
    """
    # Calcula o intervalo de datas do mês de referência
    primeiro_dia, ultimo_dia = calcular_mes_referencia(mes)
    
    # Consulta os registros financeiros da empresa com o tipo e status dentro do intervalo de datas do mês
    registros = db((db.registro_financeiro.empresa == empresa_id) &
                   (db.registro_financeiro.tipo == tipo) &
                   (db.registro_financeiro.liquidado == status) &
                   (db.registro_financeiro.data_pagamento >= primeiro_dia) &
                   (db.registro_financeiro.data_pagamento <= ultimo_dia)).select(db.registro_financeiro.valor)

    # Calcula a soma dos valores dos registros encontrados
    soma_total = sum(registro.valor for registro in registros)

    return soma_total
