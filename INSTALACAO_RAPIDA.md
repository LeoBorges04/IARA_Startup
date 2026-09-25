# 🚀 Guia de Execução Rápida - IARA (Avaliação Acadêmica)

Este guia foi elaborado para permitir que o professor/avaliador execute a aplicação IARA em qualquer computador **sem a necessidade de configurar chaves de API externas (OpenAI) ou banco de dados em nuvem (MongoDB Atlas)**.

---

## ⭐️ Execução em 1 Passo (Modo Demonstração Zero-Setup)

### 1️⃣ Instalar dependências e rodar o backend
```bash
pip install -r backend_python/requirements.txt
python backend_python/main.py
```

> 🎯 **Pronto!** O sistema detectará automaticamente a ausência de variáveis de ambiente e ativará o **Modo Demonstração Local**:
> - **Banco de Dados In-Memory:** Cria e alimenta automaticamente contas de teste (`aluno@iara.com`, `professor@iara.com`, `adm@iara.com` | senha: `iara123`) e turmas didáticas.
> - **Motor Socrático RAG Local:** Responde a perguntas conceituais e análises de código usando a base de conhecimento local acervada em Markdown (`backend_python/data/`).

### 2️⃣ Acessar a Interface Web
Abra a página `index.html` ou `login.html` no seu navegador favorito (ou acesse `http://localhost:3000/`).

---

## 🗝️ Credenciais de Teste Pré-cadastradas

Ao rodar sem arquivo `.env`, utilize as seguintes contas para testar os diferentes perfis do sistema:

| Perfil | E-mail | Senha | Acesso / Permissões |
| :--- | :--- | :--- | :--- |
| **Aluno** | `aluno@iara.com` | `iara123` | Interface principal de chat, envio de código e tutoria socrática |
| **Professor** | `professor@iara.com` | `iara123` | Seleção e gestão de turmas, personalização de diretrizes RAG |
| **Administrador**| `adm@iara.com` | `iara123` | Painel administrativo (`admin.html`), upload de documentos RAG |

*(Você também pode registrar qualquer novo usuário pela tela `register.html`).*

---

## ⚙️ Execução com Credenciais Reais (Opcional)

Se desejar conectar ao MongoDB Atlas e utilizar a API da OpenAI real, basta criar um arquivo `.env` na raiz do projeto contendo:

```env
MONGODB_URI=mongodb+srv://...
PORT=3000
API_KEY=sk-sua_chave_openai_aqui
```

---

## 📋 Pré-requisitos Mínimos
- Python 3.10+
- Navegador moderno (Google Chrome, Firefox, Edge, Safari)

