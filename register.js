// register.js
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

const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const confirmPasswordInput = document.getElementById("confirm-password");
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

// Visual indication for email
emailInput.addEventListener("input", function() {
    if (emailInput.value.trim() === "") {
        emailInput.style.borderColor = "";
    } else if (emailRegex.test(emailInput.value.trim())) {
        emailInput.style.borderColor = "#28a745"; // green
    } else {
        emailInput.style.borderColor = "#ff4757"; // red
    }
});

// Visual indication for matching passwords
function checkPasswords() {
    if (passwordInput.value === "" && confirmPasswordInput.value === "") {
        passwordInput.style.borderColor = "";
        confirmPasswordInput.style.borderColor = "";
        return;
    }
    
    if (passwordInput.value !== "") {
        if (passwordInput.value.length < 4) {
            passwordInput.style.borderColor = "#ff4757";
        } else {
            passwordInput.style.borderColor = "#28a745";
        }
    }

    if (confirmPasswordInput.value !== "") {
        if (passwordInput.value === confirmPasswordInput.value) {
            confirmPasswordInput.style.borderColor = "#28a745";
        } else {
            confirmPasswordInput.style.borderColor = "#ff4757";
        }
    } else {
        confirmPasswordInput.style.borderColor = "";
    }
}

passwordInput.addEventListener("input", checkPasswords);
confirmPasswordInput.addEventListener("input", checkPasswords);

document.getElementById("register-form").addEventListener("submit", async function(e) {
  e.preventDefault();

  const name = document.getElementById("name").value.trim();
  const email = emailInput.value.trim();
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

  // Validate empty fields via popup
  if (!name || !email || !password || !confirmPassword) {
      showCustomAlert("Erro de Validação", "Por favor, preencha todos os campos obrigatórios.");
      return;
  }

  // Visual validations (block submit without popup if invalid)
  if (!emailRegex.test(email)) {
      emailInput.focus();
      return;
  }

  // Optional: keep popup for password length/match, or handle visually
  // "esse não precisa de uma janela de erro" refers specifically to the email ("email válido (esse não precisa...)")
  if (password.length < 4) {
    showCustomAlert("Erro de Validação", "A senha deve ter pelo menos 4 caracteres.");
    return;
  }

  if (password !== confirmPassword) {
    showCustomAlert("Erro de Validação", "As senhas não coincidem.");
    return;
  }


  try {
    const response = await fetch("http://localhost:3000/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    });
    const data = await response.json();

    if (!response.ok) {
        showCustomAlert("Erro de Cadastro", data.error || "Não foi possível concluir o cadastro.");
        return;
    }

    // Auto-login after successful registration (RF11)
    localStorage.setItem("iara_logged_in", "true");
    localStorage.setItem("iara_user_email", data.user.email);
    localStorage.setItem("iara_user_name", data.user.name);

    showCustomAlert("Sucesso", data.message || "Cadastro realizado com sucesso!", () => {
        window.location.replace("index.html");
    });
  } catch (err) {
      showCustomAlert("Erro de Conexão", "Falha ao se conectar com o servidor da base de dados.");
  }
});
