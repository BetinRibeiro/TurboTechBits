db.define_table('funcionarios',
                Field('nome'),
                Field('cargo'),
                Field('salario_base', 'double'),
                Field('departamento'))

db.define_table('registros_ponto',
                Field('funcionario_id', 'reference funcionarios'),
                Field('data_entrada', 'datetime'),
                Field('data_saida', 'datetime'),
                Field('total_horas', 'double'))

db.define_table('vencimentos',
                Field('funcionario_id', 'reference funcionarios'),
                Field('tipo_vencimento',requires=IS_IN_SET(['Salário Base', 'Horas Extras', 'Comissões', 'Bônus', 'Adicionais Noturnos', 'Adicionais de Insalubridade', 'Adicionais de Periculosidade', 'Gratificações'])),
                Field('valor_vencimento', 'double'),
                Field('data_vencimento', 'date'))

db.define_table('descontos',
                Field('funcionario_id', 'reference funcionarios'),
                Field('tipo_desconto', requires=IS_IN_SET(['Impostos sobre a Folha de Pagamento', 'Plano de Saúde', 'Vale-Transporte', 'Vale-Alimentação', 'Empréstimos ou Adiantamentos', 'Faltas ou Atrasos'])),
                Field('valor_desconto', 'double'),
                Field('data_desconto', 'date'))

db.define_table('pagamentos',
                Field('funcionario_id', 'reference funcionarios'),
                Field('total_bruto', 'double'),
                Field('total_descontos', 'double'),
                Field('total_liquido', 'double'),
                Field('data_pagamento', 'date'))
