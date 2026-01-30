import pandas as pd
import os

# Lista de Códigos que aceitamos como válidos
# Se a primeira palavra da descrição for um desses, ela vira o prefixo.
CODIGOS_VALIDOS = [
    'AL', 'AN', 'BR', 'CJ', 'PS', 'CR', 'TN', 'PG', 'CL'
    # Adicione aqui outros se houver (ex: 'CL' se colar for separado)
]

# --- LÓGICA ANTIGA (RESERVA TÉCNICA) ---
# Caso precise voltar a procurar palavras no meio da frase, descomente isso:
# mapa_antigo = {
#    'ALIANÇA': 'AL', 'ANEL': 'AN', 'BRINCO': 'BR',
#    'CONJUNTO': 'CJ', 'PULSEIRA': 'PS', 'CORRENTE': 'CR',
#    'TORNOZELEIRA': 'TN', 'PINGENTE': 'PG'
# }

def definir_prefixo(descricao):
    # Proteção contra células vazias
    if not isinstance(descricao, str):
        return 'XX'
    
    # Limpa espaços extras e separa as palavras
    descricao = descricao.upper().strip()
    palavras = descricao.split()
    
    if not palavras:
        return 'XX'
    
    # --- NOVA LÓGICA: PEGAR A PRIMEIRA PALAVRA ---
    primeira_palavra = palavras[0]
    
    # Limpa pontos ou virgulas que possam estar colados (ex: "BR.")
    primeira_palavra = primeira_palavra.replace('.', '').replace(',', '')

    # Verifica se essa primeira palavra é um código válido
    if primeira_palavra in CODIGOS_VALIDOS:
        return primeira_palavra
    
    # --- LÓGICA ANTIGA (COMENTADA) ---
    # Se a primeira palavra não for o código (ex: a descrição começa com "OURO"),
    # descomente as linhas abaixo para tentar achar o código no meio do texto:
    #
    # for chave, codigo in mapa_antigo.items():
    #     if chave in descricao:
    #         return codigo
            
    return 'XX' # Retorna XX se não achar nada

def gerar_sku(row):
    try:
        valor_venda = row['Vr.Venda']
        descricao = row['Descrição']
        
        # Tratamento do Valor
        if isinstance(valor_venda, str):
            valor_venda = valor_venda.replace('.', '').replace(',', '.')
            
        valor_float = float(valor_venda)
        parte_inteira = int(valor_float)
        centavos = int(round((valor_float - parte_inteira) * 100))
        
        # Define o Prefixo usando a nova lógica (primeira palavra)
        prefixo = definir_prefixo(descricao)
        
        # Monta o SKU
        return f"{prefixo}{parte_inteira}R11{centavos:02d}0"
        
    except Exception:
        return "ERRO"

# --- EXECUÇÃO ---
arquivo_entrada = 'planilha_joias_ref.xlsx'
arquivo_saida = 'planilha_com_etiquetas_final.xlsx'

print(f"--- Processando {arquivo_entrada} ---")

if os.path.exists(arquivo_entrada):
    # --- CORREÇÃO APLICADA AQUI ---
    # dtype={'NOME_COLUNA': str} força o Pandas a ler como TEXTO.
    # Isso preserva os zeros à esquerda (ex: '0789' continua '0789').
    df = pd.read_excel(
        arquivo_entrada, 
        dtype={'Cód.Barra': str, 'Código': str}
    )
    
    # Aplica a função
    df['Ref./SKU'] = df.apply(gerar_sku, axis=1)
    
    # Salva
    df.to_excel(arquivo_saida, index=False)
    
    # Relatório rápido
    erros = df[df['Ref./SKU'].astype(str).str.startswith('XX')]
    print("-" * 30)
    if erros.empty:
        print("SUCESSO! Todos os itens identificados pelo código inicial.")
    else:
        print(f"AVISO: {len(erros)} itens ficaram como 'XX'.")
        print("Verifique se a descrição desses itens começa com o código correto (AN, BR, etc).")
        print("Exemplos de descrições falhas:")
        print(erros['Descrição'].head().tolist())
    print("-" * 30)
else:
    print("Arquivo não encontrado.")