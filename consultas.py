from typing import List, Dict
import psycopg2.extras
import psycopg2
import os
from dotenv import load_dotenv

class DB():
    def __init__(self) -> None:
        load_dotenv() # Carrega as variáveis de ambiente do .env
        self.dados_db = {
            "host": os.getenv("DB_HOST"),
            "database": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD")
        }
    
    # Função para realizar a consulta ao banco de dados PostgreSQL
    def consulta_postgresql(self, query_sql: str) -> List[Dict]:
        try:
            # Configurações de conexão (substitua com suas credenciais)
            connection = psycopg2.connect(**self.dados_db)

            # Criar um cursor que retorna os resultados como dicionários
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

            # Consulta SQL
            # query = "SELECT * FROM SSDMT"

            # Executar a consulta
            cursor.execute(query_sql)

            # Obter todos os resultados
            resultados = cursor.fetchall()

            # Converter os resultados para uma lista de dicionários
            lista_dicionarios = [dict(row) for row in resultados]

            # Fechar o cursor e a conexão
            cursor.close()
            connection.close()

            # Retornar os resultados
            return lista_dicionarios

        except psycopg2.Error as e:
            print(f"Erro ao consultar o banco de dados: {e}")
            return None


    def consulta_ctmt(self, alimentador) -> List[Dict]:
        str_sql = f"""
            select 
                cod_id,
                nome, 
                barr, 
                sub, 
                pac_ini, 
                ten_nom, 
                ten_ope,
                uni_tr_at 
            from 
                ctmt
            where 
                nome = '{alimentador}'
        """
        
        dados_ctmt = self.consulta_postgresql(str_sql)
        return dados_ctmt


    def consulta_ssdmt(self, ctmt) -> List[Dict]:
        str_sql = f"""
            select
                --ssdmt
                ssdmt.cod_id,
                pac_1,
                pac_2,
                fas_con,
                comp,
                --segcon
                "R1",
                "X1",
                "CNOM",
                "CMAX"
            from
                segcon,
                ssdmt
            where
                ssdmt.ctmt = '{ctmt}'
                and segcon."COD_ID" = ssdmt.tip_cnd
        """
        return self.consulta_postgresql(str_sql)


    def consulta_untrmt(self, ctmt) -> List[Dict]:
        str_sql = f"""
            select
                untrmt.cod_id,
                pac_1,
                pac_2,
                fas_con_p,
                fas_con_s,
                ten_lin_se,
                tap,
                untrmt.pot_nom,
                untrmt.per_fer,
                untrmt.per_tot,
                eqtrmt.ten_pri,
                eqtrmt.ten_sec,
                eqtrmt.r,
                eqtrmt.xhl,
                eqtrmt.lig
            from
                untrmt,
                eqtrmt
            where
                ctmt = '{ctmt}'
                and untrmt.cod_id = eqtrmt.uni_tr_mt
        """
        
        return self.consulta_postgresql(str_sql)


    def consulta_unsemt(self, ctmt) -> List[Dict]:
        str_sql = f"""
            select
                cod_id,
                pac_1,
                pac_2,
                fas_con,
                p_n_ope,
                cor_nom
            from
                unsemt
            where
                ctmt = '{ctmt}'
        """
        return self.consulta_postgresql(str_sql)


    def consulta_unremt(self, ctmt) -> List[Dict]:
        str_sql = f"""
            select
                unremt.cod_id,
                fas_con,
                pac_1,
                pac_2,
                tip_regu,
                eqre.pot_nom,
                eqre.ten_reg,
                eqre.cor_nom,
                eqre.lig_fas_p,
                eqre.lig_fas_s,
                eqre.per_fer,
                eqre.per_tot,
                eqre.r,
                eqre.xhl
            from
                unremt,
                eqre
            where
                unremt.ctmt = '{ctmt}'
                and eqre.un_re = unremt.cod_id      
        """
        
        return self.consulta_postgresql(str_sql)
    
    
    def consulta_ucbt(self, ctmt) -> List[Dict]:
        sql_ucbt = f"""
            select 
                pac,
                ramal,
                uni_tr_mt,
                ceg_gd,
                fas_con,
                tip_cc,
                ten_for,
                car_inst,
                ene_01,
                ene_02,
                ene_03,
                ene_04,
                ene_05,
                ene_06,
                ene_07,
                ene_08,
                ene_09,
                ene_10,
                ene_11,
                ene_12
            from
                ucbt
            where
                ctmt = '{ctmt}'
        """
        
        return self.consulta_postgresql(sql_ucbt)
