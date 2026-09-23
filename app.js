"use strict";

const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");
const formMessage = document.getElementById("form-message");
const submitBtn = document.getElementById("submit-btn");
const toggleBtn = document.getElementById("toggle-password");

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

function setError(input, errorEl, message) {
  errorEl.textContent = message;
  errorEl.hidden = false;
  input.classList.add("invalid");
  input.setAttribute("aria-invalid", "true");
}

function clearError(input, errorEl) {
  errorEl.textContent = "";
  errorEl.hidden = true;
  input.classList.remove("invalid");
  input.removeAttribute("aria-invalid");
}

function validate() {
  let ok = true;

  if (!emailInput.value.trim()) {
    setError(emailInput, emailError, "Email is required.");
    ok = false;
  } else if (!EMAIL_RE.test(emailInput.value.trim())) {
    setError(emailInput, emailError, "Enter a valid email address.");
    ok = false;
  } else {
    clearError(emailInput, emailError);
  }

  if (!passwordInput.value) {
    setError(passwordInput, passwordError, "Password is required.");
    ok = false;
  } else if (passwordInput.value.length < 8) {
    setError(passwordInput, passwordError, "Password must be at least 8 characters.");
    ok = false;
  } else {
    clearError(passwordInput, passwordError);
  }

  return ok;
}

function showMessage(type, text) {
  formMessage.textContent = text;
  formMessage.className = "form-message " + type;
  formMessage.hidden = false;
}

// Live validation once user leaves a field
emailInput.addEventListener("blur", () => {
  if (emailInput.value && !EMAIL_RE.test(emailInput.value.trim())) {
    setError(emailInput, emailError, "Enter a valid email address.");
  }
});
emailInput.addEventListener("input", () => clearError(emailInput, emailError));

passwordInput.addEventListener("input", () => clearError(passwordInput, passwordError));

// Show / hide password
toggleBtn.addEventListener("click", () => {
  const show = passwordInput.type === "password";
  passwordInput.type = show ? "text" : "password";
  toggleBtn.textContent = show ? "Hide" : "Show";
  toggleBtn.setAttribute("aria-pressed", String(show));
  toggleBtn.setAttribute("aria-label", show ? "Hide password" : "Show password");
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!validate()) {
    showMessage("error", "Please fix the errors above and try again.");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Signing in…";

  try {
    // Placeholder submit — replace with real API call
    await new Promise((resolve) => setTimeout(resolve, 800));
    showMessage("success", "Signed in successfully.");
    form.reset();
  } catch {
    showMessage("error", "Something went wrong. Please try again.");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Sign in";
  }
});
