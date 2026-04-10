# IARA - Inteligência Artificial de Raciocínio Algorítmico 🧠

O projeto **IARA** é uma plataforma que atua como uma tutora virtual com auxílio de Inteligência Artificial para apoiar o aluno no desenvolvimento de seu raciocínio algorítmico em nível universitário.

A arquitetura do projeto é dividida em:
- **Frontend:** Estático e simples construído com HTML, CSS e Vanilla JS moderno para entregar uma experiência UI/UX fluida com animações suaves e layouts imersivos.
- **Backend:** Uma API construída em **Node.js (+ Express)** conectada ao banco de dados **MongoDB Atlas**, responsável pela segurança, gestão dos históricos de chats, contas de usuários e, principalmente, por atuar como uma ponte de comunicação com a **OpenAI**.

---

## 🚀 Como acessar a aplicação

O frontend público desta aplicação está hospedado no GitHub Pages. Para acessar o site, você pode simplesmente clicar no link abaixo:

🔗 **[Acessar a Plataforma IARA (GitHub Pages)](https://leoborges04.github.io/IARA_Startup/)**

*(O site exige que a a API do backend esteja sendo executada para funcionar corretamente nas funcionalidades de chat e login).*

---

## ⚙️ Como rodar o servidor (Backend) localmente

### Pré-requisitos
- **Node.js** versão 14 ou superior ([Download aqui](https://nodejs.org/))
- **Git** instalado no sistema
- Acesso à internet para conexão com MongoDB Atlas e OpenAI API
- Credenciais válidas do MongoDB Atlas e chave da API OpenAI

### Passo a Passo de Instalação

#### **Passo 1: Clonar o Repositório**
```bash
git clone https://github.com/leoborges04/IARA_Startup.git
cd IARA_Startup
```

#### **Passo 2: Navegar até a Pasta do Backend**
```bash
cd backend
```

#### **Passo 3: Instalar as Dependências do Node.js**
```bash
npm install
```
Este comando irá instalar todas as dependências listadas no `package.json` (Express, Mongoose, bcryptjs, CORS, etc).

#### **Passo 4: Configurar as Variáveis de Ambiente**
1. Na pasta `backend/`, localize o arquivo `.env.example` (se não existir, veja a seção de Troubleshooting)
2. Crie um novo arquivo chamado `.env` na mesma pasta `backend/`
3. Copie o conteúdo do `.env.example` e preencha com suas credenciais reais:

```env
MONGODB_URI=mongodb+srv://IARA:iara123@iara.lrfvsnr.mongodb.net/?appName=IARA
PORT=3000
API_KEY=sua_chave_api_openai_aqui
```

**Campos necessários:**
- **MONGODB_URI**: Sua string de conexão do MongoDB Atlas (já está configurada)
- **PORT**: Porta onde o servidor irá rodar (padrão: 3000)
- **API_KEY**: Sua chave de API da OpenAI (obtenha em https://platform.openai.com/account/api-keys)

#### **Passo 5: Verificar Conectividade com o MongoDB Atlas**
Antes de rodar o server, verifique se consegue acessar o Atlas:
```bash
npm start
```

#### **Passo 6: Iniciar o Servidor**
```bash
npm start
```

**Se tudo der certo, você verá:**
```
[dotenv@17.3.1] injecting env (3) from .env
MongoDB: Conexão bem sucedida ao Atlas!
Servidor rodando na porta 3000
```

⚠️ **Nota sobre DNS**: Este projeto foi configurado para usar DNS público (Google 8.8.8.8 e Cloudflare 1.1.1.1) para resolver corretamente o MongoDB Atlas SRV. Isso já está implementado automaticamente no `server.js`.
API_KEY=CHAVE_DA_SUA_API_OPENAI
```

**4.** Inicie a API e deixe-a rodando:
```bash
npm start
```
Se tudo der certo, você deverá visualizar no seu terminal as mensagens:
`Servidor rodando na porta 3000`
`MongoDB: Conexão bem sucedida ao Atlas!`
>>>>>>> f900beb2a3808988d03983fbb410c829c6de7e1d

---

## 📡 Documentação das Rotas (API Docs)

A API do backend opera na rota `/api/...` sendo as principais chamadas as descritas abaixo:

### 🔐 Autenticação (`/api/auth`)
* `POST /api/auth/register`: Registra um novo usuário. Requer payload com e-mail e outras credenciais.
* `POST /api/auth/login`: Valida as informações de um usuário e permite o acesso ao sistema.

### 💬 Conversas e Chat (`/api/chats`)
* `GET /api/chats/:userId`: Retorna a lista completa de todas as conversas do usuário ordenadas pela data da última atividade.
* `POST /api/chats`: Cria e inicializa uma nova conversa em branco para o usuário.
* `DELETE /api/chats/:id`: Deleta permanentemente uma conversa através de seu ID único (`_id`).
* `PUT /api/chats/:id/rename`: Edita apenas o título de exibição de uma conversa.

### 🤖 Integração Inteligência Artificial
* `POST /api/chats/:id/message`: É a principal rota do sistema base! Ela recebe a sua nova mensagem em tempo real, consulta o histórico da conversa no banco MongoDB, envia a requisição segura internamente processada usando a `API_KEY` para a API da **OpenAI** (através do modelo selecionado), injeta a resposta no banco de dados para salvar de vez seu histórico, e devolve somente a resposta final textual da IARA para ser renderizada na sua tela com animação de máquina de escrever!
<<<<<<< HEAD

---

## 🆘 Troubleshooting - Problemas Comuns

### ❌ Erro: `Error: querySrv ECONNREFUSED _mongodb._tcp`
**Causa**: Problema de resolução DNS do MongoDB Atlas SRV.

**Solução**: Este projeto já está configurado para usar DNS público automaticamente. Se o erro persistir:
1. Reinicie seu terminal
2. Verifique sua conexão de internet
3. Tente alterar seus servidores DNS do Windows para 8.8.8.8 (Google) ou 1.1.1.1 (Cloudflare)

### ❌ Erro: `ENOENT: no such file or directory, open '.env'`
**Causa**: Arquivo `.env` não existe na pasta `backend/`.

**Solução**:
1. Crie um arquivo novo chamado `.env` dentro da pasta `backend/`
2. Copie o conteúdo do `.env.example` e preencha as credenciais

### ❌ Erro: `npm: command not found`
**Causa**: Node.js não está instalado ou não está no PATH.

**Solução**:
1. [Baixe e instale Node.js](https://nodejs.org/) (versão LTS recomendada)
2. Reinicie seu terminal/computador
3. Verifique a instalação: `node --version`

### ❌ Erro: `MongoDB: Conexão bem sucedida, mas depois não conecta`
**Causa**: Banco de dados Atlas talvez não tenha sua IP na whitelist, ou credenciais incorretas.

**Solução**:
1. Acesse [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Vá para **Network Access** 
3. Adicione seu IP à whitelist (ou use `0.0.0.0/0` para aceitar todas - apenas para desenvolvimento!)

### ❌ Erro: `API_KEY inválida da OpenAI`
**Causa**: Chave de API expirada, inválida ou com permissões insuficientes.

**Solução**:
1. Acesse [OpenAI API Keys](https://platform.openai.com/account/api-keys)
2. Crie uma nova chave ou copie uma existente
3. Atualize o arquivo `.env` com a nova chave
4. Reinicie o servidor com `npm start`

### ❌ Erro: `Port 3000 already in use`
**Causa**: Outra aplicação está usando a porta 3000.

**Solução**: 
1. Opção A: Mude a porta no `.env` (ex: `PORT=3001`)
2. Opção B: Feche a aplicação que está usando a porta 3000

---

## 📝 Estrutura de Pastas

```
IARA_Startup/
├── backend/                    # Servidor Node.js + Express
│   ├── models/                 # Modelos Mongoose (User, Chat)
│   ├── routes/                 # Rotas da API (auth, chats, admin)
│   ├── server.js               # Arquivo principal do servidor
│   ├── .env                    # Variáveis de ambiente (NÃO COMMIT)
│   ├── .env.example            # Exemplo de variáveis de ambiente
│   └── package.json            # Dependências Node.js
├── index.html                  # Página principal (Frontend)
├── login.html                  # Página de login
├── register.html               # Página de registro
├── admin.html                  # Painel administrativo
├── script.js                   # JavaScript principal (Frontend)
├── style.css                   # Estilos CSS (Frontend)
└── README.md                   # Este arquivo
```

---

## 🔐 Segurança

⚠️ **IMPORTANTE**: Nunca faça commit do arquivo `.env` ou qualquer arquivo contendo credenciais reais no Git!

O arquivo `.env` está no `.gitignore` para proteção. Use apenas o `.env.example` como template.
=======
>>>>>>> f900beb2a3808988d03983fbb410c829c6de7e1d
