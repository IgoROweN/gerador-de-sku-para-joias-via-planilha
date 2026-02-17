import pandas as pd
import os

# Lista de Códigos que aceitamos como válidos
# Se a primeira palavra da descrição for um desses, ela vira o prefixo.
CODIGOS_VALIDOS = [
    'AL', 'AN', 'BR', 'CJ', 'PS', 'CR', 'TN', 'PG', 'CL'
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
        
        # Define o Prefixo (ex: "BR")
        prefixo = definir_prefixo(descricao)
        
        # Se o prefixo tiver menos de 2 letras (erro), retorna ERRO
        if len(prefixo) < 2:
            return "ERRO_PREFIXO"

        # --- NOVA LÓGICA DE MONTAGEM DO SKU ---
        # Exemplo: Valor 175.80, Prefixo BR
        # 1. Primeira Letra (B)
        # 2. Fixo "0"
        # 3. Valor Inteiro (175)
        # 4. Segunda Letra (R)
        # 5. Fixo "11"
        # 6. Centavos (80)
        # 7. Fixo "0"
        # Resultado: B0175R11800
        
        sku = f"{prefixo[0]}0{parte_inteira}{prefixo[1]}11{centavos:02d}0"
        return sku
        
    except Exception:
        return "ERRO"

# --- EXECUÇÃO ---
arquivo_entrada = 'planilha_joias_ref.xlsx'
arquivo_saida = 'planilha_com_etiquetas_final.xlsx'

print(f"--- Processando {arquivo_entrada} ---")

if os.path.exists(arquivo_entrada):
    # dtype={'NOME_COLUNA': str} força o Pandas a ler como TEXTO.
    df = pd.read_excel(
        arquivo_entrada, 
        dtype={'Cód.Barra': str, 'Código': str}
    )
    
    # Aplica a função
    df['Ref./SKU'] = df.apply(gerar_sku, axis=1)
    
    # Salva
    df.to_excel(arquivo_saida, index=False)
    
    # Relatório rápido
    erros = df[df['Ref./SKU'].astype(str).str.startswith('X')] # Pega XX ou X...
    print("-" * 30)
    if erros.empty:
        print("SUCESSO! Todos os itens identificados e decodificados corretamente.")
    else:
        print(f"AVISO: {len(erros)} itens ficaram com prefixo desconhecido (XX).")
        print("Verifique se a descrição desses itens começa com o código correto.")
        print(erros['Descrição'].head().tolist())
    print("-" * 30)
else:
    print("Arquivo não encontrado.")