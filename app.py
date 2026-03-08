import streamlit as st
import streamlit.components.v1 as components

# Configuração da tela cheia
st.set_page_config(page_title="Gestão Assistencial Pro", layout="wide")

# O SEU NOVO DESIGN MODERNO (SPA)
html_completo = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
    <style>
        :root {
            --bg: #F4F7F6; --primary: #2563EB; --success: #10B981;
            --warning: #F59E0B; --danger: #EF4444; --radius: 16px;
        }
        body { background: var(--bg); font-family: sans-serif; padding: 20px; }
        .glass-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border-radius: var(--radius);
            padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.3);
        }
        .header { display: flex; justify-content: space-between; align-items: center; }
        .dashboard { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .btn { padding: 12px 18px; border-radius: 10px; border: none; cursor: pointer; font-weight: bold; transition: 0.3s; }
        .btn-primary { background: var(--primary); color: white; }
        .btn-success { background: var(--success); color: white; }
        .btn-action { width: 35px; height: 35px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; }
        table { width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; }
        th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
        .status { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header glass-card">
        <div>
            <h1>🏥 Gestão de Insumos Pro</h1>
            <p>Conectado: fhomarcos@gmail.com</p>
        </div>
        <div style="display: flex; gap: 10px;">
            <button class="btn btn-success" onclick="exportar()"><i class="fas fa-file-excel"></i> Exportar</button>
            <button class="btn btn-primary"><i class="fas fa-plus"></i> Novo Produto</button>
        </div>
    </div>

    <div class="dashboard">
        <div class="glass-card" style="border-left: 5px solid var(--primary);">
            <small>ESTOQUE TOTAL</small>
            <h2>R$ 14.520,00</h2>
        </div>
        <div class="glass-card" style="border-left: 5px solid var(--warning);">
            <small>RISCO ASSISTENCIAL</small>
            <h2 style="color: var(--warning);">02 ITENS</h2>
        </div>
        <div class="glass-card" style="border-left: 5px solid var(--danger);">
            <small>VALIDADES (30D)</small>
            <h2 style="color: var(--danger);">05 ITENS</h2>
        </div>
    </div>

    <div class="glass-card">
        <table id="tabela">
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>SKU</th>
                    <th>Qtd</th>
                    <th>Preço</th>
                    <th>Status</th>
                    <th>Ações Rápidas</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Aerolin 100mg</strong></td>
                    <td>AE2-26</td>
                    <td id="q1">2</td>
                    <td>R$ 45,00</td>
                    <td><span class="status" style="background: #FEF3C7; color: #92400E;">Crítico</span></td>
                    <td>
                        <button class="btn-action btn-success" onclick="alt(1)">+</button>
                        <button class="btn-action" style="background: #FFEDD5; color: var(--warning);" onclick="alt(-1)">-</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        function alt(v) {
            let el = document.getElementById('q1');
            let n = parseInt(el.innerText) + v;
            if(n >= 0) el.innerText = n;
        }
        function exportar() {
            let wb = XLSX.utils.table_to_book(document.getElementById("tabela"));
            XLSX.writeFile(wb, "Inventario_Qualidade.xlsx");
        }
    </script>
</body>
</html>
"""

# Executa o HTML dentro do Streamlit
components.html(html_completo, height=1000, scrolling=True)