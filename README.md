# MODULO DE LOCALIZACION PARA COLOMBIA PLATAFORMA ERP TRYTON

se hace una ``importación`` de [odoo l10n_co](https://github.com/buguelos/odoo/tree/master/addons/l10n_co/data)

# INSTALACION

clonar el repositorio dentro de la carpeta **modules** de tryton:
~~~
$ cd trytond/modules ; git clone https://repo.neurotec.co/CODOO/account_co
~~~

luego activar el modulo:

~~~
$ trytond-admin -c <tryton.cfg> -d <database> -u account_co
~~~

una ves activado, dar en **Contabilidad/Plantillas/Crear plan contable desde plantillas**.

# REFERENCIAS

  * http://www.puc.com.co


# TODO

tryton para cuenta define los siguientes tipos:
  * A cobrar
  * A pagar
  * Existencias
  * Ingresos
  * Gastos
  * Otros
  * Vista : vista es para agrupar cuentas

evaluar el correcto funcionamiento de las cuentas y los impuestos.


# DESARROLLO 

## ODOO 

- liquility, caja general
- expenses, gastos
- equity,
- payable, por pagar
- receivable, por cobrar
- revenue
- direct_costs, costos directos
- current_assets, activos circulantes
- current_liabilities, pasivos cirulantes

---
La codificación del Catálogo de Cuentas está estructurada sobre la base de los siguientes niveles:

Clase:
    El primer dígito
Grupo:
    Los dos primeros dígitos
Cuenta:
    Los cuatro primeros dígitos
Subcuenta:
    Los seis primeros dígitos

Las clases 1, 2 y 3 comprenden las cuentas que conforman el balance general; las clases 4, 5, 6 y 7 corresponden a las cuentas del estado de ganancias o pérdidas o estado de resultados y las clases 8 y 9 detallan las cuentas de orden.

### CLIENTES
 - Cuentas por cobrar:  130505 nacionales
 - Cuentas por pagar: 220505 nacionales

