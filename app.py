import streamlit as st
from src.frontend.cadastro import render_cadastro
from src.frontend.dashboard import render_dashboard
# Importe o novo módulo
from src.frontend.financeiro import render_financeiro 

st.set_page_config(page_title="CakeFlow", page_icon="🎂", layout="wide")

st.markdown("""
<style>
    /* Remove padding excessivo do topo para caber mais na tela do celular */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }
    /* Deixa os botões mais clicáveis no mobile */
    .stButton button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("🎂 CakeFlow")
st.sidebar.markdown("Gestão Inteligente")

# Adicionei a opção Financeiro
pagina = st.sidebar.radio("Navegar", ["Novo Pedido","Dashboard", "Financeiro"])

if pagina == "Dashboard":
    render_dashboard()
elif pagina == "Financeiro":
    render_financeiro()
elif pagina == "Novo Pedido":
    render_cadastro()