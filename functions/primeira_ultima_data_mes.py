
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
