from dataclasses import dataclass
from datetime import date,time 

@dataclass
class Pedidos:
    ID: int
    cliente_nome: str
    cliente_telefone: str
    data_entrega: date
    hora_entrega:time
    massa: str
    recheio: str
    tamanho: str
    cobertura: str
    valor: float
    status: str = "Pendente"

    def to_dict(self):
        return {
            "ID" : self.ID, 
            "Cliente": self.cliente_nome,
            "WhatsApp": self.cliente_telefone,
            # AQUI ESTÁ A MUDANÇA PARA O PADRÃO BR (Dia/Mês/Ano)
            "Data Entrega": self.data_entrega.strftime("%d/%m/%Y") if self.data_entrega else "",
            "Hora": self.hora_entrega.strftime("%H:%M") if self.hora_entrega else "", 
            "Massa": self.massa,
            "Recheio": self.recheio,
            "Tamanho": self.tamanho,
            "Cobertura": self.cobertura,
            "Valor": self.valor,
            "Status": self.status
        }