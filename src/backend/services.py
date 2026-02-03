import urllib.parse
import re

def limpar_telefone(telefone) -> str:
    """
    Limpa o telefone, removendo .0 (erro do pandas) e caracteres não numéricos.
    """
    if not telefone:
        raise ValueError("Telefone vazio")

    # 1. Converte para string
    telefone_str = str(telefone)

    if telefone_str.endswith('.0'):
        telefone_str = telefone_str[:-2]

    # 3. Mantém apenas números (Remove parenteses, traços, espaços)
    numero_limpo = re.sub(r'\D', '', telefone_str)

    if numero_limpo == '':
        raise ValueError("Telefone sem dígitos")

    return numero_limpo

def gerar_link_whatsapp(telefone, mensagem: str) -> str:
    # A lógica aqui continua a mesma, mas agora recebe o telefone limpo corretamente
    try:
        telefone_limpo = limpar_telefone(telefone)
        mensagem_codificada = urllib.parse.quote(mensagem)
        return f"https://wa.me/55{telefone_limpo}?text={mensagem_codificada}"
    except ValueError:
        return ""