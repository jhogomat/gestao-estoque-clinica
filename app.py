import streamlit as st

# Configuração da página
st.set_page_config(page_title="Gestão de Insumos Pro", layout="wide")

# Estilização CSS para o visual SaaS/Moderno
st.markdown("""
    <style>
    /* Fundo e Container Principal */
    .stApp {
        background-color: #F4F7F6;
    }
    
    /* Estilo dos Cards e Elementos (Glassmorfismo leve) */
    div[data-testid="stVerticalBlock"] > div:has(div.stMetric) {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }

    /* Botões Modernos */
    .stButton>button {
        border-radius: 8px;
        border: none;
        transition: all 0.3s ease;
        font-weight: 500;
        width: 100%;
    }
    
    /* Cores específicas dos botões */
    div.stButton > button:first-child { background-color: #2563EB; color: white; } /* Dashboard/Azul */
    
    /* Efeito Hover */
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)
# --- MENU LATERAL ---
with st.sidebar:
    st.title("📦 Gestão Pro")
    st.write(f"Conectado como: **{st.session_state.get('nome_usuario', 'Usuário')}**")
    
    st.divider()
    st.subheader("🚀 Navegação")
    
    # Restauração dos botões de navegação
    if st.button("📊 Dashboard"):
        st.session_state.menu = "Dashboard"
    
    if st.button("📝 Cadastro de Produtos"):
        st.session_state.menu = "Cadastro de Produtos"
        
    if st.button("📂 Cadastro de Categoria"):
        st.session_state.menu = "Cadastro de Categoria"

    st.divider()
    st.subheader("🔄 Movimentação")
    
    if st.button("📥 Entrada de Produtos"):
        st.session_state.menu = "Entrada"
        
    if st.button("📤 Saída de Produtos"):
        st.session_state.menu = "Saída"

    st.divider()
    if st.button("🚪 Sair"):
        st.session_state.autenticado = False
        st.rerun()
# Lógica de exibição das telas
menu = st.session_state.get('menu', 'Dashboard')

if menu == "Dashboard":
    st.header("📊 Painel de Controle")
    # Seus indicadores de Estoque Total, Risco Assistencial e Validades
    
elif menu == "Entrada":
    st.header("📥 Entrada de Produtos")
    with st.container():
        col1, col2 = st.columns(2)
        id_pedido = col1.text_input("ID do Pedido")
        data = col2.date_input("Data")
        qtd = st.number_input("Quantidade", min_value=1)
        
        # Botão Verde conforme instrução
        if st.markdown('<button style="background-color: #22C55E; color: white; border-radius: 8px; width: 100%; padding: 10px; border: none;">Confirmar Entrada</button>', unsafe_allow_html=True):
            pass # Lógica de salvar

elif menu == "Saída":
    st.header("📤 Saída de Produtos")
    with st.container():
        codigo = st.text_input("Código do Produto")
        qtd_saida = st.number_input("Qtd Saída", min_value=1)
        
        # Botão Laranja conforme instrução
        if st.markdown('<button style="background-color: #F97316; color: white; border-radius: 8px; width: 100%; padding: 10px; border: none;">Registrar Baixa</button>', unsafe_allow_html=True):
            pass # Lógica de salvar
