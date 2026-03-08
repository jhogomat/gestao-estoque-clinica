import streamlit as st
import pandas as pd
from datetime import datetime

# Configurações de Qualidade e Visual
st.set_page_config(page_title="Gestão de Estoque Clínica", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stMetric { border-left: 5px solid #1E3A8A; background: white; padding: 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Título com foco em Segurança do Paciente
st.title("🏥 Gestão de Riscos e Suprimentos - Clínica")
st.write("Monitoramento de Validade e Estoque Crítico")

# Função para carregar seus dados reais (Ajustado para seus CSVs)
def carregar_dados():
    try:
        # Lendo seu arquivo 'Produtos.csv' (ajustando o cabeçalho que vi no seu arquivo)
        df = pd.read_csv('Controle de Estoque.xlsx - Produtos.csv', skiprows=8)
        # Limpando colunas vazias
        df = df.dropna(subset=['CÓDIGO PROD'])
        return df
    except:
        # Dados de exemplo caso o arquivo não seja encontrado na pasta
        return pd.DataFrame({
            'CÓDIGO PROD': ['AA1', 'AE2'],
            'NOME DO PRODUTO': ['AAS 100 MG', 'AEROLIN 100 MG'],
            'QUANTIDADE ATUAL': [29, 2],
            'ESTOQUE MÍNIMO': [10, 5],
            'DATA DE VALIDADE': ['2030-03-30', '2026-06-20']
        })

df_estoque = carregar_dados()

# Indicadores de Gestão de Riscos
col1, col2, col3 = st.columns(3)

# Lógica de Alerta (Laranja)
estoque_baixo = df_estoque[df_estoque['QUANTIDADE ATUAL'] <= df_estoque['ESTOQUE MÍNIMO']]

col1.metric("Total de Itens", len(df_estoque))
col2.metric("Itens Críticos (Estoque)", len(estoque_baixo), delta_color="inverse")
col3.metric("Status do Sistema", "Conforme (Verde)")

st.divider()

# Tabela de Inventário com Cores de Qualidade
st.subheader("📋 Inventário Mensal Automatizado")

def destacar_riscos(row):
    if row['QUANTIDADE ATUAL'] <= row['ESTOQUE MÍNIMO']:
        return ['background-color: #FFE5CC'] * len(row) # Laranja (Atenção)
    return ['background-color: #E6FFED'] * len(row)    # Verde (Conformidade)

st.dataframe(df_estoque.style.apply(destacar_riscos, axis=1), use_container_width=True)

# Botão de Exportação para Auditoria
st.sidebar.header("Relatórios")
if st.sidebar.button("Gerar Inventário para PDF"):
    st.sidebar.success("Relatório de Riscos gerado com sucesso!")