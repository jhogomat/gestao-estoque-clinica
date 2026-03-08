from flask import Flask, render_template_string, request, jsonify
from tinydb import TinyDB, Query
from datetime import datetime
import os

app = Flask(__name__)

# Banco de dados local (arquivo JSON)
db = TinyDB('estoque_db.json')
tbl_prods = db.table('produtos')
tbl_movs = db.table('movimentacoes')
tbl_cats = db.table('categorias')

# --- TEMPLATE HTML (Jinja2 + Tailwind) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>MGM Consultoria - BioConect Stock (Python Version)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800">
    <header class="bg-white border-b p-4 sticky top-0 z-50 shadow-sm">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <div class="flex items-center gap-2">
                <i data-lucide="shield-check" class="text-blue-600"></i>
                <h1 class="text-xl font-bold italic">BioConect <span class="text-blue-600 underline">Python</span></h1>
            </div>
            <span class="text-xs bg-slate-200 px-2 py-1 rounded">Servidor Ativo: Localhost:5000</span>
        </div>
    </header>

    <div class="max-w-7xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
        <aside class="space-y-2">
            <button onclick="showTab('tab-dash')" class="w-full text-left p-3 hover:bg-white rounded-lg flex items-center gap-2"><i data-lucide="layout-dashboard"></i> Gestão de Riscos</button>
            <button onclick="showTab('tab-prod')" class="w-full text-left p-3 hover:bg-white rounded-lg flex items-center gap-2"><i data-lucide="package"></i> Cadastro Produto</button>
            <button onclick="showTab('tab-estoque')" class="w-full text-left p-3 hover:bg-white rounded-lg flex items-center gap-2"><i data-lucide="database"></i> Estoque Real</button>
        </aside>

        <main class="lg:col-span-3">
            <div id="tab-dash" class="tab-content active">
                <h2 class="text-2xl font-bold mb-4">Dashboard de Riscos Assistenciais</h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="dash-stats">
                    </div>
            </div>

            <div id="tab-prod" class="tab-content bg-white p-6 rounded-xl border">
                <h2 class="text-xl font-bold mb-4">Novo Produto</h2>
                <form id="form-produto" class="grid grid-cols-2 gap-4">
                    <input type="text" name="id" placeholder="ID (ex: 1001)" class="border p-2 rounded" required>
                    <input type="text" name="nome" placeholder="Nome do Item" class="border p-2 rounded" required>
                    <input type="number" name="minimo" placeholder="Estoque Mínimo" class="border p-2 rounded" required>
                    <button type="submit" class="bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Salvar no Python DB</button>
                </form>
            </div>

            <div id="tab-estoque" class="tab-content bg-white p-6 rounded-xl border">
                <h2 class="text-xl font-bold mb-4">Tabela de Inventário</h2>
                <table class="w-full border-collapse">
                    <thead><tr class="bg-slate-100 text-left"><th class="p-2 border">ID</th><th class="p-2 border">Nome</th><th class="p-2 border">Saldo</th></tr></thead>
                    <tbody id="lista-estoque"></tbody>
                </table>
            </div>
        </main>
    </div>

    <script>
        function showTab(id) {
            document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            if(id === 'tab-estoque') carregarEstoque();
            if(id === 'tab-dash') carregarDash();
        }

        // Chamada API para Salvar Produto
        document.getElementById('form-produto').onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.from_ those(formData.entries());
            
            const response = await fetch('/api/produto', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            const res = await response.json();
            alert(res.msg);
            e.target.reset();
        };

        async function carregarEstoque() {
            const res = await fetch('/api/estoque');
            const dados = await res.json();
            const body = document.getElementById('lista-estoque');
            body.innerHTML = dados.map(p => `
                <tr class="border-b">
                    <td class="p-2 border">${p.id}</td>
                    <td class="p-2 border">${p.nome}</td>
                    <td class="p-2 border font-bold ${p.saldo <= p.minimo ? 'text-red-500' : ''}">${p.saldo}</td>
                </tr>
            `).join('');
        }

        async function carregarDash() {
            const res = await fetch('/api/estoque');
            const dados = await res.json();
            const abaixo = dados.filter(p => p.saldo <= p.minimo).length;
            
            document.getElementById('dash-stats').innerHTML = `
                <div class="bg-white p-6 border rounded-xl shadow-sm">
                    <p class="text-sm text-slate-500">Total de Itens</p>
                    <p class="text-3xl font-bold">${dados.length}</p>
                </div>
                <div class="bg-red-50 p-6 border border-red-100 rounded-xl shadow-sm">
                    <p class="text-sm text-red-600 font-bold">Risco de Ruptura (Min)</p>
                    <p class="text-3xl font-bold text-red-700">${abaixo}</p>
                </div>
            `;
        }

        window.onload = () => { lucide.createIcons(); carregarDash(); };
    </script>
</body>
</html>
"""

# --- ROTAS DA API ---

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/produto', methods=['POST'])
def add_produto():
    data = request.json
    # Verifica se já existe
    if tbl_prods.search(Query().id == data['id']):
        return jsonify({"msg": "Erro: ID já existe no banco Python!"}), 400
    
    tbl_prods.insert(data)
    # Simula entrada inicial de 0
    return jsonify({"msg": "Produto salvo com sucesso no TinyDB!"})

@app.route('/api/estoque', methods=['GET'])
def get_estoque():
    todos_prods = tbl_prods.all()
    # Aqui poderíamos calcular as movimentações reais no Python
    # Para este exemplo rápido, retornamos o cadastro com um saldo fixo fictício
    for p in todos_prods:
        p['saldo'] = 5  # No sistema real, faríamos o cálculo das tabelas de Entrada/Saída
    return jsonify(todos_prods)

if __name__ == '__main__':
    # Rodar em modo debug para desenvolvimento
    app.run(debug=True, port=5000)