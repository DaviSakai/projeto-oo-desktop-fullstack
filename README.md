# 🏪 Loja MVC — CRUD + Checkout (FastAPI + HTML/CSS/JS)

Este projeto foi desenvolvido para a disciplina de **Programação Orientada a Objetos**, com o objetivo de demonstrar uma aplicação **desktop fullstack** estruturada no padrão **MVC (Model / View / Controller)**.

---

## 🎯 Objetivo
O sistema simula uma **loja virtual simplificada**, permitindo:
- Cadastro e login de **administradores**  
- Cadastro de **clientes**  
- Criação e gerenciamento de **produtos**  
- Criação de **carrinhos de compra** com produtos disponíveis  
- Processo de **checkout**, incluindo cálculo de frete e resumo do pedido  

Tudo isso com uma interface web estática integrada ao backend **FastAPI**.

---

## 🧱 Estrutura do Projeto


---

## ⚙️ Tecnologias Utilizadas
- **Python 3.11+**
- **FastAPI**
- **Uvicorn**
- **Pydantic**
- **HTML5 / CSS3 / JavaScript**
- **Arquitetura MVC**

---

## 🧩 Organização MVC

| Camada | Função | Localização |
|--------|---------|--------------|
| **Model** | Define as classes principais do domínio (`Produto`, `Cliente`, `Carrinho`, etc.) | `/model` |
| **Controller** | Contém as rotas e ações de CRUD (ex: `produto_controller.py`, `cliente_controller.py`) | `/controller` |
| **View** | Contém a interface web (HTML, CSS e JS) e faz as requisições à API | `/view` |

---

## 🖥️ Funcionalidades Principais

✅ **Administrador**  
- Criar e autenticar administradores  

✅ **Cliente**  
- Cadastrar clientes com nome, email e endereço  

✅ **Produto**  
- Cadastrar, editar e excluir produtos  
- Atualizar estoque  

✅ **Carrinho**  
- Criar carrinho vinculado a um cliente  
- Adicionar produtos disponíveis (com modal centralizado)  
- Remover itens  

✅ **Checkout**  
- Finalizar pedido com dados de envio e cálculo de frete  
- Exibir resumo do pedido (produtos, totais e prazo)

---

## 🚀 Como Executar o Projeto
```bash
### 1️⃣ Clone o repositório
```bash
git clone https://github.com/DaviSakai/projeto-oo-desktop-fullstack.git
cd projeto-oo-desktop-fullstack

### 2️⃣ Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # no Windows

###3️⃣ Instale as dependências
pip install fastapi uvicorn pydantic[email]

###4️⃣ Execute o servidor
uvicorn main:app --reload

###5️⃣ Acesse no navegador
👉 http://127.0.0.1:8000/
```
