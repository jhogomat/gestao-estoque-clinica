import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO E ESTILO ---
st.set_page_config(page_title="Sistema Assistencial - Clínica", layout="wide")

st.markdown("""
    <style>
    /* Padronização visual conforme imagens */
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    .btn-salvar { background-color: #28a745 !important; color: white !important; }
    .btn-limpar { background-color: #6c757d !important; color: white !important; }
    .btn-fechar { background-color: #dc3545 !important; color: white !important; }
    
    /* Posicionamento do Menu à Direita */
    [data-testid="stSidebar"] { order: 2; border-left: 1px solid #ddd; }
    section[data-testid="stSidebar"] > div { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTÃO DE USUÁRIOS E AUTENTICAÇÃO ---
if 'db_usuarios' not in st.session_state:
    # Base inicial de usuários (Pode ser salva em CSV depois)
    st.session_state.db_usuarios = {
        "fhomarcos@gmail.com": {"senha": "123", "nome": "Marcos", "perfil": "Admin"},
        "enfermagem@clinica.com": {"senha": "456", "nome": "Equipe Enfermagem", "perfil": "Assistencial"}
    }

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.title("🔐 Acesso ao Sistema Assistencial")
    with st.container():
        user_input = st.text_input("Usuário (E-mail)")
        pass_input = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if user_input in st.session_state.db_usuarios and st.session_state.db_usuarios[user_input]["senha"] == pass_input:
                st.session_state.autenticado = True
                st.session_state.usuario_logado = user_input
                st.session_state.nome_usuario = st.session_state.db_usuarios[user_input]["nome"]
                st.rerun()
            else:
                st.error("⚠️ Usuário ou senha inválidos ou expirados.")

if not st.session_state.autenticado:
    login()
    st.stop()

# --- MENU LATERAL (À DIREITA) ---
st.sidebar.title("MENU")
st.sidebar.write(f"Conectado como: **{st.session_state.nome_usuario}**")

# Botão de Upload (Canto Superior Direito)
st.sidebar.subheader("📂 Integração")
uploaded_file = st.sidebar.file_uploader("Upload base XLSX", type=['xlsx'])

st.sidebar.divider()
st.sidebar.subheader("Navegação")

# Botões Padronizados de Cima para Baixo
if st.sidebar.button("📊 Dashboard"): st.session_state.menu = "Dashboard"
if st.sidebar.button("📝 Cadastro de Produtos"): st.session_state.menu = "Cad_Prod"
if st.sidebar.button("📥 Entrada de Produtos"): st.session_state.menu = "Entrada"
if st.sidebar.button("📤 Saída de Produtos"): st.session_state.menu = "Saida"
if st.sidebar.button("📂 Cadastro de Categoria"): st.session_state.menu = "Categoria"
if st.sidebar.button("📦 Estoque"): st.session_state.menu = "Estoque"
if st.sidebar.button("📅 Inventário"): st.session_state.menu = "Inventario"
if st.sidebar.button("👥 Gerenciar Usuários"): st.session_state.menu = "Usuarios"
if st.sidebar.button("🚪 Sair"): 
    st.session_state.autenticado = False
    st.rerun()

# Estado inicial do menu
if 'menu' not in st.session_state: st.session_state.menu = "Dashboard"

# --- LÓGICA DOS FORMULÁRIOS ---

if st.session_state.menu == "Dashboard":
    st.title("📊 Painel de Monitoramento")
    c1, c2, c3 = st.columns(3)
    c1.metric("Itens Totais", "972")
    c2.metric("Críticos", "12", delta="Laranja")
    c3.metric("Status", "Conforme")

elif st.session_state.menu == "Cad_Prod":
    st.title("NOVO PRODUTO")
    with st.container():
        col1, col2 = st.columns([1, 2])
        id_prod = col1.text_input("ID")
        codigo = col2.text_input("CÓDIGO")
        nome = st.text_input("NOME")
        c_sal, c_lim, c_fec = st.columns(3)
        if c_sal.button("Salvar", key="save_p"): st.success("Produto Salvo!")
        c_lim.button("Limpar", key="clear_p")
        c_fec.button("Fechar", key="close_p")

elif st.session_state.menu == "Entrada":
    st.title("CADASTRO DE PEDIDOS (ENTRADA)")
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.text_input("ID do Pedido")
        col2.date_input("Data")
        col3.text_input("Hora")
        st.selectbox("Produto", ["Selecione um Produto", "AAS 100 MG", "AEROLIN"])
        st.text_input("Solicitante")
        st.text_area("Observação")
        c_sal, c_lim, c_fec = st.columns(3)
        c_sal.button("Salvar", key="save_e")
        c_lim.button("Limpar", key="clear_e")
        c_fec.button("Fechar", key="close_e")

elif st.session_state.menu == "Usuarios":
    st.title("👥 Gerenciamento de Usuários e Senhas")
    
    # Adicionar Novo Usuário
    with st.expander("➕ Adicionar Novo Usuário"):
        new_mail = st.text_input("E-mail")
        new_name = st.text_input("Nome")
        new_pass = st.text_input("Senha", type="password")
        if st.button("Cadastrar"):
            st.session_state.db_usuarios[new_mail] = {"senha": new_pass, "nome": new_name, "perfil": "Assistencial"}
            st.success("Novo usuário ativado!")
            
    # Listar Usuários
    st.write("### Usuários Ativos")
    df_users = pd.DataFrame.from_dict(st.session_state.db_usuarios, orient='index')
    st.table(df_users[['nome', 'perfil']])