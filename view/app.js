// =============== Helpers ===============
const $ = (s) => document.querySelector(s);
const api = async (url, opts = {}) => {
  const r = await fetch(url, opts);
  if (r.status === 204) return null;
  let d = null; try { d = await r.json(); } catch {}
  if (!r.ok) throw new Error(d?.detail || 'Erro');
  return d;
};

// caches globais
let produtos = [];
let carrinhos = [];
let pickerCarrinhoId = null; // carrinho ativo no modal

// =============== Admin ===============
$('#btnAdmin').onclick = async () => {
  const body = {
    nome: $('input[name="a_nome"]').value,
    username: $('input[name="a_user"]').value,
    senha: $('input[name="a_pass"]').value
  };
  await api('/administradores', {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)
  });
  $('#loginStatus').textContent = 'Administrador criado.';
  ['a_nome','a_user','a_pass'].forEach(n => $('input[name="'+n+'"]').value = '');
};

// =============== Clientes ===============
$('#btnCliente').onclick = async () => {
  const body = {
    nomeCliente: $('input[name="c_nome"]').value,
    email: $('input[name="c_email"]').value,
    endereco: $('input[name="c_end"]').value
  };
  await api('/clientes', {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)
  });
  ['c_nome','c_email','c_end'].forEach(n => $('input[name="'+n+'"]').value = '');
  loadClientes();
};

// Criar carrinho -> abre modal (picker) com produtos disponíveis
$('#btnCarrinho').onclick = async () => {
  const cid = parseInt($('input[name="cid"]').value || '0', 10);
  if (!cid) return alert('Informe um Cliente ID válido.');
  const carrinho = await api(`/carrinhos?cliente_id=${cid}`, { method:'POST' });
  $('input[name="cid"]').value = '';
  await Promise.all([loadCarrinhos(), loadClientes(), loadProdutos()]);
  openPicker(carrinho.id);
};

async function loadClientes() {
  const dados = await api('/clientes');
  const box = $('#clientes'); box.innerHTML = '';
  dados.forEach(c => {
    const el = document.createElement('div'); el.className = 'item';
    el.innerHTML = `
      <div><b>${c.nomeCliente}</b> — ${c.email}
        <div class="small">id: ${c.id} | carrinho: ${c.carrinho_id ?? '-'}</div>
      </div>
      <button class="ghost" data-del="${c.id}">Excluir</button>
    `;
    box.appendChild(el);
  });
  box.querySelectorAll('[data-del]').forEach(b => b.onclick = async () => {
    await api(`/clientes/${b.dataset.del}`, { method:'DELETE' });
    loadClientes();
  });
}

// =============== Produtos (cards) ===============
$('#btnProduto').onclick = async () => {
  const body = {
    nome: $('input[name="p_nome"]').value,
    descricao: $('input[name="p_desc"]').value,
    preco: parseFloat($('input[name="p_preco"]').value || '0'),
    estoque: parseInt($('input[name="p_estoque"]').value || '0', 10)
  };
  await api('/produtos', {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)
  });
  ['p_nome','p_desc','p_preco','p_estoque'].forEach(n => $('input[name="'+n+'"]').value = '');
  loadProdutos();
};

async function loadProdutos() {
  produtos = await api('/produtos') || [];
  const grid = $('#grid-produtos'); grid.innerHTML = '';
  produtos.forEach(p => {
    const card = document.createElement('div'); card.className = 'card';
    card.innerHTML = `
      <div class="card-head">
        <h3 class="card-title">${p.nome}</h3>
        <span class="badge">#${p.id}</span>
      </div>
      <p class="small">${p.descricao || '—'}</p>
      <div class="row" style="justify-content:space-between;margin-top:8px">
        <span class="price">R$ ${(p.preco || 0).toFixed(2)}</span>
        <span class="small">estoque: ${p.estoque}</span>
      </div>
      <div class="row right" style="margin-top:10px">
        <button class="ghost" data-up="${p.id}">+1 estoque</button>
        <button class="ghost" data-del="${p.id}">Excluir</button>
      </div>
    `;
    grid.appendChild(card);
  });

  // ações dos cards
  grid.querySelectorAll('[data-del]').forEach(b => b.onclick = async () => {
    await api(`/produtos/${b.dataset.del}`, { method:'DELETE' });
    loadProdutos();
  });

  grid.querySelectorAll('[data-up]').forEach(b => b.onclick = async () => {
    const id = b.dataset.up; const cur = await api(`/produtos/${id}`);
    await api(`/produtos/${id}`, {
      method: 'PATCH', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ estoque: (cur.estoque || 0) + 1 })
    });
    loadProdutos();
  });
}

// =============== Carrinhos (lista) ===============
async function loadCarrinhos() {
  carrinhos = await api('/carrinhos') || [];
  const box = $('#carrinhos'); box.innerHTML = '';
  carrinhos.forEach(c => {
    const itens = c.itens.map(i => `#${i.numProduto} x${i.quantidade}`).join(', ') || 'vazio';
    const el = document.createElement('div'); el.className = 'item';
    el.innerHTML = `
      <div><b>Carrinho ${c.numCarrinho}</b> — cliente ${c.cliente_id}
        <div class="small">itens: ${itens}</div>
      </div>
      <button class="ghost" data-del="${c.id}">Excluir</button>
    `;
    box.appendChild(el);
  });
  box.querySelectorAll('[data-del]').forEach(b => b.onclick = async () => {
    await api(`/carrinhos/${b.dataset.del}`, { method:'DELETE' });
    loadCarrinhos();
  });
}

// ================= Modal (Picker) =================
function openPicker(carrinhoId){
    pickerCarrinhoId = carrinhoId;
    $('#picker-title').textContent = `Produtos disponíveis — Carrinho ${carrinhoId}`;
    renderPickerList();                     // 🔹 monta a lista ao abrir
    $('#picker').classList.add('show');     // 🔹 mostra o modal
    document.body.classList.add('modal-open');
  }
  
  function closePicker(){
    $('#picker').classList.remove('show');
    document.body.classList.remove('modal-open');
    pickerCarrinhoId = null;
  }
  
  // 🔸 Eventos dos botões de fechar e concluir
  $('#picker-close')?.addEventListener('click', closePicker);
  $('#picker-done')?.addEventListener('click', closePicker);
  
  // 🔹 AGORA SIM — Monta a grade de produtos com estoque > 0
  function renderPickerList(){
    const box = $('#picker-list'); box.innerHTML = '';
    const disponiveis = (produtos || []).filter(p => (p.estoque||0) > 0);
  
    if (!disponiveis.length) {
      const empty = document.createElement('div');
      empty.className = 'item';
      empty.innerHTML = `<div class="small">Não há produtos disponíveis (estoque 0).</div>`;
      box.appendChild(empty);
      return;
    }
  
    disponiveis.forEach(p=>{
      const el = document.createElement('div');
      el.className = 'card';
      el.innerHTML = `
        <div class="title">${p.nome} <span class="meta">#${p.id}</span></div>
        <div class="meta">${p.descricao || '—'}</div>
        <div class="row">
          <span><b>R$ ${(p.preco||0).toFixed(2)}</b></span>
          <span class="meta">estoque: ${p.estoque}</span>
        </div>
        <div class="row">
          <input type="number" class="qty" min="1" value="1" data-qtd="${p.id}">
          <button data-add="${p.id}">Adicionar</button>
        </div>
      `;
      box.appendChild(el);
    });
  
    // Ações dos botões "Adicionar"
    box.querySelectorAll('[data-add]').forEach(btn=>{
      btn.onclick = async ()=>{
        const pid = parseInt(btn.dataset.add, 10);
        const qtd = parseInt(box.querySelector(`input[data-qtd="${pid}"]`)?.value || '1', 10);
        if (!pickerCarrinhoId) return alert('Carrinho não encontrado.');
        if (qtd <= 0) return alert('Quantidade inválida.');
  
        await api(`/carrinhos/${pickerCarrinhoId}/adicionar`, {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ numProduto: pid, quantidade: qtd })
        });
  
        await Promise.all([loadProdutos(), loadCarrinhos()]);
        renderPickerList(); // 🔁 Atualiza estoque sem fechar o modal
      };
    });
  }
  

// =============== Checkout / Pedidos ===============
$('#btnCheckout').onclick = async () => {
  const carId = parseInt($('input[name="car_id"]').value || '0', 10);
  if (!carId) return alert('Informe um carrinho.');

  const envio = {
    destinatario: $('input[name="dest"]').value,
    endereco: $('input[name="end"]').value,
    cep: $('input[name="cep"]').value,
    metodo: $('select[name="met"]').value,
    custo: parseFloat($('input[name="frete"]').value || '0'),
    prazoDias: parseInt($('input[name="prazo"]').value || '5', 10)
  };

  const p = await api(`/pedidos/checkout/${carId}`, {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(envio)
  });

  ['car_id','dest','end','cep','frete','prazo'].forEach(n => $('input[name="'+n+'"]').value = '');
  renderPedido(p);
  loadCarrinhos();
};

function renderPedido(p){
  const box = $('#pedidosBox');
  const wrap = document.createElement('div'); wrap.className = 'card'; wrap.style.padding = '16px';
  const rows = p.itens.map(i => `
    <tr>
      <td>${i.numProduto}</td><td>${i.nomeProduto}</td>
      <td>${i.quantidade}</td><td>R$ ${i.precoUnit.toFixed(2)}</td>
      <td>R$ ${i.subtotal.toFixed(2)}</td>
    </tr>`).join('');
  wrap.innerHTML = `
    <div class="card-head">
      <div><b>Pedido #${p.id}</b> — cliente ${p.cliente_id}</div>
      <span class="badge">${p.estado}</span>
    </div>
    <table class="table">
      <thead><tr><th>ID</th><th>Produto</th><th>Qtd</th><th>Preço</th><th>Subtotal</th></tr></thead>
      <tbody>${rows}</tbody>
    </table>
    <div class="total">
      <span>Produtos: R$ ${p.totalProdutos.toFixed(2)}</span>
      <span>Frete: R$ ${p.frete.toFixed(2)}</span>
      <span>Total: R$ ${p.totalGeral.toFixed(2)}</span>
    </div>
    <div class="small">Envio: ${p.envio.metodo} — ${p.envio.destinatario}, ${p.envio.endereco} (${p.envio.cep}) • ${p.envio.prazoDias} dias</div>
  `;
  box.prepend(wrap);
}

// =============== Boot ===============
(async () => {
  await Promise.all([loadProdutos(), loadClientes(), loadCarrinhos()]);
})();
