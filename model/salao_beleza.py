# -*- coding: utf-8 -*-

import os
import time
import datetime
import pytz

# Define o timezone padrão
os.environ['TZ'] = 'America/Sao_Paulo'
time.tzset()

from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# Este modelo de scaffolding faz seu aplicativo funcionar também no Google App Engine
# O arquivo é liberado sob domínio público e você pode usar sem limitações
# -------------------------------------------------------------------------
if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# se SSL/HTTPS estiver devidamente configurado e você quiser que todas as solicitações HTTP
# sejam redirecionadas para HTTPS, descomente a linha abaixo:
# -------------------------------------------------------------------------
request.requires_https()

# -------------------------------------------------------------------------
# uma vez em produção, remova reload=True para obter velocidade total
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # se NÃO estiver rodando no Google App Engine, use SQLite ou outro banco de dados
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # conectar ao Google BigTable (opcional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # armazene sessões e tickets lá
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # ou armazene sessões em Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# por padrão, atribua uma view/generic.extension a todas as ações de localhost
# nenhuma de outra forma. um padrão pode ser 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# escolha um estilo para formulários
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (opcional) otimize o manuseio de arquivos estáticos
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (opcional) versionamento de pasta de ativos estáticos
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Aqui está um código de exemplo se você precisar de
# - capacidades de email
# - autenticação (registro, login, logout, ...)
# - autorização (autorização baseada em papéis)
# - serviços (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - ações de crud de estilo antigo
# (mais opções discutidas em gluon/tools.py)
# -------------------------------------------------------------------------

# nomes de host devem ser uma lista de nomes de host permitidos (sintaxe glob permitida)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# crie todas as tabelas necessárias pela autenticação, talvez adicione uma lista de campos extras
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure o email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure a política de autenticação
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# leia mais em http://dev.w3.org/html5/markup/meta.name.html
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# seu id do http://google.com/analytics
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

T.force('pt-br')
# -------------------------------------------------------------------------
# talvez use o agendador
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))
    
db.auth_user.id.readable = False

# Define a tabela 'empresa'
db.define_table('empresa',
                Field('nome', 'string', label='Nome', requires=IS_UPPER()),
                Field('ativo', 'boolean', writable=False, readable=False, default=True, label='Ativo'),
                Field('paginacao', 'integer', writable=True, readable=True, default=10),
                Field('observacao', 'text', label='Observação', writable=False, readable=False),
                auth.signature,
                format='%(nome)s')


# Define a tabela 'usuario_empresa'
db.define_table('usuario_empresa',
                Field('usuario', 'reference auth_user', writable=False, readable=False, label='Usuário'),
                Field('empresa', 'reference empresa', writable=False, readable=False, label='Empresa'),
                Field('tipo', 'string', label='Tipo', default='Proprietário', requires=IS_IN_SET(['Programador', 'Proprietário', 'Administrador'])),
                Field('ativo', 'boolean', writable=True, readable=True, default=True, label='Ativo'))


# CLIENTE
db.define_table('cliente',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('nome','string', label='Nome', requires=IS_NOT_EMPTY()),
    Field('telefone','string', label='Telefone'),
    Field('whatsapp','string', label='Whatsapp'),
    Field('email','string', label='Email'),
    Field('data_nascimento','date', label='Nascimento',
        default=request.now.date(),
        requires=[IS_DATE(format='%d/%m/%Y')]),
    Field('observacao','text', label='Observação'),
    Field('ativo','boolean', default=True, label='Ativo'),
    auth.signature,
    format='%(nome)s'
)

db.cliente.id.readable = False

# FUNCIONARIO
db.define_table('funcionario',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('nome','string', label='Nome', requires=IS_NOT_EMPTY()),
    Field('telefone','string', label='Telefone'),
    Field('cargo','string', label='Cargo'),
    Field('comissao_percentual', 'decimal(10,2)', default=0, label='Comissão %',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('ativo','boolean', default=True, label='Ativo'),
    auth.signature,
    format='%(nome)s'
)
db.funcionario.id.readable = False

# SERVICO
db.define_table('servico',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('nome','string', label='Nome', requires=IS_NOT_EMPTY()),
    Field('descricao','text', label='Descrição'),
    Field('valor', 'decimal(10,2)', default=0, label='Valor',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('duracao_minutos','integer', label='Duração (minutos)'),
    Field('ativo','boolean', default=True, label='Ativo'),
    auth.signature,
    format='%(nome)s'
)


# PRODUTO
db.define_table('produto',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('nome','string', label='Produto', requires=IS_NOT_EMPTY()),
    Field('marca','string', label='Marca'),
    Field('preco_custo', 'decimal(10,2)', default=0, label='Preço Custo',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('preco_venda', 'decimal(10,2)', default=0, label='Preço Venda',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('estoque','integer', default=0, label='Estoque'),
    Field('estoque_minimo','integer', default=0, label='Estoque mínimo'),
    Field('ativo','boolean', default=True, label='Ativo'),
    auth.signature,
    format='%(nome)s'
)

db.define_table('agendamento',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('cliente','reference cliente', label='Cliente'),
    Field('servico','reference servico', label='Serviço'),
    Field('funcionario','reference funcionario', label='Funcionário'),
    Field('data_agendamento','date', label='Data',
        default=request.now.date(),
        requires=[IS_DATE(format='%d/%m/%Y')]),
    Field('hora','time', label='Horário'),
    Field('status','string', label='Status',
        default='Agendado',
        requires=IS_IN_SET(['Agendado', 'Confirmado', 'Realizado', 'Cancelado'])),
    Field('observacao','text', label='Observação'),
    auth.signature
)

# SERVICO REALIZADO
db.define_table('servico_realizado',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('agendamento','reference agendamento', label='Agendamento Origem'),
    Field('cliente','reference cliente', label='Cliente'),
    Field('servico','reference servico', label='Serviço'),
    Field('funcionario','reference funcionario', label='Funcionário'),
    Field('valor', 'decimal(10,2)', default=0, label='Valor',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('desconto', 'decimal(10,2)', default=0, label='Desconto',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('valor_final', 'decimal(10,2)', default=0, label='Valor Final',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('data_realizacao','date', label='Data Realização',
        default=request.now.date(),
        requires=[IS_DATE(format='%d/%m/%Y')]),
    Field('observacao','text', label='Observação'),
    auth.signature
)

# VENDA PRODUTO
db.define_table('venda_produto',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('cliente','reference cliente', label='Cliente'),
    Field('data_venda','date', label='Data da Venda',
        default=request.now.date(),
        requires=[IS_DATE(format='%d/%m/%Y')]),
    Field('valor_total', 'decimal(10,2)', default=0, label='Total',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('forma_pagamento','string', label='Forma de Pagamento',
        requires=IS_IN_SET(['Dinheiro', 'Pix', 'Cartão Crédito', 'Cartão Débito'])),
    Field('observacao','text', label='Observação'),
    auth.signature
)

# ITEM VENDA PRODUTO
db.define_table('item_venda_produto',
    Field('venda','reference venda_produto', label='Venda ID'),
    Field('produto','reference produto', label='Produto'),
    Field('quantidade','integer', default=1, label='Qtd'),
    Field('valor_unitario', 'decimal(10,2)', default=0, label='Vlr Unitário',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('valor_total', 'decimal(10,2)', default=0, label='Vlr Total',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=','))
)

# REGISTRO FINANCEIRO
db.define_table('registro_financeiro',
    Field('empresa','reference empresa', writable=False, readable=False),
    Field('tipo','string', label='Tipo', requires=IS_IN_SET(['Entrada','Saída'])),
    Field('categoria','string', label='Categoria'),
    Field('descricao','string', label='Descrição'),
    Field('valor', 'decimal(10,2)', default=0, label='Valor',
          requires=IS_DECIMAL_IN_RANGE(0, None, dot=',')),
    Field('forma_pagamento','string', label='Forma Pagto'),
    Field('data_registro','date', label='Data Registro',
        default=request.now.date(),
        requires=[IS_DATE(format='%d/%m/%Y')]),
    Field('servico_realizado','reference servico_realizado', writable=False, readable=False),
    Field('venda_produto','reference venda_produto', writable=False, readable=False),
    Field('observacao','text', label='Observação'),
    auth.signature
)

for t in db.tables:
    db[t].id.readable = False
    db[t].id.writable = False
