
def index_(tabela, coluna_pesquisa):
    """
    Função: index
    Descrição: Lista os registros de uma tabela específica, criados pelo usuário logado,
    relacionados a uma empresa, com opções de paginação e filtragem.

    Parâmetros:
    - tabela: Nome da tabela onde os registros serão buscados.
    - coluna_pesquisa: Nome da coluna para aplicar o filtro de pesquisa.

    Fluxo de Funcionamento:
    1. Verifica o usuário e a empresa associada.
    2. Redireciona para a página inicial se o usuário estiver inativo.
    3. Configurações de paginação e verifica parâmetros da URL.
    4. Cálculo de páginas e limites para exibição dos registros.
    5. Consulta os registros criados pelo usuário logado na tabela especificada.
    6. Retorna os dados para a visualização na página.

    Retorna:
    - Um dicionário contendo os registros encontrados, informações de paginação
      e detalhes da empresa para a visualização na página.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """
    # Busca o usuário e a empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Redireciona para a página inicial se o usuário estiver inativo
    if not usuario.ativo:
        redirect(URL('default', 'index'))

    # Configurações de paginação e verificação dos parâmetros da URL
    paginacao = empresa.paginacao
    pagina = int(request.args[0]) if request.args and request.args[0].isdigit() else 1

    # Lógica de cálculo de páginas e limites
    if pagina <= 0:
        pagina = 1
    total = db((tabela.empresa == empresa.id)).count()
    paginas = (total + paginacao - 1) // paginacao  # Calcula o número total de páginas
    if total == 0:
        paginas = 1
    if pagina > paginas:
        redirect(URL(args=[paginas]))

    limites = (paginacao * (pagina - 1), paginacao * pagina)

    # Consulta os registros da tabela especificada criados pelo usuário logado
    registros = db((tabela.empresa == empresa.id)).select(
        limitby=limites, orderby=~tabela.id)

    # Filtro de pesquisa
    consul = request.args(1)
    if consul:
        registros = db((tabela.empresa == empresa.id) &
                       (coluna_pesquisa.contains(consul))).select(
            limitby=limites, orderby=tabela.id)

    # Retorna os dados para a visualização
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)



@auth.requires_login()
def cadastro(tabela_nome):
    """
    Função: cadastrar (genérica)
    Descrição: Realiza o cadastro de um registro em qualquer tabela especificada.

    Fluxo de Funcionamento:
    1. Busca o usuário e a empresa associada.
    2. Configura a visualização e define o título da página.
    3. Define o valor padrão da empresa no formulário de cadastro.
    4. Processa o formulário de cadastro para a tabela específica.
    5. Redireciona para a página principal após aceitar o formulário.
    6. Exibe uma mensagem de erro se o formulário não for aceito.

    Parâmetros:
    - tabela_nome: nome da tabela no banco de dados (ex: 'cliente', 'produto').

    Retorna:
    - Um dicionário contendo o formulário para o cadastro da tabela especificada.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """

    # Verifica se a tabela passada como argumento existe no banco de dados
    if not hasattr(db, tabela_nome):
        raise HTTP(400, "Tabela não encontrada")

    tabela = db[tabela_nome]  # Obtenção dinâmica da tabela

    # Busca o usuário e empresa relacionada
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    empresa = db.empresa(usuario.empresa)

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = f"Cadastro de {tabela_nome}"  # define o título da página dinamicamente

    # Define o valor padrão da empresa no formulário
    if 'empresa' in tabela.fields:  # só define o valor se a tabela tiver o campo 'empresa'
        tabela.empresa.default = usuario.empresa

    # Gera e processa o formulário da tabela passada
    form = SQLFORM(tabela).process()

    # Redireciona para a página principal após aceitar o formulário
    if form.accepted:
        redirect(URL('index'))  # ou pode personalizar para redirecionar para a listagem da tabela específica
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)


@auth.requires_login()
def alteracao(tabela_nome):
    """
    Função: alterar
    Descrição: Permite a alteração de um registro existente de forma genérica para qualquer tabela.

    Fluxo de Funcionamento:
    1. Busca o usuário e o registro relacionado.
    2. Verifica se o registro pertence à empresa do usuário logado.
    3. Configurações da visualização e definição do título da página.
    4. Cria e processa o formulário de alteração do registro.
    5. Redireciona para a página principal após a aceitação do formulário.
    6. Exibe uma mensagem de erro se o formulário não for aceito.

    Parâmetros:
    - tabela_nome: nome da tabela que será utilizada para alteração do registro.

    Retorna:
    - Um dicionário contendo o formulário para a alteração do registro.

    Requisitos:
    - O usuário deve estar logado para acessar esta funcionalidade.
    """
    # Tabela referenciada dinamicamente
    tabela = db[tabela_nome]

    # Busca o usuário e o registro relacionado
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    registro = tabela(request.args(0, cast=int))

    pagina = int(request.args[1]) if len(request.args) > 1 else 1

    # Redireciona se o registro não pertencer à empresa do usuário
    if registro.empresa != usuario.empresa:
        redirect(URL('index'))

    # Configurações da visualização e definição do título da página
    response.view = 'generic.html'  # usa uma visualização genérica
    request.function = f'Alterar {tabela_nome}'  # define o título da página dinamicamente

    # Cria e processa o formulário de alteração
    form = SQLFORM(tabela, request.args(0, cast=int))
    if form.process().accepted:
        redirect(URL('index', args=pagina))
    elif form.errors:
        response.flash = 'Formulário não aceito'  # exibe uma mensagem de erro se o formulário não for aceito

    # Retorna o formulário para a visualização
    return dict(form=form)


#######################COMO UTILIZAR NO CONTROLLER#######################################

# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    return index_(db.produto, db.produto.descricao)


@auth.requires_login()
def cadastrar():
    return cadastro('produto')


@auth.requires_login()
def alterar():
    return alteracao('produto')


@auth.requires_login()
def acessar():
    response.view = 'generic.html'  # usa uma visualização genérica
    mensagem = 'Aguardando desenvolvimento'
    return locals()
