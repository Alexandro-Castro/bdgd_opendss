from funcs_criar_rede import CriarRede
from py_dss_interface import DSS
import consultas as cst

''' ====== INI ======'''

alimentador = '012001'
arquivo = fr"C:\Users\castr\Documents\projetos_python\distribuicao\bdgd_mt\aln{alimentador}.dss"

dss = DSS()
rede = CriarRede(dss=dss, aln=alimentador)

with open(arquivo, 'w') as arq:
    arq.write('clear')

dss.text(f'compile {arquivo}')

aln = rede.db.consulta_ctmt(alimentador)[0]
trfs = rede.db.consulta_untrmt(aln['cod_id'])
print(len(trfs))
print(trfs[10])
