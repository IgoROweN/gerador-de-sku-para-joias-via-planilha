@echo off
title Automação de SKUs - Template
echo --- INICIANDO AUTOMACAO ---

:: ============================================================================
:: INSTRUÇÕES DE CONFIGURAÇÃO:
:: 1. Renomeie este arquivo para 'executar_automacao.bat' (ou crie uma cópia).
:: 2. Abaixo, substitua o caminho do 'activate.bat' pelo local onde o Conda
::    está instalado na sua máquina.
::    Exemplos comuns:
::    - C:\Users\SEU_USUARIO\anaconda3\Scripts\activate.bat
::    - C:\ProgramData\miniconda3\Scripts\activate.bat
:: ============================================================================

:: --- CONFIGURAR CAMINHO ABAIXO ---
set CAMINHO_CONDA=C:\Caminho\Para\Seu\Anaconda3\Scripts\activate.bat

:: Nome do ambiente virtual criado no projeto
set NOME_AMBIENTE=correcao_ref_etiquetas_joias

:: Validação simples para verificar se o usuário configurou
if not exist "%CAMINHO_CONDA%" (
    echo [ERRO] O caminho do Conda nao foi configurado corretamente.
    echo Edite o arquivo .bat e ajuste a variavel CAMINHO_CONDA.
    pause
    exit
)

:: Ativa o ambiente e roda o script
call "%CAMINHO_CONDA%" %NOME_AMBIENTE%
python gerador_ref_etiquetas.py

echo.
echo Processo finalizado.
pause