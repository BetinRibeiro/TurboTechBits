from datetime import datetime, timedelta  # Importa classes para manipulação de data e tempo
from time import sleep  # Importa função para pausar a execução do programa

# Função para calcular a data da próxima parcela
def calcular_proxima_parcela(data_referencia, dia_referencia):
    """
    Calcula a data da próxima parcela com base na data de referência e no dia de referência.

    :param data_referencia: Data inicial a partir da qual a próxima parcela será calculada.
    :param dia_referencia: Dia do mês a ser considerado para a próxima parcela.
    :return: Data da próxima parcela ajustada conforme o mês e o dia.
    """
    mes = data_referencia.month  # Obtém o mês da data de referência
    ano = data_referencia.year  # Obtém o ano da data de referência
    
    # Avança o mês
    if mes == 12:  # Se o mês for dezembro
        novo_mes = 1  # O novo mês será janeiro
        novo_ano = ano + 1  # O ano será incrementado
    else:
        novo_mes = mes + 1  # Incrementa o mês
        novo_ano = ano  # O ano permanece o mesmo
    
    # Verifica o último dia do novo mês
    if novo_mes in [4, 6, 9, 11]:  # Meses com 30 dias
        max_dias = 30
    elif novo_mes == 2:  # Fevereiro
        # Verifica se o ano é bissexto
        if (novo_ano % 4 == 0 and novo_ano % 100 != 0) or (novo_ano % 400 == 0):
            max_dias = 29  # Fevereiro tem 29 dias em anos bissextos
        else:
            max_dias = 28  # Fevereiro tem 28 dias em anos não bissextos
    else:  # Meses com 31 dias
        max_dias = 31
    
    # Ajusta o dia de acordo com o máximo permitido no novo mês
    novo_dia = min(dia_referencia, max_dias)  # O novo dia é o mínimo entre o dia de referência e o máximo permitido
    
    return datetime(novo_ano, novo_mes, novo_dia)  # Retorna a nova data

# Função para gerar as parcelas
def gerar_parcelas(data_inicial, valor_total, num_parcelas):
    """
    Gera as parcelas a partir da data inicial, valor total e número de parcelas.

    :param data_inicial: Data da primeira parcela.
    :param valor_total: Valor total a ser dividido em parcelas.
    :param num_parcelas: Número total de parcelas a serem geradas.
    :return: Lista de dicionários contendo informações sobre cada parcela.
    """
    valor_parcela = valor_total / num_parcelas  # Calcula o valor de cada parcela
    dia_referencia = data_inicial.day  # Obtém o dia da data inicial
    parcelas = []  # Inicializa a lista de parcelas
    
    # Loop para gerar as datas de todas as parcelas
    for i in range(num_parcelas):
        # A primeira parcela é na data inicial
        if i == 0:
            data_parcela = data_inicial  # Define a data da primeira parcela
        else:
            # Calcula a próxima parcela com base na data da última parcela
            data_parcela = calcular_proxima_parcela(parcelas[-1]['data'], dia_referencia)  # Chama a função para calcular a próxima data
        
        # Adiciona informações da parcela à lista
        parcelas.append({
            'parcela': i + 1,  # Número da parcela
            'valor': valor_parcela,  # Valor da parcela
            'data': data_parcela  # Data da parcela
        })
    
    return parcelas  # Retorna a lista de parcelas geradas

# Loop para testar todos os meses do ano de 2024 com 29 ou mais dias
for mes in range(1, 13):  # Meses de 1 a 12
    for dia in [29, 30, 31]:  # Testa dias 29, 30 e 31
        try:
            # Tenta criar a data inicial com o dia especificado
            data_inicial = datetime(2024, mes, dia)  # Cria a data inicial
            valor_total = 1200  # Define o valor total a ser parcelado
            num_parcelas = 12  # Define o número total de parcelas

            # Gera as parcelas
            parcelas = gerar_parcelas(data_inicial, valor_total, num_parcelas)  # Chama a função para gerar as parcelas

            # Imprime as parcelas geradas
            print(f"\nData inicial: {data_inicial.strftime('%d/%m/%Y')} - Gerando 12 parcelas")  # Exibe a data inicial
            for parcela in parcelas:  # Loop para imprimir cada parcela
                print(f"Parcela {parcela['parcela']}: R$ {parcela['valor']:.2f} - Data: {parcela['data'].strftime('%d/%m/%Y')}")  # Imprime informações da parcela
            sleep(5)  # Pausa a execução por 5 segundos
        except ValueError:
            # Caso o dia não exista no mês (ex: 31 de fevereiro), ignora e segue
            continue  # Continua para a próxima iteração
