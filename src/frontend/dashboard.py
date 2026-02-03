import streamlit as st
import pandas as pd
from datetime import date, timedelta
from src.frontend.calendario import render_calendario
from src.backend.database import get_all_pedidos, update_status_by_id
from src.backend.services import gerar_link_whatsapp
import time

def render_dashboard():
    st.header("📊 Painel de Produção")
    
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    df = get_all_pedidos()
    
    if df.empty:
        st.info("Nenhum pedido no sistema.")
        return

    # Tratamento de dados
    df["Data Entrega"] = pd.to_datetime(df["Data Entrega"], dayfirst=True, errors='coerce').dt.date
    df = df.dropna(subset=["Data Entrega"])

    tab_kanban, tab_calendario = st.tabs(["📋 Kanban", "📅 Calendário"])
    
    with tab_kanban:
        render_kanban(df)
        
    with tab_calendario:
        render_calendario(df)

def render_kanban(df):
    # Removemos Entregues/Cancelados da visão principal
    df_ativo = df[~df["Status"].isin(["Entregue", "Cancelado"])]
    
    col1, col2, col3 = st.columns(3)
    
    # --- COLUNA 1: A FAZER ---
    with col1:
        st.subheader("📝 A Fazer")
        df_todo = df_ativo[df_ativo["Status"].isin(["Pendente", "A Fazer"])]
        for _, row in df_todo.iterrows():
            criar_card_pedido(row, "Pendente")

    # --- COLUNA 2: EM PRODUÇÃO ---
    with col2:
        st.subheader("🥣 Em Produção")
        df_doing = df_ativo[df_ativo["Status"] == "Produção"]
        for _, row in df_doing.iterrows():
            criar_card_pedido(row, "Produção")

    # --- COLUNA 3: PRONTO / FINALIZADO (Mudamos aqui) ---
    with col3:
        st.subheader("🎁 Pronto / Finalizado")
        # Agora buscamos pelo status 'Pronto'
        df_ready = df_ativo[df_ativo["Status"] == "Pronto"]
        for _, row in df_ready.iterrows():
            criar_card_pedido(row, "Pronto")

def criar_card_pedido(row, estagio_atual):
    # Cores indicativas
    cores = {"Pendente": "red", "Produção": "orange", "Pronto": "green"}
    cor = cores.get(estagio_atual, "grey")

    with st.container(border=True):
        data_formatada = row['Data Entrega'].strftime('%d/%m')
        hora = row.get("Hora", "")
        
        st.markdown(f"**#{int(row['ID'])} - {row['Cliente']}**")
        st.caption(f"📅 {data_formatada} às {hora}h | {row['Massa']}")
        
        with st.expander("Detalhes & Ações"):
            st.write(f"🍰 {row['Recheio']} | 📏 {row['Tamanho']}")
            st.write(f"🎨 {row['Cobertura']}")
            st.write(f"💰 R$ {row['Valor']:.2f}")
            
            st.markdown("---")
            
            c1, c2 = st.columns(2)
            
            # --- LÓGICA DO KANBAN COM WHATSAPP ---
            
            # 1. De Pendente -> Produção
            if estagio_atual == "Pendente":
                if c1.button("🥣 Produzir", key=f"prod_{row['ID']}"):
                    update_status_by_id(row['ID'], "Produção")
                    st.rerun()
            
            # 2. De Produção -> Pronto (AQUI TEM O AVISO)
            elif estagio_atual == "Produção":
                if c1.button("🎁 Finalizar", key=f"finish_{row['ID']}"):
                    update_status_by_id(row['ID'], "Pronto")
                    st.toast(f"Bolo de {row['Cliente']} marcado como PRONTO! 🎉")
                    time.sleep(1)
                    st.rerun()
            
            # 3. De Pronto -> Entregue (Sai do Quadro)
            elif estagio_atual == "Pronto":
                # Mostra o botão de WhatsApp destacado para avisar que está pronto
                msg_pronto = f"Olá {row['Cliente']}! Seu bolo já está pronto e ficou lindo! 🎂 Pode vir buscar ou combinamos a entrega?"
                link_pronto = gerar_link_whatsapp(str(row['WhatsApp']), msg_pronto)
                st.link_button("📲 AVISAR CLIENTE", link_pronto, type="primary")

                if c1.button("✅ Entreguei", key=f"deliver_{row['ID']}"):
                    update_status_by_id(row['ID'], "Entregue")
                    st.success("Pedido finalizado com sucesso!")
                    time.sleep(1)
                    st.rerun()

            # Botão Cancelar
            if c2.button("❌ Cancelar", key=f"cancel_{row['ID']}"):
                update_status_by_id(row['ID'], "Cancelado")
                st.rerun()

            # Link Genérico do WhatsApp (para dúvidas gerais)
            if estagio_atual != "Pronto":
                msg = f"Olá {row['Cliente']}, sobre o pedido #{int(row['ID'])}..."
                link = gerar_link_whatsapp(str(row['WhatsApp']), msg)
                if link:
                    st.markdown(f"[💬 WhatsApp]({link})")