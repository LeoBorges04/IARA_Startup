# IARA - Inteligência Artificial de Raciocínio Algorítmico 🧠

O projeto **IARA** é uma plataforma que atua como uma tutora virtual com auxílio de Inteligência Artificial para apoiar o aluno no desenvolvimento de seu raciocínio algorítmico em nível universitário.

A arquitetura do projeto é dividida em:
- **Frontend:** Estático e simples construído com HTML, CSS e Vanilla JS moderno para entregar uma experiência UI/UX fluida com animações suaves e layouts imersivos.
- **Backend:** Uma API de alta performance construída em **Python (FastAPI)** conectada ao banco de dados **MongoDB Atlas** e equipada com sistema **RAG (Retrieval-Augmented Generation)**, responsável pela segurança, gestão de históricos, contas de usuários e mediação com a **OpenAI**.

---

## 🚀 Como acessar a aplicação

O frontend público desta aplicação está hospedado no GitHub Pages. Para acessar o site, você pode simplesmente clicar no link abaixo:

🔗 **[Acessar a Plataforma IARA (GitHub Pages)](https://leoborges04.github.io/IARA_Startup/)**

*(O site exige que a API do backend Python esteja sendo executada para funcionar corretamente nas funcionalidades de chat, autenticação e RAG).*

---

## ⚙️ Como rodar o servidor (Backend Python) localmente

### Pré-requisitos
- **Python** versão 3.10 ou superior
- Acesso à internet para conexão com MongoDB Atlas e OpenAI API

---

## 📡 Documentação das Rotas (API Docs)

A API do backend opera na porta `3000` (ou configurada via `PORT`).

### 🔐 Autenticação (`/api/auth`)
* `POST /api/auth/register`: Registra um novo usuário.
* `POST /api/auth/login`: Valida as credenciais do usuário.

### 💬 Conversas e Chat (`/api/chats`)
* `GET /api/chats/:userId`: Retorna a lista de conversas do usuário.
* `POST /api/chats`: Cria uma nova conversa.
* `DELETE /api/chats/:id`: Deleta uma conversa.
* `PUT /api/chats/:id/rename`: Edita o título de uma conversa.
* `POST /api/chats/:id/message`: Processa a mensagem do usuário via RAG e OpenAI.

---

## 📝 Estrutura de Pastas

```
IARA_Startup/
├── backend_python/             # Servidor Python (FastAPI + RAG)
│   ├── data/                   # Bases de conhecimento e exercícios RAG
│   ├── routes/                 # Rotas da API (auth, chats, admin)
│   ├── services/               # Serviços RAG e integração OpenAI
│   ├── config.py               # Configurações de ambiente
│   ├── database.py             # Conexão MongoDB Atlas
│   └── main.py                 # Aplicação FastAPI (Ponto de entrada)
├── index.html                  # Interface Web Principal
├── login.html                  # Tela de Login
├── register.html               # Tela de Cadastro
├── admin.html                  # Painel Administrativo
├── script.js                   # Lógica Frontend em JS
└── README.md                   # Este arquivo
```
