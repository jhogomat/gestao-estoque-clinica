import streamlit as st
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sistema Assistencial", layout="wide")

# BANCO DE DADOS DE USUÁRIOS (Mestre)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.title("🔐 Acesso ao Sistema Assistencial")
    with st.form("login_form"):
        # Use estes dados para entrar:
        user = st.text_input("Usuário (E-mail)")
        password = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            if user == "fhomarcos@gmail.com" and password == "clinica2026":
                st.session_state.autenticado = True
                st.rerun()
            else:
                st.error("⚠️ Usuário ou senha incorretos.")

if not st.session_state.autenticado:
    login()
    st.stop()

# SE LOGADO, MOSTRA O DASHBOARD
st.sidebar.title("MENU")
st.sidebar.write(f"Usuário: **fhomarcos@gmail.com**")
if st.sidebar.button("🚪 Sair"):
    st.session_state.autenticado = False
    st.rerun()

st.title("🏥 Gestão de Riscos e Suprimentos - Clínica")
st.success("Login realizado com sucesso! Bem-vindo ao painel de controle.")

# Exemplo de Dashboard de Risco (Como na sua imagem c69d28)
c1, c2, c3 = st.columns(3)
c1.metric("Total de Itens", "972")
c2.metric("Itens Críticos", "1", delta="Laranja")
c3.metric("Status", "Conforme (Verde)")