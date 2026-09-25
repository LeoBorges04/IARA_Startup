# IARA — Inteligência Artificial de Raciocínio Algorítmico 🧠

O projeto **IARA** é uma plataforma educacional web interativa desenvolvida para apoiar estudantes universitários no aprendizado e desenvolvimento de seu raciocínio algorítmico, lógica de programação e estruturas de dados.

---

## 📄 Documentação do Trabalho de Interface Web

Para visualizar o documento detalhado relativo aos **Princípios de Design, Usabilidade, Experiência do Usuário (UX) e Acessibilidade (WCAG)** exigidos para a entrega do Trabalho 1, acesse:

📄 **[Documento Explicativo da Interface (DOCUMENTO_EXPLICATIVO_IARA.md)](file:///home/Leo_Borges/IARAFRONT/DOCUMENTO_EXPLICATIVO_IARA.md)**

---

## ⚡ Execução Rápida Sem Credenciais (Avaliação Acadêmica)

A aplicação foi projetada com um **Modo Demonstração Zero-Setup** para permitir a execução no computador do professor sem a necessidade de chaves da API OpenAI ou banco de dados MongoDB Atlas.

### 1️⃣ Executar o backend
```bash
pip install -r backend_python/requirements.txt
python backend_python/main.py
```

O backend inicializará automaticamente o banco de dados em memória (*In-Memory Store*) e o motor de respostas socráticas sintonizado com os materiais didáticos locais RAG.

### 2️⃣ Acessar a aplicação
Abra `index.html` ou `login.html` no seu navegador favorito.

### 🗝️ Contas de Teste Pré-cadastradas
* **Aluno:** `aluno@iara.com` / Senha: `iara123`
* **Professor:** `professor@iara.com` / Senha: `iara123`
* **Administrador:** `adm@iara.com` / Senha: `iara123`

---

## 📁 Estrutura do Projeto

```
IARA_Startup/
├── backend_python/             # Servidor Python (FastAPI + RAG + Fallback Local)
│   ├── data/                   # Bases de conhecimento RAG em Markdown (conceitos e exercícios)
│   ├── routes/                 # Rotas da API (auth, chats, classes, admin)
│   ├── services/               # RAG service, auth e guardrails de código
│   ├── database.py             # Gerenciador de banco de dados (MongoDB Atlas / In-Memory Mock)
│   └── main.py                 # Ponto de entrada do FastAPI
├── index.html                  # Interface Principal do Chat UI
├── login.html                  # Tela de Autenticação
├── register.html               # Tela de Cadastro
├── selecionar_turma.html       # Painel de Seleção de Turmas
├── admin.html                  # Painel Administrativo RAG
├── style.css                   # Sistema Visual em Vanilla CSS
├── script.js                   # Lógica de Interação Frontend em JS
├── DOCUMENTO_EXPLICATIVO_IARA.md # Documento explicativo de UI/UX/A11y (Trabalho 1)
└── INSTALACAO_RAPIDA.md        # Guia de execução rápida
```
