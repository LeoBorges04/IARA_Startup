# 🚀 Guia de Instalação Rápida - IARA

Resumo rápido para clonar e rodar o projeto em uma nova máquina.

## ⚡ Instalação em 5 Minutos

### 1️⃣ Clonar o Repositório
```bash
git clone https://github.com/leoborges04/IARA_Startup.git
cd IARA_Startup/backend
```

### 2️⃣ Instalar Dependências
```bash
npm install
```

### 3️⃣ Configurar Credenciais (.env)
Crie um arquivo `.env` na pasta `backend/` com o seguinte conteúdo:

```env
MONGODB_URI=mongodb+srv://IARA:iara123@iara.lrfvsnr.mongodb.net/?appName=IARA
PORT=3000
API_KEY=sua_chave_openai_aqui
```

**Onde obter:**
- **MONGODB_URI**: Já está configurado (mesma conta fornecida)
- **API_KEY**: [OpenAI API Keys](https://platform.openai.com/account/api-keys)

### 4️⃣ Rodar o Servidor
```bash
npm start
```

✅ **Pronto!** Se ver as mensagens abaixo, tudo está funcionando:
```
MongoDB: Conexão bem sucedida ao Atlas!
Servidor rodando na porta 3000
```

---

## 🌐 Acessar o Frontend

1. **Opção 1 - Online** (sem rodal backend local):
   - [https://leoborges04.github.io/IARA_Startup/](https://leoborges04.github.io/IARA_Startup/)

2. **Opção 2 - Local** (com backend rodando):
   - Abra `index.html` no navegador
   - O servidor backend estará disponível em `http://localhost:3000`

---

## 📋 Pré-requisitos Verificar

- [ ] Node.js instalado? → `node --version`
- [ ] npm funciona? → `npm --version`
- [ ] Git instalado? → `git --version`
- [ ] Arquivo `.env` criado na pasta `backend/`?
- [ ] Chave OpenAI configurada no `.env`?
- [ ] Conexão de internet funciona?

---

## 🆘 Problemas?

| Erro | Solução |
|------|---------|
| `npm: command not found` | Instale [Node.js](https://nodejs.org/) |
| `MongoDB connection error` | Verifique `.env` e conexão com a internet |
| `Port 3000 already in use` | Mude `PORT=3001` no `.env` |
| `API_KEY invalid` | Verifique a chave OpenAI em `.env` |

Para mais detalhes, consulte a seção **Troubleshooting** no [README.md](README.md).

---

## 📚 Próximos Passos

1. Registre uma conta no frontend
2. Faça login
3. Comece a usar o chat com IA
4. (Opcional) Acesse `/admin.html` com conta de admin

---

**Última atualização**: Abril 2026  
**Desenvolvedor**: Léo Borges
