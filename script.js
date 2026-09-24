const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const submitBtn = document.getElementById("submit-btn");
const formError = document.getElementById("form-error");

function setError(input, message) {
  const errorSpan = document.querySelector(`[data-error-for="${input.name}"]`);
  errorSpan.textContent = message;
  input.classList.toggle("invalid", Boolean(message));
}

function validateEmail() {
  const value = emailInput.value.trim();
  if (!value) return "Email is required.";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) return "Enter a valid email address.";
  return "";
}

function validatePassword() {
  const value = passwordInput.value;
  if (!value) return "Password is required.";
  if (value.length < 8) return "Password must be at least 8 characters.";
  return "";
}

emailInput.addEventListener("input", () => setError(emailInput, validateEmail()));
passwordInput.addEventListener("input", () => setError(passwordInput, validatePassword()));

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  formError.hidden = true;

  const emailError = validateEmail();
  const passwordError = validatePassword();
  setError(emailInput, emailError);
  setError(passwordInput, passwordError);
  if (emailError || passwordError) return;

  submitBtn.disabled = true;
  submitBtn.textContent = "Signing in...";

  try {
    // Replace with your real auth endpoint
    const res = await fetch("/api/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: emailInput.value.trim(),
        password: passwordInput.value,
      }),
    });

    if (!res.ok) {
      const data = await res.json().catch(() => ({}));
      throw new Error(data.message || "Invalid email or password.");
    }

    form.reset();
    formError.hidden = false;
    formError.style.color = "#4ade80";
    formError.textContent = "Signed in successfully!";
  } catch (err) {
    formError.hidden = false;
    formError.style.color = "";
    formError.textContent = err.message;
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Sign In";
  }
});
