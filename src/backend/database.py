import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from src.backend.models import Pedidos

# Conexão Global
conn = st.connection("gsheets", type=GSheetsConnection)

def get_all_pedidos() -> pd.DataFrame:
    try:
        url_planilha = st.secrets["spreadsheet"]
        df = conn.read(spreadsheet=url_planilha, worksheet="Pedidos", ttl=5) # ttl=0 para não cachear dados velhos
        df = df.dropna(how="all")
        return df
    except Exception as e:
        st.error(f"Erro ao ler banco: {e}")
        return pd.DataFrame()

def _gerar_novo_id(df: pd.DataFrame) -> int:
    """Gera ID incremental baseado no maior ID existente"""
    if df.empty:
        return 1
    
    # Garante que a coluna ID seja numérica (trata erros com coerce)
    try:
        ids = pd.to_numeric(df["ID"], errors='coerce').fillna(0)
        return int(ids.max()) + 1
    except KeyError:
        # Se a coluna ID não existir ainda na planilha
        return 1

def save_pedido(pedido_obj: Pedidos):
    try:
        url = st.secrets["spreadsheet"]
        
        # 1. Baixa dados atuais
        df_atual = get_all_pedidos()
        
        # 2. Gera e injeta o ID
        novo_id = _gerar_novo_id(df_atual)
        pedido_obj.ID = novo_id # Atualiza o objeto com o ID gerado
        
        # 3. Cria DF e salva
        novo_pedido_df = pd.DataFrame([pedido_obj.to_dict()])
        df_atualizado = pd.concat([df_atual, novo_pedido_df], ignore_index=True)
        
        conn.update(spreadsheet=url, worksheet="Pedidos", data=df_atualizado)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        raise e

def update_status_by_id(pedido_id: int, novo_status: str):
    """Busca pelo ID e atualiza o status na nuvem"""
    try:
        url = st.secrets["spreadsheet"]
        df = get_all_pedidos()
        
        # Converte ID para numero para garantir a comparação
        df["ID"] = pd.to_numeric(df["ID"], errors='coerce')
        
        # Localiza a linha onde ID bate
        # O .index traz o número da linha no DataFrame
        mask = df["ID"] == pedido_id
        
        if df[mask].empty:
            st.error("ID não encontrado")
            return False
            
        # Atualiza o valor
        df.loc[mask, "Status"] = novo_status
        
        # Salva de volta
        conn.update(spreadsheet=url, worksheet="Pedidos", data=df)
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar status: {e}")
        return False