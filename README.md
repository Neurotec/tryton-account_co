# migracion de datos de odoo-l10n_co a trytond-account

## odoo

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

# TODO

tryton para cuenta define los siguientes tipos:
  * A cobrar
  * A pagar
  * Existencias
  * Ingresos
  * Gastos
  * Otros
  * Vista : vista es para agrupar cuentas
  
# REFERENCIAS

  * http://www.puc.com.co

