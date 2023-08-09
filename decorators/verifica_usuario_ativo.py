from functools import wraps

def verifica_usuario_ativo(f):
    """
    Decorador para verificar se o usuário está ativo e associado a uma empresa válida.

    Este decorador verifica se o usuário está logado, ativo e associado a uma empresa válida.
    Caso contrário, redireciona para a página inicial.

    Args:
        f (function): A função a ser decorada.

    Returns:
        function: A função decorada.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # Obtém o registro do usuário na tabela usuario_empresa
        usuario = db.usuario_empresa(db.usuario_empresa.usuario == auth.user.id)
        
        # Verifica se o usuário e a empresa existem e se o usuário está ativo
        if not usuario or not usuario.empresa or not usuario.ativo:
            redirect(URL('default', 'index'))
        
        # Obtém o registro da empresa associada ao usuário
        empresa = db.empresa(usuario.empresa)
        
        return f(*args, **kwargs)
    
    return decorated
