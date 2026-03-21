// login.js
function showCustomAlert(title, message, callback) {
    const alertModal = document.getElementById("custom-alert");
    const alertTitle = document.getElementById("alert-title");
    const alertMessage = document.getElementById("alert-message");
    const alertOkBtn = document.getElementById("alert-ok-btn");
    
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

document.getElementById("login-form").addEventListener("submit", async function(e) {
  e.preventDefault();

  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value;

  if (!email || !password) {
      showCustomAlert("Erro de Validação", "Por favor, preencha todos os campos obrigatórios.");
      return;
  }

  try {
    const response = await fetch("http://localhost:3000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });
    const data = await response.json();

    if (!response.ok) {
        showCustomAlert("Erro de Autenticação", data.error || "E-mail ou senha inválidos.");
        return;
    }

    localStorage.setItem("iara_logged_in", "true");
    localStorage.setItem("iara_user_email", data.email);
    localStorage.setItem("iara_user_name", data.name);

    showCustomAlert("Sucesso", "Login efetuado com sucesso!", () => {
        window.location.replace("index.html");
    });
  } catch (err) {
      showCustomAlert("Erro de Conexão", "Falha ao conectar com o banco de dados.");
  }
});