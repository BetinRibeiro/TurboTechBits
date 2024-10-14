# -*- coding: utf-8 -*-

# Definição da tabela 'pessoa' com CPF, telefone e nome completo
db.define_table('pessoa',
    Field('nome_completo', 'string', label='Nome Completo', default='', requires=IS_NOT_EMPTY()),  # Campo para nome completo
    Field('cpf', 'string', label='CPF', default='', requires=IS_NOT_EMPTY()),  # Campo para CPF
    Field('telefone', 'string', label='Telefone', default='', requires=IS_NOT_EMPTY())  # Campo para telefone
)

db.pessoa.id.writable = False
db.pessoa.id.readable = False

# Definição da tabela 'vendedor' herdando de 'pessoa'
db.define_table('vendedor',
    db.pessoa,  # Herda todos os campos da tabela pessoa
    Field('total_venda', 'double', label='Venda Total', default=0,requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),  # Campo para venda
    Field('comissao', 'double', label='Comissão (%)', default=0,requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),  # Campo para comissão do vendedor
    Field('ativo', 'boolean', writable=False, readable=False, default=True),  # Campo para status ativo
    auth.signature,  # Campos de auditoria (criado por, modificado por, etc.)
    format='%(nome_completo)s'  # Exibição do nome completo nos formulários
)

# Definir campos de leitura e escrita
db.vendedor.id.writable = False
db.vendedor.id.readable = False
db.vendedor.total_venda.writable = False
db.vendedor.total_venda.readable = False
