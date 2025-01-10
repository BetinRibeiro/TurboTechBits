# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# Configuração do AppConfig facilitada. Veja dentro de private/appconfig.ini
# Auth é para autenticação e controle de acesso
# -------------------------------------------------------------------------

from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# Este modelo de estrutura faz seu aplicativo funcionar também no Google App Engine
# O arquivo é liberado sob domínio público e você pode usar sem limitações
# -------------------------------------------------------------------------


if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# Se o SSL/HTTPS estiver corretamente configurado e você desejar que todas as 
# solicitações HTTP sejam redirecionadas para HTTPS, descomente a linha abaixo:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# Uma vez em produção, remova reload=True para obter velocidade total
# -------------------------------------------------------------------------


configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # Se NÃO estiver rodando no Google App Engine, use SQLite ou outro banco de dados
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # Conectar ao Google BigTable (opcional 'google:datastore://namespace')
    # ---------------------------------------------------------------------

    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # armazene sessões e tickets lá
    # ---------------------------------------------------------------------

    session.connect(request, response, db=db)
    
    # ---------------------------------------------------------------------
    # ou armazene a sessão em Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# por padrão, atribua uma view/generic.extension a todas as ações de localhost
# nenhuma outra forma. um padrão pode ser 'controller/function.extension'
# -------------------------------------------------------------------------

response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# escolha um estilo para os formulários
# -------------------------------------------------------------------------

response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (opcional) otimize o tratamento de arquivos estáticos
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (opcional) versionamento de pastas de ativos estáticos
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Aqui está um código de exemplo se você precisar para
# - capacidades de e-mail
# - autenticação (registro, login, logout, ...)
# - autorização (autorização baseada em papéis)
# - serviços (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - ações crud de estilo antigo
# (mais opções discutidas em gluon/tools.py)
# -------------------------------------------------------------------------

# os nomes de host devem ser uma lista de nomes de host permitidos (sintaxe glob permitida)
auth = Auth(db, host_names=configuration.get('host.names'))
# -------------------------------------------------------------------------
# crie todas as tabelas necessárias para autenticação, talvez adicione uma lista de campos extras
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
# seu ID do http://google.com/analytics
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')
# -------------------------------------------------------------------------
# talvez use o agendador
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

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
