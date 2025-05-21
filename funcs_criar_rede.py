from py_dss_interface import DSS
from consultas import DB


class CriarRede():
    def __init__(self, dss: DSS, aln: str) -> None:
        self.db = DB()
        self.dss: DSS = dss
        self.alimentador = aln
        self.ctmt = ''
        self.basekvs = []
        
        self.tten = { # tensão em kv
            '1': 0.11,
            '2': 0.15,
            '3': 0.12,
            '6': 0.127,
            '10': 0.22,
            '11': 0.23,
            '13': 0.24,
            '14': 0.254,
            '15': 0.38,
            '39': 7.96,
            '49': 13.8,
            '72': 35.5
        }

        self.tcor = { # corrente nominal das chaves seccionadoras
            "12": 100,
            "18": 200,
            "24": 300,
            "25": 320,
            "27": 400,
            "35": 630,
            "36": 800
        }

        self.tpotaprt = {
            '32': 276
        }


    def new_circuit(self):
        dados = self.db.consulta_ctmt(self.alimentador)[0]
        str_circuit = f"new circuit.{dados['cod_id']} basekv={self.tten[dados['ten_nom']]} "
        str_circuit += f"pu={dados['ten_ope']} bus1={dados['pac_ini']} frequency=60 r1=0.00000 x1=0.00010"
        self.dss.text(str_circuit)
        
        self.basekvs.append(self.tten[dados['ten_nom']])
        self.ctmt = dados['cod_id']


    def new_linesMT(self):
        dados = self.db.consulta_ssdmt(self.ctmt)
        for dado in dados:
            if dado['fas_con'] == 'ABC':
                str_line = f"new line.{dado['cod_id']}.1.2.3 phases=3 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m "
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
                
            elif dado['fas_con'] == 'AB':
                str_line = f'new line.{dado['cod_id']}.1.2 phases=2 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
                
            elif dado['fas_con'] == 'BC':
                str_line = f'new line.{dado['cod_id']}.2.3 phases=2 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)  
            
            elif dado['fas_con'] == 'CA':
                str_line = f'new line.{dado['cod_id']}.1.3 phases=2 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
            
            elif dado['fas_con'] == 'A':
                str_line = f'new line.{dado['cod_id']}.1 phases=1 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
            
            elif dado['fas_con'] == 'B':
                str_line = f'new line.{dado['cod_id']}.2 phases=1 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
            
            elif dado['fas_con'] == 'C':
                str_line = f'new line.{dado['cod_id']}.3 phases=1 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
            else:
                print(f"ERRO ao criar linha. {dado}")
        
        print("SSDMT criado com sucesso")


    def new_transformers(self):
        dados = self.db.consulta_untrmt(self.ctmt)
        for dado in dados:
            loadloss = 100 * dado['per_tot'] / (1000 * dado['pot_nom'])
            noloadloss = 100 * dado['per_fer'] / (1000 * dado['pot_nom'])
            ten_pri = self.tten[dado['ten_pri']]
            ten_sec = self.tten[dado['ten_sec']]
            
            if dado['lig'] == '2': # trafo trifásico urbano
                str_trf = f"new transformer.{dado['cod_id']} buses=[{dado['pac_1']}.1.2.3 {dado['pac_2']}.1.2.3.4] kva={dado['pot_nom']} "
                str_trf += f"kvs=[{ten_pri} {ten_sec}] xhl={dado['xhl']} %R={dado['r']} tap={dado['tap']} "
                str_trf += f"conns=[delta wye] %loadloss={loadloss} %noloadloss={noloadloss }"
                self.dss.text(str_trf)
            
            elif dado['lig'] == '6': # trafo mono rural
                if dado['fas_con_p'] == 'A':
                    str_trf = f"new transformer.{dado['cod_id']} phases=1 windings=3 "
                    str_trf += f"buses=[{dado['pac_1']}.1 {dado['pac_2']}.1.0 {dado['pac_2']}.0.2] "
                    str_trf += f"kvs=[{ten_pri} {ten_sec * 0.5} {ten_sec * 0.5}] "
                    str_trf += f"conns=[wye wye wye] kvas=[{dado['pot_nom']} {dado['pot_nom'] * 0.5} {dado['pot_nom'] * 0.5}] "
                    str_trf += f"xhl={dado['xhl']} %R={dado['r']} tap={dado['tap']} %loadloss={loadloss} %noloadloss={noloadloss }"
                    self.dss.text(str_trf)
                    
                elif dado['fas_con_p'] == 'B':
                    str_trf = f"new transformer.{dado['cod_id']} phases=1 windings=3 "
                    str_trf += f"buses=[{dado['pac_1']}.2 {dado['pac_2']}.1.0 {dado['pac_2']}.0.2] "
                    str_trf += f"kvs=[{ten_pri} {ten_sec} {ten_sec}] "
                    str_trf += f"conns=[wye wye wye] kvas=[{dado['pot_nom']} {dado['pot_nom']} {dado['pot_nom']}] "
                    str_trf += f"xhl={dado['xhl']} %R={dado['r']} tap={dado['tap']} %loadloss={loadloss} %noloadloss={noloadloss }"
                    self.dss.text(str_trf)
                    
                elif dado['fas_con_p'] == 'C':
                    str_trf = f"new transformer.{dado['cod_id']} phases=1 windings=3 "
                    str_trf += f"buses=[{dado['pac_1']}.3 {dado['pac_2']}.1.0 {dado['pac_2']}.0.2] "
                    str_trf += f"kvs=[{ten_pri} {ten_sec} {ten_sec}] "
                    str_trf += f"conns=[wye wye wye] kvas=[{dado['pot_nom']} {dado['pot_nom']} {dado['pot_nom']}] "
                    str_trf += f"xhl={dado['xhl']} %R={dado['r']} tap={dado['tap']} %loadloss={loadloss} %noloadloss={noloadloss }"
                    self.dss.text(str_trf)
                
                else:
                    print(f"erro ao criar trafo mono rural. {dado}")
        
        print("UNTRMT criado com sucesso")


    def new_secs(self):
        dados = self.db.consulta_unsemt(self.ctmt)
        for dado in dados:
            
            if dado['fas_con'] == 'ABC':
                str_line = f"new line.{dado['cod_id']}.1.2.3 phases=3 bus1={dado['pac_1']} bus2={dado['pac_2']} "
                str_line += f'length=0.1 units=m switch=y'
                self.dss.text(str_line)
                
            elif dado['fas_con'] == 'AB':
                str_line = f'new line.{dado['cod_id']}.1.2 phases=2 bus1={dado['pac_1']} bus2={dado['pac_2']} length={dado['comp']} units=m '
                str_line += f'r1={dado['R1']} x1={dado['X1']} normamps={dado['CNOM']} emergamps={dado['CMAX']}'
                self.dss.text(str_line)
                
            elif dado['fas_con'] == 'BC':
                str_line = f'new line.{dado['cod_id']}.2.3 phases=2 bus1={dado['pac_1']} bus2={dado['pac_2']} '
                str_line += f'length=0.1 units=m switch=y'
                self.dss.text(str_line)  
            
            elif dado['fas_con'] == 'CA':
                str_line = f'new line.{dado['cod_id']}.1.3 phases=2 bus1={dado['pac_1']} bus2={dado['pac_2']} '
                str_line += f'length=0.1 units=m switch=y'
                self.dss.text(str_line)
            
            elif dado['fas_con'] == 'A':
                str_line = f'new line.{dado['cod_id']}.1 phases=1 bus1={dado['pac_1']} bus2={dado['pac_2']} '
                str_line += f'length=0.1 units=m switch=y'
                self.dss.text(str_line)
            
            elif dado['fas_con'] == 'B':
                str_line = f'new line.{dado['cod_id']}.2 phases=1 bus1={dado['pac_1']} bus2={dado['pac_2']} '
                str_line += f'length=0.1 units=m switch=y'
                self.dss.text(str_line)
            
            elif dado['fas_con'] == 'C':
                str_line = f'new line.{dado['cod_id']}.3 phases=1 bus1={dado['pac_1']} bus2={dado['pac_2']} '
                str_line += f'length=0.1 units=m switch=y'
                self.dss.text(str_line)
            else:
                print(f"ERRO ao criar linha UNSEMT. {dado}")
        
        print("UNSEMT criado com sucesso")


    def new_regs(self):
        dados = self.db.consulta_unremt(self.ctmt)
        for dado in dados:
            pot_nom = self.tpotaprt[dado['pot_nom']]
            loadloss = 100 * dado['per_tot'] / (1000 * pot_nom)
            noloadloss = 100 * dado['per_fer'] / (1000 * pot_nom)
            
            if dado['lig_fas_p'] == 'AB':
                str_reg = f"new transformer.{dado['cod_id']}{dado['lig_fas_p']} phases=2 windings=2 "
                str_reg += f"buses=[{dado['pac_1']}.1.2, {dado['pac_2']}.1.2] conns=[Delta Delta] kvs=[13.8 13.8] "
                str_reg += f"kvas=[{pot_nom} {pot_nom}] xhl={dado['xhl']} %R={dado['r']} "
                str_reg += f"%loadloss={loadloss} %noloadloss={noloadloss}"
                self.dss.text(str_reg)
                
                str_reg = f"new regcontrol.{dado['cod_id']}{dado['lig_fas_p']} transformer={dado['cod_id']}{dado['lig_fas_p']} "
                str_reg += f"winding=2 vreg"
                self.dss.text(str_reg)
                
            elif dado['lig_fas_p'] == 'BC':
                str_reg = f"new transformer.{dado['cod_id']}{dado['lig_fas_p']} phases=2 windings=2 "
                str_reg += f"buses=[{dado['pac_1']}.2.3, {dado['pac_2']}.2.3] conns=[Delta Delta] kvs=[13.8 13.8] "
                str_reg += f"kvas=[{pot_nom} {pot_nom}] xhl={dado['xhl']} %R={dado['r']} "
                str_reg += f"%loadloss={loadloss} %noloadloss={noloadloss}"
                self.dss.text(str_reg)
                
                str_reg = f"new regcontrol.{dado['cod_id']}{dado['lig_fas_p']} transformer={dado['cod_id']}{dado['lig_fas_p']} "
                str_reg += f"winding=2 vreg"
                self.dss.text(str_reg)
            
            elif dado['lig_fas_p'] == 'CA':
                str_reg = f"new transformer.{dado['cod_id']}{dado['lig_fas_p']} phases=2 windings=2 "
                str_reg += f"buses=[{dado['pac_1']}.3.1, {dado['pac_2']}.3.1] conns=[Delta Delta] kvs=[13.8 13.8] "
                str_reg += f"kvas=[{pot_nom} {pot_nom}] xhl={dado['xhl']} %R={dado['r']} "
                str_reg += f"%loadloss={loadloss} %noloadloss={noloadloss}"
                self.dss.text(str_reg)
                
                str_reg = f"new regcontrol.{dado['cod_id']}{dado['lig_fas_p']} transformer={dado['cod_id']}{dado['lig_fas_p']} "
                str_reg += f"winding=2 vreg"
                self.dss.text(str_reg)


    def criar_rede(self):
        self.new_circuit()
        self.new_linesMT()
        self.new_transformers()
        self.new_secs()
    