from dotenv import dotenv_values
import odoorpc

params = dotenv_values('.env')
password = dotenv_values('.secret')['PASSWORD']

def get_odoo():
    print('login to Odoo loaded...')
    odoo = odoorpc.ODOO(params['ODOO_SRV'], port=params['PORT'], protocol='jsonrpc+ssl')
    odoo.login(params['DB'], params['USER'], password)
    return odoo
