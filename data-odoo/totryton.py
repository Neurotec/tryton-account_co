#!/usr/bin/env python
#@author Jovany Leandro G.C <dirindesa@neurotec.co>
#@date 2017-05-24

import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom

#se hace un mapeo a las cuentas de tryton
#el kind de las cuentas es inferido de minimal account char,
#necesita evaluacion.
ODOO_TO_TRYTON_ACCOUNT_TYPE = {
    'account.data_account_type_liquidity': 'account_type_liquidity',
    'account.data_account_type_current_assets': 'account_type_current_assets',
    'account.data_account_type_receivable': {'type': {'ref': 'account_type_receivable'}, 'kind': 'receivable', 'deferral': True},
    'account.data_account_type_payable': {'type': {'ref': 'account_type_payable'}, 'kind': 'payable', 'deferral': True},
    'account.data_account_type_current_liabilities': 'account_type_current_liabilities',
    'account.data_account_type_equity': 'account_type_equity',
    'account.data_account_type_revenue': {'type': {'ref': 'account_type_revenue'}, 'kind': 'revenue'},
    'account.data_account_type_expenses': {'type': {'ref': 'account_type_expenses'}, 'kind': 'expense'},
    'account.data_account_type_direct_costs': 'account_type_direct_costs',
}

def parse_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        header = None
        for row in reader:
            if header == None:
                header = row
            else:
                yield dict(zip(header, row))

def cfield(parent, name, value):
        field = SubElement(parent,'field')
        field.set('name', name)
        if value == True:
            field.set('eval', 'True')
        elif value == False:
            field.set('eval', 'False')
        else:
            if isinstance(value, dict):
                for k in value:
                    field.set(k, value[k])
            else:
                field.text=value

def prettyprint(dom):        
    rough_string = tostring(dom, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

## GENERACION DE CUENTAS
trytonaccounts = Element('tryton')
trytonaccounts.append(Comment("Don't edit this file manually autogenerate from totryton.py"))
datae = SubElement(trytonaccounts, 'data')

for row in parse_csv('account.account.template.csv'):
    record = SubElement(datae, 'record')
    record.set('id', row['id'])
    record.set('model', 'account.account.template')
    

    fields = {
        'name': row['name'],
        'code': row['code'],
        'deferral': False,
        'kind': 'other',
    }


    usertype = ODOO_TO_TRYTON_ACCOUNT_TYPE[row['user_type_id:id']]
    if isinstance(usertype, dict):
        for var in usertype:
            fields[var] = usertype[var]
    else:            
        fields['type'] = {'ref': usertype}

        
    if row['reconcile'] == 'TRUE':
        fields['reconcile'] = True
    if row['reconcile'] == 'FALSE':
        fields['reconcile'] = False

    fields['parent'] = {'ref': row['id'][0:8]}
    for k in fields:
        cfield(record, k, fields[k])
        
with open('accounts.xml', 'w') as f:
    f.write(prettyprint(trytonaccounts))
    
# GENERACION DE IMPUESTOS
trytontaxs = Element('tryton')
trytontaxs.append(Comment("Don't edit this file manually autogenerate from totryton.py"))
datae = SubElement(trytontaxs, 'data')

for row in parse_csv('account.account.tag.csv'):
    record = SubElement(datae, 'record')
    record.set('id', row['id'])
    record.set('model', 'account.tax.code.template')

    if row['applicability'] != 'taxes':
        raise RuntimeError("applicability unknown")
    
    cfield(record, 'name', row['name'])
    cfield(record, 'code', row['name'])
    cfield(record, 'parent', {'ref': 'vat_code_chart_root'})
    cfield(record, 'account', {'ref': 'root'})
    
nline = 0
for row in parse_csv('account.tax.template.csv'):
    nline += 1
    amount_type = row['amount_type']
    if amount_type != 'percent':
        print("Warning omiting line {} unknow amount type {}".format(nline, amount_type))
        continue
    if row['account_id:id'] == "":
        print("Warning omiting line {} unknow account_type".format(nline, amount_type))
        continue
    record = SubElement(datae, 'record')
    record.set('id', row['id'])
    record.set('model', 'account.tax.template')
    cfield(record, 'name', row['name'])
    cfield(record, 'description', row['description'])
    
    amount_type = row['amount_type']
    if amount_type == 'percent':
        cfield(record,'type', 'percentage')
        amount = float(row['amount']) / 100
        cfield(record, 'rate', {'eval': "Decimal('{}')".format(row['amount'])})
    else:
        raise RuntimeError("unknown amount type {}".format(amount_type))


    cfield(record, 'invoice_account', {'ref': row['account_id:id']})
    cfield(record, 'credit_note_account', {'ref': row['refund_account_id:id']})
    cfield(record, 'invoice_base_code', {'ref': row['tag_ids/id']})
    cfield(record, 'credit_note_base_code', {'ref': row['tag_ids/id']})
    cfield(record, 'credit_note_base_sign', {'eval': "-1"})
    cfield(record, 'account', {'ref': 'root'})

    type_tax_use = row['type_tax_use']
    if type_tax_use == 'sale':
        cfield(record, 'group', {'ref': 'impuesto_venta'})
    elif type_tax_use == 'purchase':
        cfield(record, 'group', {'ref': 'impuesto_compra'})
    else:
        cfield(record, 'group', {'ref': 'impuesto_general'})
with open('taxs.xml', 'w') as f:
    f.write(prettyprint(trytontaxs))
        
