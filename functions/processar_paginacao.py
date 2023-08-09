
def processar_paginacao(empresa, tabela, paginacao, consulta=None):
    """
    Processa a paginação de registros de uma tabela associada a uma empresa.

    Args:
    empresa (int): O ID da empresa associada aos registros.
    tabela (Table): A tabela do banco de dados à qual a paginação se aplica.
    paginacao (int): O número de registros por página.
    consulta (Expression, optional): Uma expressão de consulta adicional para filtrar os registros. Padrão é None.

    Retorna:
    Uma tupla contendo:
    - Uma lista de registros da tabela, de acordo com a página e a consulta.
    - O número da página atual.
    - O número total de páginas.

    Exemplo de Uso:
    rows, pagina_atual, total_paginas = processar_paginacao(empresa, db.minha_tabela, 10, consulta=db.minha_tabela.campo == valor)

    Dependências:
    Esta função assume que as tabelas e o módulo 'db' estão configurados corretamente.

    """
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))
    if pagina <= 0:
        pagina = 1
    total = db(tabela.empresa == empresa.id).count()
    paginas = total // paginacao
    if total % paginacao:
        paginas += 1
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao * (pagina - 1), (paginacao * pagina))
    query = db(tabela.empresa == empresa.id)
    if consulta:
        query = query & consulta
    rows = query.select(limitby=limites, orderby=~tabela.id | tabela.nome)
    return rows, pagina, paginas, total
