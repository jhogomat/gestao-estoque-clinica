import streamlit as st
import pandas as pd
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SafeStock | Gestão Assistencial",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CSS CUSTOMIZADO (ESTILO SAAS / MODERN)
st.markdown("""
    <style>
    /* Fundo da aplicação */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Customização da Sidebar */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }

    /* Cards de Dashboard (Neumorfismo Leve) */
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        border: 1px solid #F1F5F9;
        text-align: center;
    }

    /* Botões Modernos */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: none;
        background-color: #2563EB;
        color: white;
        transition: all 0.3s ease;
        font-weight: 500;
        height: 45px;
    }
    
    .stButton>button:hover {
        background-color: #1D4ED8;
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        transform: translateY(-1px);
    }

    /* Inputs arredondados */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 8px !important;
    }

    /* Tabelas */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE LOGIN (Simplificada para o exemplo)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
        st.title("🔐 SafeStock")
        st.subheader("Gestão de Riscos & Qualidade")
        with st.form("login"):
            u = st.text_input("E-mail institucional")
            p = st.text_input("Senha", type="password")
            if st.form_submit_button("Acessar Painel"):
                if u == "fhomarcos@gmail.com" and p == "clinica2026":
                    st.session_state.autenticado = True
                    st.session_state.usuario = u
                    st.rerun()
                else:
                    st.error("Credenciais inválidas")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. MENU LATERAL REESTRUTURADO
with st.sidebar:
    st.markdown(f"### 🏥 SafeStock")
    st.caption(f"Logado como: **{st.session_state.usuario}**")
    st.divider()
    
    # Navegação com ícones
    if st.button("📊 Dashboard Geral"): st.session_state.aba = "dash"
    if st.button("📦 Estoque Atual"): st.session_state.aba = "estoque"
    st.markdown("---")
    st.markdown("### Operações")
    if st.button("📥 Entrada de Itens"): st.session_state.aba = "entrada"
    if st.button("📤 Registro de Saída"): st.session_state.aba = "saida"
    st.markdown("---")
    st.markdown("### Configurações")
    if st.button("📝 Cadastro de Produtos"): st.session_state.aba = "cad_prod"
    if st.button("📂 Categorias"): st.session_state.aba = "categoria"
    if st.button("📅 Auditoria/Inventário"): st.session_state.aba = "inventario"
    
    st.sidebar.markdown("<br>"*5, unsafe_allow_html=True)
    if st.button("🚪 Sair do Sistema"):
        st.session_state.autenticado = False
        st.rerun()

if 'aba' not in st.session_state: st.session_state.aba = "dash"

# 5. CONTEÚDO PRINCIPAL
if st.session_state.aba == "dash":
    st.title("📊 Dashboard de Gestão de Riscos")
    st.markdown("Monitoramento de conformidade e níveis críticos de assistência.")
    
    # Cards de Métricas Estilizados
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="metric-card"><p style="color:#64748B;">Itens Totais</p><h2>972</h2></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="metric-card"><p style="color:#64748B;">Riscos (Qtd Mínima)</p><h2 style="color:#F59E0B;">08</h2></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="metric-card"><p style="color:#64748B;">Validade Próxima</p><h2 style="color:#EF4444;">03</h2></div>', unsafe_allow_html=True)
    with m4:
        st.markdown('<div class="metric-card"><p style="color:#64748B;">Status Geral</p><h2 style="color:#10B981;">Conforme</h2></div>', unsafe_allow_html=True)

    st.divider()
    
    # Exemplo de Gráfico ou Tabela de Risco
    col_inf1, col_inf2 = st.columns(2)
    with col_inf1:
        st.subheader("⚠️ Alertas de Reposição")
        df_alert = pd.DataFrame({'Item': ['Luva Estéril', 'Soro Fisiológico'], 'Qtd': [5, 12], 'Status': ['Crítico', 'Atenção']})
        st.table(df_alert)
    with col_inf2:
        st.subheader("📈 Movimentação (Últimos 7 dias)")
        st.line_chart(pd.DataFrame([10, 25, 15, 40, 32, 28, 45]))

elif st.session_state.aba == "estoque":
    st.header("📦 Gerenciamento de Estoque")
    # Barra de busca rápida
    search = st.text_input("🔍 Buscar por nome ou código do produto...")
    
    df = pd.DataFrame({
        'Código': ['MT-001', 'MD-042', 'MT-088'],
        'Item': ['Gaze 7,5x7,5', 'Dipirona 500mg/ml', 'Seringa 5ml'],
        'Categoria': ['Materiais', 'Medicamentos', 'Materiais'],
        'Qtd Atual': [120, 45, 12],
        'Lote': ['2024AX', '9988-B', 'L-09']
    })
    st.dataframe(df, use_container_width=True, hide_index=True)

elif st.session_state.aba == "entrada":
    st.header("📥 Entrada de Materiais")
    with st.container():
        st.info("Utilize esta tela para registrar o recebimento de notas fiscais e doações.")
        with st.form("f_ent", clear_on_submit=True):
            c1, c2 = st.columns(2)
            c1.text_input("Número do Pedido / NF")
            c2.date_input("Data de Recebimento")
            st.selectbox("Fornecedor", ["Distribuidora Saúde", "Almoxarifado Central"])
            st.number_input("Quantidade", min_value=1)
            if st.form_submit_button("Confirmar Entrada no Sistema"):
                st.success("Entrada registrada com sucesso!")

# ... Outras abas seguem o mesmo padrão de containers e colunas ...