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


trytone = Element('tryton')
trytone.append(Comment("Don't edit this file manually autogenerate from totryton.py"))
datae = SubElement(trytone, 'data')

for row in parse_csv('account.account.template.csv'):
    record = SubElement(datae, 'record')
    record.set('id', row['id'])
    record.set('model', 'account.account.template')
    
    def cfield(name, value):
        field = SubElement(record,'field')
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
        cfield(k, fields[k])

        

rough_string = tostring(trytone, 'utf-8')
reparsed = minidom.parseString(rough_string)
with open('odoo_accounts.xml', 'w') as f:
    f.write(reparsed.toprettyxml(indent="  "))

