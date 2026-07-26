# 🚀 Guia de Instalação Rápida - IARA (Backend Python)

Resumo rápido para clonar e rodar o projeto em uma nova máquina.

## ⚡ Instalação em 5 Minutos

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/leoborges04/IARA_Startup.git
cd IARA_Startup
```

### 2️⃣ Criar Ambiente Virtual e Instalar Dependências
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r backend_python/requirements.txt
```

### 3️⃣ Configurar Credenciais (.env)
Crie um arquivo `.env` na raiz ou na pasta `backend_python/` com o seguinte conteúdo:

```env
MONGODB_URI=mongodb+srv://IARA:iara123@iara.lrfvsnr.mongodb.net/?appName=IARA
PORT=3000
API_KEY=sua_chave_openai_aqui
```

### 4️⃣ Rodar o Servidor Backend Python
```bash
python backend_python/main.py
```

✅ **Pronto!** Se ver as mensagens abaixo, tudo está funcionando:
```
Iniciando backend Python RAG da IARA...
Servidor rodando em http://0.0.0.0:3000
```

---

## 🌐 Acessar o Frontend

Abra o arquivo `index.html` no navegador (com o backend Python rodando na porta 3000).

---

## 📋 Pré-requisitos
- Python 3.10+
- Chave de API da OpenAI (`API_KEY`)
- Conexão de internet para o MongoDB Atlas
