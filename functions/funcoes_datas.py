

def primeiro_ultimo_dia_do_mes(index):
    """
    Retorna o primeiro e último dia de um mês baseado no índice fornecido, com cache de 10 minutos.

    Args:
        index (int): Índice relativo ao mês atual (0 = mês atual, -1 = mês anterior, etc.).

    Returns:
        tuple: Primeiro e último dia do mês.
    """
    # Definir o limite para index
    max_anos = 100
    index = max(-max_anos * 12, min(max_anos * 12, index))

    # Criar uma chave única para o cache com base no índice
    cache_key = f"primeiro_ultimo_dia_mes_{index}"

    # Função para calcular as datas, usada como fallback no cache
    def calcular_datas():
        # Data atual
        data_atual = datetime.now()

        # Cálculo direto do novo ano e mês
        novo_ano = data_atual.year + (data_atual.month - 1 + index) // 12
        novo_mes = (data_atual.month - 1 + index) % 12 + 1

        # Primeiro dia do mês
        primeiro_dia = datetime(novo_ano, novo_mes, 1)

        # Último dia do mês usando o número de dias do `calendar.monthrange`
        ultimo_dia = datetime(novo_ano, novo_mes, calendar.monthrange(novo_ano, novo_mes)[1])

        return primeiro_dia, ultimo_dia

    # Obter as datas do cache ou calcular se não estiver em cache
    return cache.ram(cache_key, calcular_datas, time_expire=600)





def mes_ano(mes_ano_str):
    """
    Retorna o nome do mês e o ano formatados com base em uma string no formato 'mes.ano' ou 'mes/ano',
    com cache de 10 minutos.

    Args:
        mes_ano_str (str): String contendo mês e ano (ex.: '1/23', '01.2023').

    Returns:
        str: Nome do mês e ano no formato 'NomeDoMês/Ano' (ex.: 'Janeiro/2023').
    """
    # Criar uma chave única para o cache com base no valor da entrada
    cache_key = f"mes_ano_{mes_ano_str}"

    # Função para calcular o resultado, usada como fallback no cache
    def calcular_mes_ano():
        # Mapeia os números dos meses para os nomes em português
        meses = {
            '1': 'Janeiro',
            '2': 'Fevereiro',
            '3': 'Março',
            '4': 'Abril',
            '5': 'Maio',
            '6': 'Junho',
            '7': 'Julho',
            '8': 'Agosto',
            '9': 'Setembro',
            '10': 'Outubro',
            '11': 'Novembro',
            '12': 'Dezembro',
        }

        # Substitui '.' e '/' por um único separador ('.')
        mes_ano_str_normalizado = mes_ano_str.replace('/', '.')

        # Divide a string em mês e ano
        mes, ano = mes_ano_str_normalizado.split('.')

        # Adiciona '20' ao ano somente se ele tiver 2 dígitos
        if len(ano) == 2:
            ano = '20' + ano

        # Retorna o nome do mês e o ano
        return f"{meses[mes]}/{ano}"

    # Obter o resultado do cache ou calcular se não estiver em cache
    return cache.ram(cache_key, calcular_mes_ano, time_expire=600)



def data_referencia(index):
#     try:
    data_atual = request.now.date() + timedelta(days=index)
#     except:
#         return None
    return data_atual



def formatar_data2(data):
    
    try:
        # Se o input já for um datetime, formata diretamente
        if isinstance(data, datetime):
            return data.strftime('%d/%m/%y')
        # Se for uma string, tenta convertê-la para datetime primeiro
        data = datetime.strptime(data, '%Y-%m-%d')
        return data.strftime('%d/%m/%y')
    except (ValueError, AttributeError, TypeError):
        # Retorna "ERRO!" em caso de erro
        try:
            date_obj = datetime.strptime(data, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime("%d/%m/%y")
        except:
            return "ERRO"



def formatar_data(data):
    try:
        if data is None:
            return "ERRO!"
        return data.strftime('%d/%m/%Y')
    except AttributeError:
        return "ERRO!"


def formatar_data_dia(data):
    try:
        if data is None:
            return "ERRO!"
        return data.strftime('%d/%m')
    except AttributeError:
        return "ERRO!"



def calcula_diferenca_datas(data_vencimento, data_pagamento):
    try:
        # Converte as strings para objetos datetime
        vencimento = datetime.strptime(data_vencimento, "%d/%m/%y")
        pagamento = datetime.strptime(data_pagamento, "%d/%m/%y")

        # Calcula a diferença de dias
        diferenca = (pagamento - vencimento).days

        return diferenca  # Positivo para atraso, negativo para adiantamento
    except ValueError:
        return "Formato de data inválido. Use DD/MM/YY."
