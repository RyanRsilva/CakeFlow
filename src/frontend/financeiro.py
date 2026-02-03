import streamlit as st
import pandas as pd
from datetime import date
from src.backend.database import get_all_pedidos


def render_financeiro():
    st.header("💰 Fluxo de Caixa")

    # 1. Carregar Dados
    df = get_all_pedidos()
    if df.empty:
        st.info("Cadastre pedidos para ver as estatísticas.")
        return

    # Tratamento de Data
    df["Data Entrega"] = pd.to_datetime(
        df["Data Entrega"], dayfirst=True, errors='coerce')
    df["Mês"] = df["Data Entrega"].dt.month.astype("Int64")  # type:ignore
    df["Ano"] = df["Data Entrega"].dt.year.astype("Int64")  # type:ignore

    # Filtros de Tempo (Mês Atual)
    hoje = date.today()
    df_mes = df[df["Data Entrega"].notna() & (
        df["Mês"] == hoje.month) & (df["Ano"] == hoje.year)]

    # --- MÉTRICAS PRINCIPAIS (KPIs) ---
    # Removemos cancelados da conta
    df_valido = df_mes[~df_mes["Status"].isin(["Cancelado"])]

    total_vendido = df_valido["Valor"].sum()
    qtde_pedidos = len(df_valido)
    ticket_medio = total_vendido / qtde_pedidos if qtde_pedidos > 0 else 0

    # O que já foi entregue vs O que vai entrar
    receita_realizada = df_valido[df_valido["Status"]
                                  == "Entregue"]["Valor"].sum()
    receita_prevista = total_vendido - receita_realizada

    # Visualização em Colunas Estilizadas
    st.markdown("### 📅 Resumo deste Mês")
    col1, col2, col3 = st.columns(3)
    col1.metric("Faturamento Total", f"R$ {total_vendido:.2f}")
    col2.metric("Já Recebido (Entregues)", f"R$ {receita_realizada:.2f}",
                delta=f"{len(df_valido[df_valido['Status'] == 'Entregue'])} bolos")
    col3.metric("A Receber (Produção)",
                f"R$ {receita_prevista:.2f}", delta_color="off")

    st.divider()

    # --- GRÁFICOS E RANKINGS ---
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("🏆 Top Recheios")
        if not df_valido.empty:
            # Agrupa por recheio e conta quantos pedidos
            top_recheios = df_valido["Recheio"].value_counts().head(5)
            st.bar_chart(top_recheios, color="#FF4B4B")
        else:
            st.write("Sem dados.")

    with c2:
        st.subheader("🍰 Top Massas")
        if not df_valido.empty:
            top_massas = df_valido["Massa"].value_counts().head(5)
            st.bar_chart(top_massas, color="#FFA500")
        else:
            st.write("Sem dados.")

    with c3:
        st.subheader("👥 Top Clientes")
        if not df_valido.empty:
            clientes_top = df_valido["Cliente"].value_counts().head(5)
            st.bar_chart(clientes_top, color="#4B8BFF")
        else:
            st.write("Sem dados.")

    # Tabela detalhada (Expansível)
    with st.expander("🔎 Ver Relatório Detalhado (Tabela)"):
        st.dataframe(
            df_valido[["Data Entrega", "Cliente", "Valor", "Status"]
                      ].sort_values("Data Entrega"),
            use_container_width=True
        )
