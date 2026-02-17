# 💎 Automação de Geração de SKUs para Joias

Este projeto é uma ferramenta de automação desenvolvida em Python para processar planilhas de estoque de joalherias. O sistema lê descrições de produtos e preços de venda, gerando automaticamente SKUs (Stock Keeping Units) codificados e padronizados.

## 🎯 Objetivo
O principal objetivo é automatizar a criação de etiquetas que "mascaram" o preço de venda dentro do código de referência. Esta é uma prática comum no atacado para que revendedores saibam o preço de custo/venda sem expor o valor explicitamente ao consumidor final.

## ⚙️ Funcionalidades

- **Leitura de Planilhas:** Processamento eficiente de arquivos Excel (`.xlsx`) utilizando `pandas`.
- **Categorização Automática:** Identifica o tipo de produto (Anel, Brinco, Colar) baseando-se no código inicial da descrição (ex: `AN`, `BR`) ou palavras-chave.
- **Mascaramento de Preço (Algoritmo):** Converte o valor monetário em um código alfanumérico intercalado com o prefixo do produto.
  - *Lógica:* `[LETRA_1] + "0" + [PARTE_INTEIRA] + [LETRA_2] + "11" + [CENTAVOS] + "0"`
  - *Exemplo:* Um Brinco (**BR**) de **R$ 175,80** vira o SKU **B0175R11800**.
- **Sanitização de Dados:** Trata inconsistências comuns em planilhas (vírgulas vs pontos) e preserva zeros à esquerda em Códigos de Barras.
- **Interface Simplificada:** Inclui template de script `.bat` para execução rápida em ambiente Windows.

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Pandas:** Manipulação e análise de dados.
- **OpenPyXL:** Leitura e escrita de arquivos Excel.
- **Anaconda/Conda:** Gerenciamento de ambiente virtual.

## 🚀 Como Executar

### Pré-requisitos
Certifique-se de ter o Python instalado ou o gerenciador Conda.

### 1. Clone o repositório:
```bash
git clone https://github.com/IgoROweN/gerador-de-sku-para-joias-via-planilha.git
cd gerador-de-sku-para-joias-via-planilha
```

### 2. Instale as dependências:
```bash
pip install pandas openpyxl
# Ou via Conda
conda install pandas openpyxl
```

### 3. Executando no Windows (Automático)

Para facilitar o uso diário, o projeto inclui um template de execução `.bat`. Siga os passos para configurar o seu ambiente local:

1. Localize o arquivo `executar_automacao_TEMPLATE.bat`.
2. Crie uma cópia deste arquivo e renomeie para `executar_automacao.bat` (este arquivo será ignorado pelo Git).
3. Clique com o botão direito no novo arquivo > **Editar**.
4. Ajuste a variável `CAMINHO_CONDA` para apontar para a instalação do seu Anaconda/Miniconda:

```bat
set CAMINHO_CONDA=C:\Users\SEU_USUARIO\anaconda3\Scripts\activate.bat
```

5. Salve e feche. Agora basta dar um duplo clique para rodar a automação.

### 4. Executando via Terminal (Manual)

Caso prefira rodar manualmente:

```bash
python gerador_ref_etiquetas.py
```

## 📋 Regras de Negócio (Prefixos)

O sistema reconhece os seguintes padrões no início da descrição do produto (ex: `"AN ANEL SOLITARIO"`).

| Código | Tipo de Produto |
|------|-----------------|
| AL | Aliança |
| AN | Anel |
| BR | Brinco |
| CJ | Conjunto |
| CR | Corrente |
| PS | Pulseira |
| TN | Tornozeleira |
| PG | Pingente |
| CL | Colar |

## 🔄 Configuração Avançada (Lógica Alternativa)

Por padrão, o script espera que a descrição comece com o código (ex: `AN ...`).

Caso suas planilhas não sigam esse padrão (ex: descrições como `"Anel de Ouro"` sem o código no início), o código possui uma **Lógica de Reserva** implementada, mas desativada.

### Para ativar:

1. Abra o arquivo `gerador_ref_etiquetas.py`.
2. Localize e descomente o dicionário `mapa_antigo`.
3. Na função `definir_prefixo`, descomente o bloco final que percorre esse mapa procurando palavras-chave na descrição.

Isso permitirá que o sistema identifique automaticamente o tipo de produto mesmo sem o prefixo inicial.

## 📝 Autor

Desenvolvido por **Igor Owen**.  
Projeto criado para otimização de processos de ERP e logística.
