from funcs_criar_rede import CriarRede
from py_dss_interface import DSS
import consultas as cst

''' ====== INI ======'''

alimentador = '012001'


dss = DSS()
dss.text('Clear')
rede = CriarRede(dss=dss, aln=alimentador)

# aln = rede.db.consulta_ctmt(alimentador)[0]
# trfs = rede.db.consulta_untrmt(aln['cod_id'])
