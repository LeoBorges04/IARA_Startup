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

Siga o passo a passo abaixo para rodar o backend da IARA na sua própria máquina local.

**1.** Abra o seu terminal e navegue até a pasta do backend:
```bash
cd backend/
```

**2.** Instale as dependências necessárias do Node.js:
```bash
npm install
```

**3.** Configure as Suas Variáveis de Ambiente:
Renomeie ou crie uma cópia do arquivo `.env.example` chamando-a apenas de `.env`. Em seguida, preencha os valores reais lá dentro:
```env
MONGODB_URI=mongodb+srv://IARA:<iara123>@iara.lrfvsnr.mongodb.net/?appName=IARA
API_KEY=CHAVE_DA_SUA_API_OPENAI
```

**4.** Inicie a API e deixe-a rodando:
```bash
npm start
```
Se tudo der certo, você deverá visualizar no seu terminal as mensagens:
`Servidor rodando na porta 3000`
`MongoDB: Conexão bem sucedida ao Atlas!`

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
