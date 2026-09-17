function getCurrentUser() {
  const isLoggedIn = localStorage.getItem("iara_logged_in") === "true";
  let userObj = {};
  try { userObj = JSON.parse(localStorage.getItem("user") || "{}"); } catch (e) {}

  const email = localStorage.getItem("iara_user_email") || userObj.email || "";
  const name = localStorage.getItem("iara_user_name") || userObj.name || "Usuário";
  const role = localStorage.getItem("iara_user_role") || userObj.role || "aluno";

  if (isLoggedIn && email && role) {
    localStorage.setItem("iara_logged_in", "true");
    localStorage.setItem("iara_user_email", email);
    localStorage.setItem("iara_user_role", role);
    localStorage.setItem("iara_user_name", name);
    localStorage.setItem("user", JSON.stringify({ email, name, role }));
  }

  return { isLoggedIn, email, name, role };
}

const activeUser = getCurrentUser();
if (!activeUser.isLoggedIn) {
  window.location.replace("login.html");
}

// ===== CONSTANTES =====
const API_URL = "http://localhost:3000/api";
let currentUserEmail = activeUser.email;
let currentUserName = activeUser.name;

// ===== ELEMENTOS DOM =====
const chatDiv = document.getElementById('chat');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('send-btn');
const cancelBtn = document.getElementById('cancel-btn');
const chatHistoryList = document.getElementById('chat-history-list');
const newChatBtn = document.getElementById('new-chat-btn');
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const sidebar = document.getElementById('sidebar');
const appLayout = document.getElementById('app-layout');
const logoutBtn = document.getElementById("logout-btn");
const userEmailDisplay = document.getElementById("user-email-display");
const userNameDisplay = document.getElementById("user-name-display");
const userAvatarInitial = document.getElementById("user-avatar-initial");

// Modals
const renameModal = document.getElementById('rename-modal');
const renameInput = document.getElementById('rename-input');
const renameCancelBtn = document.getElementById('rename-cancel-btn');
const renameConfirmBtn = document.getElementById('rename-confirm-btn');
const deleteModal = document.getElementById('delete-modal');
const deleteCancelBtn = document.getElementById('delete-cancel-btn');
const deleteConfirmBtn = document.getElementById('delete-confirm-btn');

// Settings Modal Elements (Node 156-43)
const settingsModal = document.getElementById('settings-modal');
const openSettingsBtn = document.getElementById('open-settings-btn');
const settingsForm = document.getElementById('settings-form');
const settingsNameInput = document.getElementById('settings-name');
const settingsEmailInput = document.getElementById('settings-email');
const settingsPasswordInput = document.getElementById('settings-password');
const settingsConfirmPasswordInput = document.getElementById('settings-confirm-password');
const settingsCancelBtn = document.getElementById('settings-cancel-btn');

// Select Class Modal Elements
const selectClassModal = document.getElementById('select-class-modal');
const studentClassesList = document.getElementById('student-classes-list');
const selectClassCancelBtn = document.getElementById('select-class-cancel-btn');

if (selectClassCancelBtn) {
  selectClassCancelBtn.onclick = () => {
    if (selectClassModal) selectClassModal.style.display = 'none';
  };
}

// Alert Modal
function showCustomAlert(title, message, callback) {
  const alertModal = document.getElementById("custom-alert");
  const alertTitle = document.getElementById("alert-title");
  const alertMessage = document.getElementById("alert-message");
  const alertOkBtn = document.getElementById("alert-ok-btn");

  if (alertModal && alertTitle && alertMessage && alertOkBtn) {
    alertTitle.textContent = title;
    alertMessage.textContent = message;
    alertModal.style.display = "flex";

    const handleOk = () => {
      alertModal.style.display = "none";
      alertOkBtn.removeEventListener("click", handleOk);
      if (callback) callback();
    };
    alertOkBtn.addEventListener("click", handleOk);
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}

function escapeJs(str) {
  if (!str) return '';
  return str.replace(/'/g, "\\'").replace(/"/g, '\\"');
}

// ===== ESTADO GLOBAL DA APLICAÇÃO =====
let chats = [];
let currentChatId = null;
let chatToRenameId = null;
let chatToDeleteId = null;
let isGenerating = false;
let generatingChatId = null;
let unreadChatIds = new Set();
let currentAbortController = null;

// Display user info in sidebar & check role for admin RAG button
function updateProfileDisplay() {
  const user = getCurrentUser();
  currentUserEmail = user.email || "user@email.com";
  currentUserName = user.name || "Usuário";
  const userRole = user.role || "aluno";

  if (userEmailDisplay) userEmailDisplay.textContent = currentUserEmail;
  if (userNameDisplay) userNameDisplay.textContent = currentUserName;
  if (userAvatarInitial) userAvatarInitial.textContent = currentUserName.charAt(0).toUpperCase();

  const adminRagBtn = document.getElementById("admin-rag-btn");
  if (adminRagBtn) {
    if (userRole === "professor" || userRole === "admin") {
      adminRagBtn.style.display = "flex";
    } else {
      adminRagBtn.style.display = "none";
    }
  }
}
updateProfileDisplay();

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
    showEmptyState();
  } else {
    chats.sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
    selectChat(chats[0]._id);
  }
}

// ===== GERENCIAMENTO DE CHATS =====
async function createNewChat() {
  try {
    const res = await fetch(`${API_URL}/classes`);
    if (res.ok) {
      const classesList = await res.json();
      if (Array.isArray(classesList) && classesList.length > 0) {
        if (classesList.length === 1) {
          executeCreateChat(classesList[0]._id, classesList[0].name);
        } else {
          openSelectClassModal(classesList);
        }
        return;
      }
    }
  } catch (e) {
    console.error("Erro ao buscar turmas:", e);
  }
  executeCreateChat(null, null);
}

function openSelectClassModal(classesList) {
  if (!selectClassModal || !studentClassesList) {
    executeCreateChat(classesList[0]._id, classesList[0].name);
    return;
  }

  studentClassesList.innerHTML = classesList.map(c => {
    const isProg = c.subject_type === 'programming';
    const badgeText = isProg ? '💻 Computação' : '📝 Outra Matéria';
    const badgeBg = isProg ? '#fdf0f5' : '#f3e8ff';
    const badgeColor = isProg ? '#ff5c8a' : '#a855f7';

    return `
      <div class="class-modal-item" onclick="executeCreateChat('${c._id}', '${escapeJs(c.name)}')" 
           style="background: white; border: 1.5px solid rgba(255, 92, 138, 0.2); border-radius: 14px; padding: 12px 16px; cursor: pointer; transition: all 0.2s; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <div style="font-weight: 700; color: #2d2b38; font-size: 14px;">${escapeHtml(c.name)}</div>
          <div style="font-size: 12px; color: #777;">${escapeHtml(c.description || c.code || '')}</div>
        </div>
        <span style="background: ${badgeBg}; color: ${badgeColor}; font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 12px;">${badgeText}</span>
      </div>
    `;
  }).join('');

  selectClassModal.style.display = 'flex';
}

async function executeCreateChat(class_id, class_name) {
  if (selectClassModal) selectClassModal.style.display = 'none';

  const newChatObj = {
    userId: currentUserEmail,
    title: "Nova Conversa",
    class_id: class_id || null,
    class_name: class_name || null
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

      if (sidebar.classList.contains('empty-sidebar')) {
        initiateLogoAnimation();
        completeInterfaceTransition(dbChat._id);
      } else {
        renderSidebar();
        selectChat(dbChat._id);
        document.getElementById('input-area').style.display = 'flex';
      }
    }
  } catch (err) {
    console.error("Erro ao criar chat:", err);
  }
}

function initiateLogoAnimation() {
  sidebar.classList.remove('empty-sidebar');
}

function completeInterfaceTransition(id) {
  document.getElementById('input-area').style.display = 'none';

  setTimeout(() => {
    sidebar.classList.remove('sidebar-hide-content');
    if (newChatBtn) newChatBtn.classList.remove('hidden');
    if (chatHistoryList) chatHistoryList.classList.remove('hidden');
    document.getElementById('input-area').style.display = 'flex';

    renderSidebar();
    if (id) {
      const chat = chats.find(c => c._id === id);
      if (chat) {
        currentChatId = id;
        chatDiv.innerHTML = '';
        chat.messages.forEach(msg => {
          if (msg.role === 'user') appendMessageUI('user', msg.content);
          if (msg.role === 'assistant') appendMessageUI('bot', msg.content);
        });
        messageInput.focus();
      }
    }
  }, 300);
}

function selectChat(id) {
  if (unreadChatIds.has(id)) {
    unreadChatIds.delete(id);
  }
  currentChatId = id;
  const chat = chats.find(c => c._id === id);
  if (!chat) return;

  const badgeEl = document.getElementById('active-chat-class-badge');
  if (badgeEl) {
    if (chat.class_name) {
      badgeEl.innerText = `📚 ${chat.class_name}`;
      badgeEl.style.display = 'inline-block';
    } else {
      badgeEl.style.display = 'none';
    }
  }

  if (sidebar.classList.contains('empty-sidebar')) {
    initiateLogoAnimation();
    completeInterfaceTransition(id);
    return;
  }

  document.getElementById('input-area').style.display = 'flex';
  if (newChatBtn) newChatBtn.classList.remove('hidden');
  if (chatHistoryList) chatHistoryList.classList.remove('hidden');
  sidebar.classList.remove('sidebar-hide-content');

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

// ===== INTERFACE (SIDEBAR) =====
function renderSidebar() {
  if (!chatHistoryList) return;
  chatHistoryList.innerHTML = '';

  if (chats.length === 0) {
    if (newChatBtn) newChatBtn.classList.add('hidden');
    chatHistoryList.classList.add('hidden');
  } else {
    if (newChatBtn) newChatBtn.classList.remove('hidden');
    chatHistoryList.classList.remove('hidden');
  }

  chats.forEach(chat => {
    const btn = document.createElement('div');
    btn.classList.add('history-item');
    if (chat._id === currentChatId) {
      btn.classList.add('active');
    }

    const textContainer = document.createElement('div');
    textContainer.style.display = 'flex';
    textContainer.style.flexDirection = 'column';
    textContainer.style.overflow = 'hidden';
    textContainer.style.flex = '1';
    textContainer.style.cursor = 'pointer';
    textContainer.onclick = () => selectChat(chat._id);

    const titleSpan = document.createElement('span');
    titleSpan.classList.add('history-item-title');
    titleSpan.textContent = chat.title;
    textContainer.appendChild(titleSpan);

    if (chat.class_name) {
      const classSpan = document.createElement('span');
      classSpan.style.fontSize = '10px';
      classSpan.style.color = '#ff5c8a';
      classSpan.style.fontWeight = '700';
      classSpan.style.textOverflow = 'ellipsis';
      classSpan.style.overflow = 'hidden';
      classSpan.style.whiteSpace = 'nowrap';
      classSpan.style.marginTop = '2px';
      classSpan.textContent = `📚 ${chat.class_name}`;
      textContainer.appendChild(classSpan);
    }

    let indicator = null;
    if (chat._id === generatingChatId) {
      indicator = document.createElement('div');
      indicator.classList.add('generating-indicator');
      indicator.title = "Gerando resposta...";
      indicator.innerHTML = '<span class="generating-dot"></span><span class="generating-text">Gerando</span>';
      indicator.onclick = () => selectChat(chat._id);
    } else if (unreadChatIds.has(chat._id)) {
      indicator = document.createElement('div');
      indicator.classList.add('generating-indicator', 'unread');
      indicator.title = "Nova resposta pronta!";
      indicator.innerHTML = '<span class="generating-dot"></span><span class="generating-text">Nova</span>';
      indicator.onclick = () => selectChat(chat._id);
    }

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

    btn.appendChild(textContainer);
    if (indicator) btn.appendChild(indicator);
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
      showEmptyState();
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

// Welcome State / Tela Inicial (Node 156-42)
function showEmptyState() {
  renderSidebar();
  chatDiv.innerHTML = `
    <div class="welcome-hero-container">
      <div class="welcome-hero-avatar">
        <img src="assets/NewIaraLogo.png" alt="IARA Logo" class="welcome-hero-logo-img" />
      </div>
      <h2 class="welcome-hero-title">Bem-vindo a <span class="highlight-pink">IARA</span></h2>
      <p class="welcome-hero-subtitle">Sua tutora virtual de programação. Comece uma nova conversa para tirar duvidas ou praticar exercícios.</p>
      <button id="start-conversation-btn" class="btn-gradient welcome-hero-btn">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
         Iniciar conversa
      </button>
    </div>
  `;

  document.getElementById('input-area').style.display = 'none';
  if (newChatBtn) newChatBtn.classList.add('hidden');
  sidebar.classList.add('empty-sidebar');
  sidebar.classList.add('sidebar-hide-content');

  const startBtn = document.getElementById('start-conversation-btn');
  if (startBtn) {
    startBtn.onclick = () => createNewChat();
  }
}

// ===== CONFIGURAÇÕES MODAL LOGIC (Node 156-43) =====
function openSettingsModal() {
  if (settingsNameInput) settingsNameInput.value = currentUserName;
  if (settingsEmailInput) settingsEmailInput.value = currentUserEmail;
  if (settingsPasswordInput) settingsPasswordInput.value = "";
  if (settingsConfirmPasswordInput) settingsConfirmPasswordInput.value = "";
  if (settingsModal) settingsModal.style.display = 'flex';
}

function closeSettingsModal() {
  if (settingsModal) settingsModal.style.display = 'none';
}

if (openSettingsBtn) openSettingsBtn.addEventListener('click', openSettingsModal);
if (settingsCancelBtn) settingsCancelBtn.addEventListener('click', closeSettingsModal);

if (settingsForm) {
  settingsForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const newName = settingsNameInput.value.trim();
    const newEmail = settingsEmailInput.value.trim();
    const pass = settingsPasswordInput.value;
    const confirmPass = settingsConfirmPasswordInput.value;

    if (!newName || !newEmail) {
      showCustomAlert("Erro de Validação", "Nome e E-mail não podem ficar vazios.");
      return;
    }

    if (pass && pass !== confirmPass) {
      showCustomAlert("Erro de Validação", "As senhas não coincidem.");
      return;
    }

    localStorage.setItem("iara_user_name", newName);
    localStorage.setItem("iara_user_email", newEmail);
    updateProfileDisplay();
    closeSettingsModal();
    showCustomAlert("Sucesso", "Perfil atualizado com sucesso!");
  });
}

// ===== EVENTOS =====
if (mobileMenuBtn) {
  mobileMenuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('open');
    appLayout.classList.toggle('sidebar-open');
  });
}

if (newChatBtn) {
  newChatBtn.addEventListener('click', () => {
    createNewChat();
  });
}

if (logoutBtn) {
  logoutBtn.addEventListener("click", () => {
    localStorage.clear();
    window.location.replace("login.html");
  });
}

if (messageInput) {
  messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
      e.target.style.height = '52px';
    }
  });

  messageInput.addEventListener("input", function () {
    this.style.height = '52px';
    this.style.height = (this.scrollHeight) + 'px';
  });
}

if (sendBtn) sendBtn.addEventListener("click", sendMessage);
if (cancelBtn) {
  cancelBtn.addEventListener("click", () => {
    if (currentAbortController) {
      currentAbortController.abort();
    }
    isGenerating = false;
  });
}

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
  if (settingsModal && e.target === settingsModal) closeSettingsModal();
});

// ===== COMUNICAÇÃO (ENVIAR/RECEBER) =====
async function sendMessage() {
  if (isGenerating) return;
  const userMessage = messageInput.value.trim();
  if (!userMessage) return;

  const targetChatId = currentChatId;
  const chat = chats.find(c => c._id === targetChatId);
  if (!chat) return;

  isGenerating = true;
  generatingChatId = targetChatId;
  messageInput.disabled = true;
  sendBtn.style.display = 'none';
  if (cancelBtn) cancelBtn.style.display = 'flex';

  const newMsgObj = { role: "user", content: userMessage };
  chat.messages.push(newMsgObj);
  chat.updatedAt = Date.now();

  messageInput.value = "";
  messageInput.style.height = '52px';

  if (currentChatId === targetChatId) {
    appendMessageUI("user", userMessage);
  }

  const loadingId = "loading-" + Date.now();
  if (currentChatId === targetChatId) {
    appendLoadingUI(loadingId);
  }

  renderSidebar();

  currentAbortController = new AbortController();

  try {
    const response = await fetch(`${API_URL}/chats/${targetChatId}/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: newMsgObj }),
      signal: currentAbortController.signal
    });

    if (!response.ok) throw new Error("Erro de comunicação com o servidor.");

    const { botMsgObj, newTitle } = await response.json();

    if (currentChatId === targetChatId) {
      removeLoadingUI(loadingId);
    }

    chat.messages.push(botMsgObj);

    if (newTitle) {
      chat.title = newTitle;
    }

    chat.updatedAt = Date.now();
    renderSidebar();

    if (currentChatId === targetChatId) {
      await appendMessageUITypewriter("bot", botMsgObj.content, targetChatId);
    } else {
      unreadChatIds.add(targetChatId);
    }

  } catch (error) {
    if (currentChatId === targetChatId) {
      removeLoadingUI(loadingId);
    }
    if (error.name === 'AbortError') {
      if (currentChatId === targetChatId) {
        appendMessageUI("bot", "A geração da resposta foi cancelada.");
      }
    } else {
      console.error("Erro:", error);
      if (currentChatId === targetChatId) {
        appendMessageUI("bot", "Ops... algo deu errado. Tente novamente!");
      }
    }
  } finally {
    isGenerating = false;
    generatingChatId = null;
    if (currentChatId !== targetChatId && chat.messages.length > 0) {
      unreadChatIds.add(targetChatId);
    }
    messageInput.disabled = false;
    sendBtn.style.display = 'flex';
    if (cancelBtn) cancelBtn.style.display = 'none';
    currentAbortController = null;
    renderSidebar();
    if (currentChatId === targetChatId) {
      messageInput.focus();
    }
  }
}

// ===== RENDERIZAÇÃO E FORMATAÇÃO =====

const katexExtension = {
  name: 'katex',
  level: 'inline',
  start(src) { return src.match(/\$|\\\(|\\\[/)?.index; },
  tokenizer(src, tokens) {
    const blockMatch = src.match(/^\$\$([\s\S]+?)\$\$/);
    if (blockMatch) {
      return { type: 'katex', raw: blockMatch[0], text: blockMatch[1].trim(), displayMode: true };
    }
    const blockBracketMatch = src.match(/^\\\[([\s\S]+?)\\\]/);
    if (blockBracketMatch) {
      return { type: 'katex', raw: blockBracketMatch[0], text: blockBracketMatch[1].trim(), displayMode: true };
    }
    const inlineMatch = src.match(/^\$([^$]+?)\$/);
    if (inlineMatch) {
      return { type: 'katex', raw: inlineMatch[0], text: inlineMatch[1].trim(), displayMode: false };
    }
    const inlineBracketMatch = src.match(/^\\\(([\s\S]+?)\\\)/);
    if (inlineBracketMatch) {
      return { type: 'katex', raw: inlineBracketMatch[0], text: inlineBracketMatch[1].trim(), displayMode: false };
    }
  },
  renderer(token) {
    return katex.renderToString(token.text, {
      displayMode: token.displayMode,
      throwOnError: false
    });
  }
};

if (window.marked && window.katex) {
  marked.use({ extensions: [katexExtension] });
}

function formatMessageHTML(text) {
  if (!window.marked) return text;
  const html = marked.parse(text, { breaks: true, gfm: true });

  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;

  const codeBlocks = tempDiv.querySelectorAll('pre code');
  codeBlocks.forEach(codeEl => {
    const preEl = codeEl.parentElement;
    const codeText = codeEl.innerText;
    const langMatch = codeEl.className.match(/language-(\w+)/);
    const language = langMatch ? langMatch[1] : "código";

    const wrapper = document.createElement('div');
    wrapper.className = 'code-block-wrapper';
    wrapper.innerHTML = `
      <div class="code-block-header">
        <span class="code-lang-badge">${language}</span>
        <button class="copy-btn" onclick="navigator.clipboard.writeText(this.parentElement.nextElementSibling.innerText); this.innerHTML='✓ copiado'; setTimeout(() => this.innerHTML='<svg width=\\'14\\' height=\\'14\\' viewBox=\\'0 0 24 24\\' fill=\\'none\\' stroke=\\'currentColor\\' stroke-width=\\'2\\' stroke-linecap=\\'round\\' stroke-linejoin=\\'round\\'><rect x=\\'9\\' y=\\'9\\' width=\\'13\\' height=\\'13\\' rx=\\'2\\' ry=\\'2\\'></rect><path d=\\'M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1\\'></path></svg> copiar', 2000)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
          copiar
        </button>
      </div>
      <pre><code>${codeText.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</code></pre>
    `;
    preEl.replaceWith(wrapper);
  });

  let htmlResult = tempDiv.innerHTML;
  htmlResult = htmlResult.replace(
    /(<p>)?📚\s*Informação retirada do acervo de fontes da turma(<\/p>)?/gi,
    '<div class="source-badge turma-source"><span class="source-badge-icon">📚</span> <span>Informação retirada do acervo de fontes da turma</span></div>'
  );
  htmlResult = htmlResult.replace(
    /(<p>)?🌐\s*Fontes diversas da internet(<\/p>)?/gi,
    '<div class="source-badge internet-source"><span class="source-badge-icon">🌐</span> <span>Fontes diversas da internet</span></div>'
  );

  return htmlResult;
}

// Chat UI Bubbles (Nodes 156-44 & 156-45)
function appendMessageUI(sender, text) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);

  const timeStr = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  if (sender === "bot") {
    msgDiv.innerHTML = `
      <div class="message-bot-container">
        <div class="message-bot-avatar">
          <img src="assets/NewIaraLogo.png" alt="IARA" class="message-bot-logo-img" />
        </div>
        <div class="message-bubble-content">
          <div class="message-header-line">
            <span class="sender-name">IARA</span>
            <span class="time">${timeStr}</span>
          </div>
          <div class="message-text">${formatMessageHTML(text)}</div>
        </div>
      </div>
    `;
  } else {
    msgDiv.innerHTML = `
      <div class="message-user-container">
        <div class="message-header-line user-header-line">
          <span class="sender-name">${currentUserName.split(' ')[0]}</span>
          <span class="time">${timeStr}</span>
        </div>
        <div class="message-text">${text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/ /g, "&nbsp;").replace(/\n/g, "<br>")}</div>
      </div>
    `;
  }

  chatDiv.appendChild(msgDiv);
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

async function appendMessageUITypewriter(sender, text, targetChatId) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  const timeStr = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

  msgDiv.innerHTML = `
    <div class="message-bot-container">
      <div class="message-bot-avatar">
        <img src="assets/NewIaraLogo.png" alt="IARA" class="message-bot-logo-img" />
      </div>
      <div class="message-bubble-content">
        <div class="message-header-line">
          <span class="sender-name">IARA</span>
          <span class="time">${timeStr}</span>
        </div>
        <div class="message-text"></div>
      </div>
    </div>
  `;

  chatDiv.appendChild(msgDiv);
  chatDiv.scrollTop = chatDiv.scrollHeight;

  const contentDiv = msgDiv.querySelector(".message-text");
  let currentRawText = "";
  const parts = text.split("```");

  for (let i = 0; i < parts.length; i++) {
    if (!isGenerating || currentChatId !== targetChatId) break;
    if (i % 2 === 0) {
      const chars = parts[i].split('');
      for (let char of chars) {
        if (!isGenerating || currentChatId !== targetChatId) break;
        currentRawText += char;
        contentDiv.innerHTML = formatMessageHTML(currentRawText);
        chatDiv.scrollTop = chatDiv.scrollHeight;
        await new Promise(r => setTimeout(r, 4));
      }
    } else {
      const codeBlockFull = "```" + parts[i] + "```";
      currentRawText += codeBlockFull;
      contentDiv.innerHTML = formatMessageHTML(currentRawText);
      chatDiv.scrollTop = chatDiv.scrollHeight;
      await new Promise(r => setTimeout(r, 40));
    }
  }

  if (currentChatId === targetChatId) {
    contentDiv.innerHTML = formatMessageHTML(text);
    chatDiv.scrollTop = chatDiv.scrollHeight;
  }
}

function appendLoadingUI(id) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", "bot");
  msgDiv.id = id;

  msgDiv.innerHTML = `
    <div class="message-bot-container">
      <div class="message-bot-avatar">
        <img src="assets/NewIaraLogo.png" alt="IARA" class="message-bot-logo-img" />
      </div>
      <div class="message-bubble-content">
        <div class="message-header-line">
          <span class="sender-name">IARA</span>
        </div>
        <div class="typing-indicator"><span></span><span></span><span></span></div>
      </div>
    </div>
  `;

  chatDiv.appendChild(msgDiv);
  chatDiv.scrollTop = chatDiv.scrollHeight;
}

function removeLoadingUI(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// Inicia aplicação
init();