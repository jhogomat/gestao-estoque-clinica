import streamlit as st
import streamlit.components.v1 as components

# Configuração da página para ocupar a tela toda
st.set_page_config(page_title="Gestão de Estoque Pro", layout="wide")

# O CÓDIGO HTML/CSS/JS QUE VOCÊ SOLICITOU
html_code = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <style>
        :root {
            --bg: #F4F7F6; --white: #FFFFFF; --primary: #2563EB;
            --success: #10B981; --warning: #F59E0B; --danger: #EF4444;
            --radius: 16px; --shadow: 0 10px 30px rgba(0,0,0,0.05);
        }
        body { background: var(--bg); font-family: 'Inter', sans-serif; padding: 20px; }
        
        /* Glassmorphism Effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: var(--radius);
            padding: 25px;
            box-shadow: var(--shadow);
            margin-bottom: 25px;
        }

        .header { display: flex; justify-content: space-between; align-items: center; }
        .btn { 
            padding: 12px 20px; border-radius: 10px; border: none; font-weight: 600;
            cursor: pointer; transition: 0.3s; display: flex; align-items: center; gap: 8px;
        }
        .btn-primary { background: var(--primary); color: white; }
        .btn-success { background: var(--success); color: white; }
        .btn-warning { background: var(--warning); color: white; }
        .btn-danger { background: rgba(239, 68, 68, 0.1); color: var(--danger); }
        .btn:hover { transform: translateY(-2px); filter: brightness(1.1); }

        .dashboard-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 25px 0; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th { text-align: left; padding: 15px; color: #64748B; font-size: 0.85rem; text-transform: uppercase; }
        td { padding: 15px; border-top: 1px solid #F1F5F9; background: white; }
        tr:first-child td:first-child { border-top-left-radius: var(--radius); }
        
        .status-pill { padding: 6px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; }
        .bg-green { background: #DCFCE7; color: #166534; }
        .bg-orange { background: #FEF3C7; color: #92400E; }

        .search-container { display: flex; gap: 15px; margin-bottom: 20px; }
        input { flex: 1; padding: 12px; border-radius: 10px; border: 1px solid #E2E8F0; outline: none; }
    </style>
</head>
<body>

    <div class="header glass-card">
        <div>
            <h1 style="color: #1E293B; font-size: 24px;">🏥 Gestão Assistencial Pro</h1>
            <p style="color: #64748B;">Bem-vindo, fhomarcos@gmail.com</p>
        </div>
        <div style="display: flex; gap: 10px;">
            <button class="btn btn-success" onclick="exportExcel()"><i class="fas fa-file-excel"></i> Inventário</button>
            <button class="btn btn-primary"><i class="fas fa-plus"></i> Novo Produto</button>
        </div>
    </div>

    <div class="dashboard-grid">
        <div class="glass-card" style="border-left: 6px solid var(--primary);">
            <p style="font-size: 13px; font-weight: 700; color: #64748B;">ESTOQUE TOTAL</p>
            <h2 style="font-size: 28px; margin-top: 5px;">R$ 14.520,00</h2>
        </div>
        <div class="glass-card" style="border-left: 6px solid var(--warning);">
            <p style="font-size: 13px; font-weight: 700; color: #64748B;">RISCO ASSISTENCIAL</p>
            <h2 style="font-size: 28px; color: var(--warning); margin-top: 5px;">02 ITENS</h2>
        </div>
        <div class="glass-card" style="border-left: 6px solid var(--danger);">
            <p style="font-size: 13px; font-weight: 700; color: #64748B;">VENCIMENTO (30D)</p>
            <h2 style="font-size: 28px; color: var(--danger); margin-top: 5px;">05 ITENS</h2>
        </div>
    </div>

    <div class="glass-card">
        <div class="search-container">
            <input type="text" placeholder="Pesquisar produto ou SKU...">
            <select style="padding: 10px; border-radius: 10px; border: 1px solid #E2E8F0;">
                <option>Medicamentos</option>
                <option>Insumos</option>
            </select>
        </div>

        <table id="tabela-estoque">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>SKU</th>
                    <th>Qtd</th>
                    <th>Preço</th>
                    <th>Status</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Aerolin 100mg</strong></td>
                    <td>AE2-26</td>
                    <td id="q1">2</td>
                    <td>R$ 45,00</td>
                    <td><span class="status-pill bg-orange">Crítico</span></td>
                    <td style="display: flex; gap: 8px;">
                        <button class="btn btn-success" style="padding: 5px 10px;" onclick="add(1)">+</button>
                        <button class="btn btn-warning" style="padding: 5px 10px;" onclick="add(-1)">-</button>
                        <button class="btn btn-danger" style="padding: 5px 10px;"><i class="fas fa-trash"></i></button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        function exportExcel() {
            const table = document.getElementById("tabela-estoque");
            const wb = XLSX.utils.table_to_book(table);
            XLSX.writeFile(wb, "Inventario_Clinica.xlsx");
        }
        function add(val) {
            let q = document.getElementById("q1");
            let novo = parseInt(q.innerText) + val;
            if(novo >= 0) q.innerText = novo;
        }
    </script>
</body>
</html>
"""

# Renderiza o HTML no Streamlit
components.html(html_code, height=1000, scrolling=True)