// =============================
// IARA - Frontend OpenAI Direct + Chat History via API (MongoDB)
// =============================
if (localStorage.getItem("iara_logged_in") !== "true") {
  window.location.replace("login.html");
}

// ===== CONSTANTES =====
const API_URL = "http://localhost:3000/api";
const currentUserEmail = localStorage.getItem("iara_user_email") || "admin@admin.com";
const currentUserName = localStorage.getItem("iara_user_name") || "Usuário";

// ===== ELEMENTOS DOM =====
const chatDiv = document.getElementById('chat');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('send-btn');
const chatHistoryList = document.getElementById('chat-history-list');
const newChatBtn = document.getElementById('new-chat-btn');
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const sidebar = document.getElementById('sidebar');
const appLayout = document.getElementById('app-layout');
const logoutBtn = document.getElementById("logout-btn");
const userEmailDisplay = document.getElementById("user-email-display");
const userAvatarInitial = document.getElementById("user-avatar-initial");

// Modals
const renameModal = document.getElementById('rename-modal');
const renameInput = document.getElementById('rename-input');
const renameCancelBtn = document.getElementById('rename-cancel-btn');
const renameConfirmBtn = document.getElementById('rename-confirm-btn');
const deleteModal = document.getElementById('delete-modal');
const deleteCancelBtn = document.getElementById('delete-cancel-btn');
const deleteConfirmBtn = document.getElementById('delete-confirm-btn');

// ===== SYSTEM PROMPT =====
const systemPrompt = `
Você é IARA, uma tutora virtual de programação em nível universitário.
Seu papel é apoiar o aluno no desenvolvimento do raciocínio lógico e conceitual,
promovendo autonomia intelectual e evitando a entrega de respostas prontas.

Diretrizes pedagógicas:
- Priorize explicações conceituais antes de qualquer orientação prática.
- Estimule o pensamento crítico e a construção ativa do raciocínio.
- Utilize perguntas orientadoras apenas após uma explicação conceitual inicial.
- Faça no máximo uma pergunta por interação.
- Ofereça dicas graduais.
- Evite fornecer soluções completas.
- Mantenha um tom empático e professoral.
`;

// ===== ESTADO GLOBAL DA APLICAÇÃO =====
let chats = []; 
let currentChatId = null;
let chatToRenameId = null;
let chatToDeleteId = null;

// Display user info in sidebar
userEmailDisplay.textContent = currentUserName;
userAvatarInitial.textContent = currentUserName.charAt(0).toUpperCase();

// Saudaçao personalizada no modal (RF12)
const greetingModal = document.getElementById("greeting-modal");
const greetingMessageElement = document.getElementById("greeting-message");
const greetingCloseBtn = document.getElementById("greeting-close-btn");

if (greetingModal && greetingMessageElement && greetingCloseBtn) {
    greetingMessageElement.textContent = `Olá, ${currentUserName.split(' ')[0]}! Bem-vindo(a) ao IARA. Como posso te auxiliar hoje?`;
    greetingModal.style.display = "flex";

    let timeoutId = setTimeout(() => {
        greetingModal.style.display = "none";
    }, 5000);

    greetingCloseBtn.addEventListener("click", () => {
        clearTimeout(timeoutId);
        greetingModal.style.display = "none";
    });
}

// ===== INICIALIZAÇÃO =====
async function init() {
    try {
        const response = await fetch(`${API_URL}/chats/${currentUserEmail}`);
        if (response.ok) {
            chats = await response.json();
        }
    } catch (err) {
        console.error("Erro ao carregar chats:", err);
    }

    if (chats.length === 0) {
        await createNewChat();
    } else {
        // Sort por recência
        chats.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
        selectChat(chats[0]._id);
    }
}

// ===== GERENCIAMENTO DE CHATS =====
async function createNewChat() {
    const newChatObj = {
        userId: currentUserEmail,
        title: "Nova Conversa",
        messages: [{ role: "system", content: systemPrompt }]
    };
    
    try {
        const response = await fetch(`${API_URL}/chats`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(newChatObj)
        });
        if (response.ok) {
            const dbChat = await response.json();
            chats.unshift(dbChat);
            renderSidebar();
            selectChat(dbChat._id);
        }
    } catch (err) {
        console.error("Erro ao criar chat:", err);
    }
}

function selectChat(id) {
    currentChatId = id;
    const chat = chats.find(c => c._id === id);
    if (!chat) return;
    
    chatDiv.innerHTML = '';
    
    chat.messages.forEach(msg => {
        if (msg.role === 'user') appendMessageUI('user', msg.content);
        if (msg.role === 'assistant') appendMessageUI('bot', msg.content);
    });

    renderSidebar();

    if (window.innerWidth <= 768) {
        sidebar.classList.remove('open');
        appLayout.classList.remove('sidebar-open');
    }
    
    messageInput.focus();
}

async function updateChatTitleIfNeeded(userMessage) {
    const chat = chats.find(c => c._id === currentChatId);
    const userMsgCount = chat.messages.filter(m => m.role === 'user').length;
    
    if (userMsgCount === 1 && chat.title === "Nova Conversa") {
        const newTitle = userMessage.substring(0, 25) + (userMessage.length > 25 ? "..." : "");
        chat.title = newTitle;
        try {
            await fetch(`${API_URL}/chats/${currentChatId}/rename`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ title: newTitle })
            });
            renderSidebar();
        } catch (err) {
            console.error("Erro ao renomear chat automático", err);
        }
    }
}

// ===== INTERFACE (SIDEBAR) =====
function renderSidebar() {
    chatHistoryList.innerHTML = '';
    
    chats.forEach(chat => {
        const btn = document.createElement('div');
        btn.classList.add('history-item');
        if (chat._id === currentChatId) {
            btn.classList.add('active');
        }

        const titleSpan = document.createElement('span');
        titleSpan.classList.add('history-item-title');
        titleSpan.textContent = chat.title;
        titleSpan.onclick = (e) => {
            selectChat(chat._id);
        };
        
        const actionsDiv = document.createElement('div');
        actionsDiv.classList.add('chat-actions');

        const editBtn = document.createElement('button');
        editBtn.classList.add('action-btn');
        editBtn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>';
        editBtn.title = "Renomear";
        editBtn.onclick = (e) => {
            e.stopPropagation();
            renameChat(chat._id);
        };

        const deleteBtn = document.createElement('button');
        deleteBtn.classList.add('action-btn');
        deleteBtn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>';
        deleteBtn.title = "Excluir";
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            deleteChat(chat._id);
        };

        actionsDiv.appendChild(editBtn);
        actionsDiv.appendChild(deleteBtn);

        btn.appendChild(titleSpan);
        btn.appendChild(actionsDiv);
        
        chatHistoryList.appendChild(btn);
    });
}

function renameChat(id) {
    const chat = chats.find(c => c._id === id);
    if (!chat) return;
    
    chatToRenameId = id;
    if (renameInput) renameInput.value = chat.title;
    if (renameModal) {
        renameModal.style.display = 'flex';
        renameInput.focus();
    }
}

async function handleRenameConfirm() {
    if (!chatToRenameId) return;
    const newName = renameInput.value.trim();
    if (newName !== "") {
        const chat = chats.find(c => c._id === chatToRenameId);
        if (chat) {
            try {
                await fetch(`${API_URL}/chats/${chatToRenameId}/rename`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ title: newName })
                });
                chat.title = newName;
                renderSidebar();
            } catch (err) { console.error(err); }
        }
    }
    closeRenameModal();
}

function closeRenameModal() {
    if (renameModal) renameModal.style.display = 'none';
    chatToRenameId = null;
    if (renameInput) renameInput.value = '';
}

function deleteChat(id) {
    chatToDeleteId = id;
    if (deleteModal) deleteModal.style.display = 'flex';
}

async function handleDeleteConfirm() {
    if (!chatToDeleteId) return;
    
    try {
        await fetch(`${API_URL}/chats/${chatToDeleteId}`, { method: "DELETE" });
        chats = chats.filter(c => c._id !== chatToDeleteId);
        
        if (chats.length === 0) {
            await createNewChat();
        } else if (currentChatId === chatToDeleteId) {
            selectChat(chats[0]._id);
        } else {
            renderSidebar();
        }
    } catch (err) {
        console.error(err);
    }
    
    closeDeleteModal();
}

function closeDeleteModal() {
    if (deleteModal) deleteModal.style.display = 'none';
    chatToDeleteId = null;
}

// ===== EVENTOS =====
mobileMenuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    appLayout.classList.toggle('sidebar-open');
});

newChatBtn.addEventListener('click', () => {
    createNewChat();
});

logoutBtn.addEventListener("click", () => {
  localStorage.removeItem("iara_logged_in");
  localStorage.removeItem("iara_user_email");
  window.location.replace("login.html");
});

messageInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
    e.target.style.height = '52px';
  }
});

messageInput.addEventListener("input", function() {
  this.style.height = '52px';
  this.style.height = (this.scrollHeight) + 'px';
});

sendBtn.addEventListener("click", sendMessage);

// Modal Event Listeners
if (renameCancelBtn) renameCancelBtn.addEventListener('click', closeRenameModal);
if (renameConfirmBtn) renameConfirmBtn.addEventListener('click', handleRenameConfirm);
if (renameInput) renameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleRenameConfirm();
});

if (deleteCancelBtn) deleteCancelBtn.addEventListener('click', closeDeleteModal);
if (deleteConfirmBtn) deleteConfirmBtn.addEventListener('click', handleDeleteConfirm);

window.addEventListener('click', (e) => {
    if (renameModal && e.target === renameModal) closeRenameModal();
    if (deleteModal && e.target === deleteModal) closeDeleteModal();
});

// ===== COMUNICAÇÃO (ENVIAR/RECEBER) =====
async function sendMessage() {
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;

  const chat = chats.find(c => c._id === currentChatId);

  // Renderiza a mensagem do usuário (optimistic UI)
  const newMsgObj = { role: "user", content: userMessage };
  chat.messages.push(newMsgObj);
  chat.updatedAt = Date.now();
  
  appendMessageUI("user", userMessage);
  messageInput.value = "";
  
  updateChatTitleIfNeeded(userMessage);

  const loadingId = "loading-" + Date.now();
  appendLoadingUI(loadingId);

  try {
    // Comunicar com o nosso Backend (ele processa e fala com a OpenAI)
    const response = await fetch(`${API_URL}/chats/${currentChatId}/message`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: newMsgObj })
    });

    if (!response.ok) throw new Error("Erro de comunicação com o servidor.");

    const botMsgObj = await response.json();

    removeLoadingUI(loadingId);

    // Atualizar UI com a resposta real da IARA processada lá no servidor
    chat.messages.push(botMsgObj);
    chat.updatedAt = Date.now();
    
    appendMessageUITypewriter("bot", botMsgObj.content);

  } catch (error) {
    console.error("Erro:", error);
    removeLoadingUI(loadingId);
    appendMessageUI("bot", "Ops... algo deu errado. Tente novamente!");
  }
}

// ===== RENDERIZAÇÃO E FORMATAÇÃO =====

function formatMessageHTML(text) {
  const parts = text.split("```");
  let html = "";
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 0) {
      // Plain text
      html += parts[i].replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br>");
    } else {
      // Code block
      const codeContent = parts[i];
      const firstLineBreak = codeContent.indexOf("\n");
      let language = "";
      let code = codeContent;
      if (firstLineBreak !== -1) {
         language = codeContent.substring(0, firstLineBreak).trim();
         code = codeContent.substring(firstLineBreak + 1);
      }
      code = code.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      
      html += `
        <div class="code-block-wrapper">
          <div class="code-block-header">
            <span class="language-label">${language || "código"}</span>
            <button class="copy-btn" onclick="navigator.clipboard.writeText(this.parentElement.nextElementSibling.innerText)">📋 Copiar</button>
          </div>
          <pre><code>${code}</code></pre>
        </div>
      `;
    }
  }
  return html;
}

function appendMessageUI(sender, text) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);

  let prefix = "";
  if (sender === "user") {
    prefix = "<strong>Você:</strong><br>";
  } else if (sender === "bot") {
    prefix = "<strong>IARA:</strong><br>";
  }

  let formattedText = "";
  if (sender === "bot") {
    formattedText = formatMessageHTML(text);
  } else {
    // Preserve multiple spaces and newlines for user input (which may contain pasted code)
    formattedText = text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/ /g, "&nbsp;").replace(/\n/g, "<br>");
  }

  msgDiv.innerHTML = prefix + formattedText;

  const time = document.createElement("time");
  time.textContent = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit"
  });

  msgDiv.appendChild(time);
  chatDiv.appendChild(msgDiv);
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function appendMessageUITypewriter(sender, text) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);

  let prefix = "";
  if (sender === "user") {
    prefix = "<strong>Você:</strong><br>";
  } else if (sender === "bot") {
    prefix = "<strong>IARA:</strong><br>";
  }

  msgDiv.innerHTML = prefix;
  const time = document.createElement("time");
  time.textContent = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  msgDiv.appendChild(time);
  
  chatDiv.appendChild(msgDiv);
  chatDiv.scrollTop = chatDiv.scrollHeight;

  const parts = text.split("```");
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 0) {
      // Texto normal (aparece caracter por caracter)
      const span = document.createElement("span");
      msgDiv.insertBefore(span, time);
      
      const chars = parts[i].split('');
      for (let char of chars) {
        if (char === '\n') span.innerHTML += "<br>";
        else span.innerHTML += char.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        chatDiv.scrollTop = chatDiv.scrollHeight;
        await new Promise(r => setTimeout(r, 7));
      }
    } else {
      // Bloco de Markdown de código (gera a caixa instantaneamente e dita o código nela)
      const codeContent = parts[i];
      const firstLineBreak = codeContent.indexOf("\n");
      let language = "";
      let code = codeContent;
      if (firstLineBreak !== -1) {
         language = codeContent.substring(0, firstLineBreak).trim();
         code = codeContent.substring(firstLineBreak + 1);
      }

      const wrapper = document.createElement("div");
      wrapper.classList.add("code-block-wrapper");
      wrapper.innerHTML = `
        <div class="code-block-header">
          <span class="language-label">${language || "código"}</span>
          <button class="copy-btn" onclick="navigator.clipboard.writeText(this.parentElement.nextElementSibling.innerText)">📋 Copiar</button>
        </div>
        <pre><code></code></pre>
      `;
      msgDiv.insertBefore(wrapper, time);
      const codeEl = wrapper.querySelector("code");

      const chars = code.split('');
      for (let j = 0; j < chars.length; j++) {
        codeEl.innerHTML += chars[j].replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
        if (j % 5 === 0) chatDiv.scrollTop = chatDiv.scrollHeight;
        await new Promise(r => setTimeout(r, 3));
      }
    }
  }
}


function appendLoadingUI(id) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", "bot");
  msgDiv.id = id;
  
  const prefix = "<strong>IARA:</strong> ";
  
  const indicatorDiv = document.createElement("div");
  indicatorDiv.classList.add("typing-indicator");
  indicatorDiv.innerHTML = "<span></span><span></span><span></span>";

  msgDiv.innerHTML = prefix;
  msgDiv.appendChild(indicatorDiv);

  chatDiv.appendChild(msgDiv);
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

function removeLoadingUI(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// Inicia aplicação
init();