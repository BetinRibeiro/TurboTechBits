def verificar_usuario_ativo():
    """
    Verifica se o usuário autenticado está ativo como parte de uma empresa no sistema.

    Retorna:
    Uma instância da linha correspondente na tabela 'usuario_empresa' se o usuário estiver ativo.

    Redireciona:
    Para a página 'default/index' se o usuário não for encontrado na tabela 'usuario_empresa' ou estiver inativo.

    Exemplo de Uso:
    usuario = verificar_usuario_ativo()
    if usuario:
        # O usuário está ativo, faça algo com os dados do usuário.
    else:
        # O usuário não foi encontrado ou está inativo, redirecione para a página principal.

    """
    usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
    if not usuario or not usuario.ativo:
        redirect(URL('default', 'index'))
    return usuario
