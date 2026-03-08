import streamlit as st
import pandas as pd
from datetime import datetime

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestão de Estoque Clínica", layout="wide")

# CSS PARA BOTÕES À DIREITA
st.markdown("""
    <style>
    [data-testid="stSidebar"] { order: 2; border-left: 1px solid #ddd; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# LOGIN
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acesso ao Sistema Assistencial")
    with st.form("login"):
        u = st.text_input("Usuário")
        p = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if u == "fhomarcos@gmail.com" and p == "clinica2026":
                st.session_state.autenticado = True
                st.session_state.usuario = u
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos")
    st.stop()

# MENU LATERAL (DIREITA)
st.sidebar.title("MENU")
st.sidebar.write(f"👤 {st.session_state.usuario}")
uploaded_file = st.sidebar.file_uploader("Upload XLSX", type=['xlsx'])
st.sidebar.divider()

if st.sidebar.button("📊 Dashboard"): st.session_state.aba = "dash"
if st.sidebar.button("📝 Cadastro de Produtos"): st.session_state.aba = "cad_prod"
if st.sidebar.button("📥 Entrada de Produtos"): st.session_state.aba = "entrada"
if st.sidebar.button("📤 Saída de Produtos"): st.session_state.aba = "saida"
if st.sidebar.button("📂 Cadastro de Categoria"): st.session_state.aba = "categoria"
if st.sidebar.button("📦 Estoque"): st.session_state.aba = "estoque"
if st.sidebar.button("📅 Inventário"): st.session_state.aba = "inventario"
if st.sidebar.button("🚪 Sair"):
    st.session_state.autenticado = False
    st.rerun()

if 'aba' not in st.session_state: st.session_state.aba = "dash"

# TELAS
if st.session_state.aba == "dash":
    st.title("🏥 Gestão de Riscos e Suprimentos")
    c1, c2, c3 = st.columns(3)
    c1.metric("Itens Totais", "972")
    c2.metric("Críticos", "1", delta="Laranja")
    c3.metric("Status", "Conforme")

elif st.session_state.aba == "cad_prod":
    st.header("📝 Cadastro de Produtos")
    with st.form("f_prod"):
        st.text_input("Nome do Produto")
        st.text_input("Código")
        st.selectbox("Categoria", ["Medicamentos", "Materiais"])
        st.form_submit_button("Salvar")

elif st.session_state.aba == "entrada":
    st.header("📥 Entrada de Produtos")
    with st.form("f_ent"):
        col1, col2 = st.columns(2)
        col1.text_input("ID do Pedido")
        col2.date_input("Data")
        st.number_input("Quantidade", min_value=1)
        st.form_submit_button("Confirmar Entrada")

elif st.session_state.aba == "saida":
    st.header("📤 Saída de Produtos")
    with st.form("f_sai"):
        st.text_input("Código do Produto")
        st.number_input("Qtd Saída", min_value=1)
        st.form_submit_button("Registrar Baixa")

elif st.session_state.aba == "categoria":
    st.header("📂 Cadastro de Categoria")
    st.text_input("Nova Categoria")
    st.button("Cadastrar")

elif st.session_state.aba == "estoque":
    st.header("📦 Estoque Atual")
    df = pd.DataFrame({'Item': ['AAS', 'Aerolin'], 'Qtd': [29, 2]})
    st.table(df)

elif st.session_state.aba == "inventario":
    st.header("📅 Inventário por Período")
    d1 = st.date_input("De")
    d2 = st.date_input("Até")
    st.button("Gerar Relatório")