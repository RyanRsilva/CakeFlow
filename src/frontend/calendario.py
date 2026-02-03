from streamlit_calendar import calendar

def render_calendario(df):
    """
    Renderiza o componente de calendário visual.
    Recebe o DataFrame já filtrado e tratado.
    """
    events = []
    
    # Se o DataFrame vier vazio, não trava
    if not df.empty:
        for _, row in df.iterrows():
            # Define cor: Cinza se cancelado, Vermelho normal, verde finalizado
            cor = "#808080" 
            if "Cancelado" in str(row["Status"]):
                cor = "#FF4B4B" 
                
            if "Entregue" in str(row["Status"]):
                cor = "#219B3A"
            
            events.append({
                "title": f"{row['Cliente']} ({row['Massa']})",
                "start": row["Data Entrega"].isoformat(), 
                "backgroundColor": cor,
                "borderColor": cor,
                # Dica: 'allDay': True deixa o evento mais compacto na visualização
                "allDay": True 
            })

    calendar_options = {
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,listWeek"
        },
        "initialView": "dayGridMonth",
        "locale": "pt-br", 
        "height": "500px", 
        "contentHeight": "auto"
    }
    
    # Renderiza o componente
    # key="calendar" evita que ele recarregue à toa
    calendar(events=events, options=calendar_options, key="calendar_widget")
    