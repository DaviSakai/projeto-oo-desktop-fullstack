# 💫 Kelaryz Desk — Loja MVC + Autenticação (FastAPI + HTML/CSS/JS)

Este projeto foi desenvolvido para a disciplina de **Programação Orientada a Objetos**, com o objetivo de demonstrar uma aplicação **desktop fullstack** estruturada no padrão **MVC (Model / View / Controller)**, integrada a um **sistema de login e persistência com banco JSON**.

---

## 🎯 Objetivo

O **Kelaryz Desk** é um sistema que simula uma **loja virtual administrativa**, permitindo o controle de clientes, produtos e pedidos.  
Além disso, conta com **autenticação completa** (cadastro, login e sessão com cookies), servindo como base para futuros **painéis empresariais desenvolvidos pela Kelaryz**.

### Funcionalidades principais:
- Cadastro e login de **usuários**
- Cadastro de **clientes**
- Criação e gerenciamento de **produtos**
- Criação de **carrinhos de compra**
- Processo de **checkout** com resumo e frete
- Interface moderna em HTML/CSS/JS comunicando com FastAPI

---

## ⚙️ Tecnologias Utilizadas

- 🐍 **Python 3.11+**
- ⚡ **FastAPI**
- 🧩 **Uvicorn**
- 🧠 **Pydantic** (com suporte a `EmailStr`)
- 💾 **Banco de Dados JSON (persistência local)**
- 🎨 **HTML5 / CSS3 / JavaScript**
- 🧱 **Arquitetura MVC**

---

## 🧩 Organização do Projeto (MVC)

| Camada | Função | Localização |
|--------|---------|-------------|
| **Domain / Model** | Define as classes do domínio (`Produto`, `Cliente`, `User`, `Pedido`, etc.) | `/domain` |
| **Infra** | Responsável pela persistência em JSON (`user_repository.py`, `json_store.py`, etc.) | `/infra` |
| **Controller** | Contém as rotas e lógicas de CRUD (ex: `produto_controller.py`, `cliente_controller.py`) | `/controller` |
| **API** | Define endpoints de autenticação (`/auth/register`, `/auth/login`, `/auth/logout`, `/auth/me`) | `/api` |
| **View** | Interface web estática (HTML, CSS, JS) | `/view` |
| **Static** | Páginas de login/cadastro (frontend integrado) | `/static` |

---

## 🔐 Funcionalidades de Autenticação

✅ **Cadastro de usuário** (`/auth/register`)  
Cria novos usuários e armazena no `data/users.json` com senha criptografada.  

✅ **Login de usuário** (`/auth/login`)  
Valida email e senha, cria cookie de sessão no navegador e salva em `data/sessions.json`.  

✅ **Logout** (`/auth/logout`)  
Remove a sessão do usuário atual.  

✅ **Rota protegida** (`/auth/me`)  
Retorna os dados do usuário logado.

---

## 🖥️ Funcionalidades Gerais

✅ **Administrador**
- Cadastrar e autenticar administradores  

✅ **Cliente**
- Cadastrar clientes com nome, email e endereço  

✅ **Produto**
- Cadastrar, editar e excluir produtos  
- Atualizar estoque  

✅ **Carrinho**
- Criar carrinho vinculado a um cliente  
- Adicionar/remover produtos  

✅ **Checkout**
- Finalizar pedido com cálculo de frete e resumo do pedido  

---

## 🗂️ Estrutura Simplificada

```bash
projeto-oo-desktop-fullstack/
│
├── api/               # Rotas de autenticação (login, registro, sessão)
├── controller/         # Controladores de CRUD (cliente, produto, etc.)
├── domain/             # Modelos (Produto, Cliente, User, Pedido...)
├── infra/              # Persistência em JSON (repositórios)
├── static/             # Páginas HTML (login, register)
├── view/               # Frontend (HTML, CSS, JS adicionais)
├── data/               # Banco de dados JSON (users.json, sessions.json)
├── main.py             # Arquivo principal (FastAPI app)
└── config.py           # Configurações de diretórios e paths
```

## 💾 Banco de Dados JSON

```bash
data/
├── users.json     → usuários registrados
└── sessions.json  → tokens de sessão ativos



---

## 🚀 Como Executar o Projeto

```bash
# 1️⃣ Clone o repositório
git clone https://github.com/DaviSakai/projeto-oo-desktop-fullstack.git
cd projeto-oo-desktop-fullstack

# 2️⃣ Crie e ative o ambiente virtual
python -m venv .venv
.venv\Scripts\activate  # no Windows

# 3️⃣ Instale as dependências
pip install fastapi uvicorn "pydantic[email]"

# 4️⃣ Execute o servidor
uvicorn main:app --reload

# 5️⃣ Acesse no navegador
http://127.0.0.1:8000/
```

## 🌐 Acesso Rápido
```bash

📄 Documentação Swagger: http://127.0.0.1:8000/docs

🔐 Tela de Login: http://127.0.0.1:8000/

🛍️ Painel Administrativo (View): http://127.0.0.1:8000/app
```