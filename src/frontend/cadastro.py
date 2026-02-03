import streamlit as st
from datetime import date
from src.backend.models import Pedidos
from src.backend.database import save_pedido

def render_cadastro():
    st.header("📝 Novo Pedido")
    
    with st.form("form_pedido", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome do Cliente")
        fone = col2.text_input("WhatsApp (DDD + Número)", help="Apenas números")
        
        # COLUNA DE DATA E HORA LADO A LADO
        c_data, c_hora = st.columns(2)
        data_entrega = c_data.date_input("Data da Entrega", min_value=date.today(), format="DD/MM/YYYY")
        hora_entrega = c_hora.time_input("Horário da Entrega") # <--- NOVO INPUT
        
        st.subheader("Detalhes do Bolo")
        # ... (MANTENHA O RESTO DOS SELETORES IGUAIS: Massa, Recheio, etc) ...
        c1, c2 = st.columns(2)
        massa = c1.selectbox("Massa", ["Branca", "Chocolate", "Red Velvet", "Cenoura", "Outra"])
        recheio = c2.selectbox("Recheio", ["Brigadeiro", "Ninho", "Doce de Leite", "Frutas Vermelhas", "Outro"])
        
        c3, c4 = st.columns(2)
        tamanho = c3.selectbox("Tamanho", ["15cm (1kg)", "20cm (2kg)", "25cm (3kg)", "Andares"])
        cobertura = c4.selectbox("Cobertura", ["Chantininho", "Ganache", "Pasta Americana", "Naked"])
        
        valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        
        submitted = st.form_submit_button("✅ Salvar Encomenda")
        
        if submitted:
            if not nome or not fone:
                st.error("⚠️ Nome e Telefone são obrigatórios!")
            else:
                try:
                    novo_pedido = Pedidos(
                        ID=0,
                        cliente_nome=nome,
                        cliente_telefone=fone,
                        data_entrega=data_entrega,
                        hora_entrega=hora_entrega, # <--- PASSANDO A HORA PRO MODELO
                        massa=massa,
                        recheio=recheio,
                        tamanho=tamanho,
                        cobertura=cobertura,
                        valor=valor
                    )
                    
                    save_pedido(novo_pedido)
                    st.success(f"Pedido de {nome} salvo com sucesso!")
                    
                except Exception as e:
                    st.error(f"Erro ao salvar: {e}")