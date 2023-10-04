# Desativa a edição e leitura do campo ID da tabela auth_user
db.auth_user.id.writable = False
db.auth_user.id.readable = False

# Define a tabela 'empresa'
db.define_table('empresa',
                Field('nome', 'string', label='Nome', requires=IS_UPPER()),
                Field('ativo', 'boolean', writable=False, readable=False, default=True, label='Ativo'),
                Field('paginacao', 'integer', writable=True, readable=True, default=10),
                Field('observacao', 'text', label='Observação', writable=False, readable=False),
                auth.signature,
                format='%(nome)s')

# Desativa a edição e leitura do campo ID da tabela empresa
db.empresa.id.writable = False
db.empresa.id.readable = False

# Define a tabela 'usuario_empresa'
db.define_table('usuario_empresa',
                Field('usuario', 'reference auth_user', writable=False, readable=False, label='Usuário'),
                Field('empresa', 'reference empresa', writable=False, readable=False, label='Empresa'),
                Field('tipo', 'string', label='Tipo', default='Proprietário', requires=IS_IN_SET(['Programador', 'Proprietário', 'Administrador'])),
                Field('ativo', 'boolean', writable=True, readable=True, default=True, label='Ativo'))

# Desativa a edição e leitura do campo ID da tabela usuario_empresa
db.usuario_empresa.id.writable = False
db.usuario_empresa.id.readable = False

# Documentação das tabelas
"""
Tabela auth_user:
- Campos:
  - id: ID do usuário (não editável/visível)
  - ... outros campos padrão do auth (não documentados aqui)

Tabela empresa:
- Campos:
  - id: ID da empresa (não editável/visível)
  - nome: Nome da empresa (obrigatório, formato em maiúsculas)
  - ativo: Indica se a empresa está ativa (não editável/visível, padrão: True)
  - observacao: Observação da empresa (não editável/visível)
  - ... outros campos padrão do auth (não documentados aqui)

Tabela usuario_empresa:
- Campos:
  - id: ID do relacionamento usuário-empresa (não editável/visível)
  - usuario: Usuário associado (não editável/visível)
  - empresa: Empresa associada (não editável/visível)
  - tipo: Tipo do usuário na empresa (Padrão: 'Proprietário', opções: 'Programador', 'Proprietário', 'Administrador')
  - ativo: Indica se o usuário está ativo na empresa (editável, padrão: True)
"""
