import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="Gestão de Insumos Pro", layout="wide")

# CSS para Design SaaS / Glassmorphism
st.markdown("""
    <style>
    .stApp { background-color: #F4F7F6; }
    [data-testid="stSidebar"] { background-color: #FFFFFF; border-right: 1px solid #E2E8F0; }
    
    /* Estilo dos Botões do Menu */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        background-color: white;
        transition: all 0.3s;
        text-align: left;
        padding: 10px;
    }
    .stButton>button:hover {
        border-color: #2563EB;
        color: #2563EB;
        transform: translateX(5px);
    }
    
    /* Cards de Indicadores */
    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATERAL (Restauração dos Itens) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063171.png", width=50)
    st.title("Menu")
    st.write(f"👤 fhomarcos@gmail.com")
    
    st.divider()
    if st.button("📊 Painel de controle"): st.session_state.pagina = "home"
    if st.button("📝 Cadastro de Produtos"): st.session_state.pagina = "cad_prod"
    if st.button("📥 Entrada de Produtos"): st.session_state.pagina = "entrada"
    if st.button("📤 Saída de Produtos"): st.session_state.pagina = "saida"
    if st.button("📂 Cadastro de Categoria"): st.session_state.pagina = "cad_cat"
    if st.button("📦 Estoque"): st.session_state.pagina = "estoque"
    if st.button("📋 Inventário"): st.session_state.pagina = "inventario"
    
    st.divider()
    if st.button("🚪 Sair"): st.session_state.autenticado = False

# Lógica de Navegação
if "pagina" not in st.session_state: st.session_state.pagina = "home"

if st.session_state.pagina == "home":
    st.header("📊 Gestão de Riscos e Suprimentos")
    
    # Cards de Indicadores (Dashboard)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><p style="color:#64748B">ESTOQUE TOTAL</p><h2>R$ 14.520,00</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card" style="border-left:5px solid #F59E0B"><p style="color:#64748B">RISCO ASSISTENCIAL</p><h2 style="color:#F59E0B">02 ITENS</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card" style="border-left:5px solid #EF4444"><p style="color:#64748B">VALIDADES (30D)</p><h2 style="color:#EF4444">05 ITENS</h2></div>', unsafe_allow_html=True)

elif st.session_state.pagina == "entrada":
    st.header("📥 Entrada de Produtos")
    with st.container(border=True):
        col_a, col_b = st.columns(2)
        col_a.text_input("ID do Pedido")
        col_b.date_input("Data")
        st.number_input("Quantidade", min_value=1)
        st.button("Confirmar Entrada", type="primary") # Azul vibrante

elif st.session_state.pagina == "saida":
    st.header("📤 Saída de Produtos")
    with st.container(border=True):
        st.text_input("Código do Produto")
        st.number_input("Qtd Saída", min_value=1)
        # Botão Laranja via CSS customizado ou nativo
        st.button("Registrar Baixa", use_container_width=True)