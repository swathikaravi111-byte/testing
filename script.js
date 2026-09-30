// DOM Elements
const loginForm = document.getElementById('loginForm');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const togglePasswordBtn = document.getElementById('togglePassword');
const rememberMeCheckbox = document.getElementById('rememberMe');
const emailError = document.getElementById('emailError');
const passwordError = document.getElementById('passwordError');

// Toggle password visibility
togglePasswordBtn.addEventListener('click', (e) => {
    e.preventDefault();
    const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput.setAttribute('type', type);
    togglePasswordBtn.classList.toggle('active');
});

// Clear error messages on input
emailInput.addEventListener('input', () => {
    emailError.textContent = '';
    emailError.classList.remove('show');
});

passwordInput.addEventListener('input', () => {
    passwordError.textContent = '';
    passwordError.classList.remove('show');
});

// Email validation
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Form submission
loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    let isValid = true;

    // Reset errors
    emailError.textContent = '';
    emailError.classList.remove('show');
    passwordError.textContent = '';
    passwordError.classList.remove('show');

    // Validate email
    if (!email) {
        emailError.textContent = 'Email is required';
        emailError.classList.add('show');
        isValid = false;
    } else if (!validateEmail(email)) {
        emailError.textContent = 'Please enter a valid email address';
        emailError.classList.add('show');
        isValid = false;
    }

    // Validate password
    if (!password) {
        passwordError.textContent = 'Password is required';
        passwordError.classList.add('show');
        isValid = false;
    } else if (password.length < 6) {
        passwordError.textContent = 'Password must be at least 6 characters';
        passwordError.classList.add('show');
        isValid = false;
    }

    if (!isValid) return;

    // Disable button during submission
    const submitBtn = loginForm.querySelector('.login-button');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Signing in...';

    try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Save remember me preference
        if (rememberMeCheckbox.checked) {
            localStorage.setItem('rememberedEmail', email);
        } else {
            localStorage.removeItem('rememberedEmail');
        }

        // Success - in a real app, you'd redirect or update UI
        showSuccessMessage('Login successful! Redirecting...');
        console.log('Login successful:', { email, rememberMe: rememberMeCheckbox.checked });

        // Simulate redirect after 1.5 seconds
        setTimeout(() => {
            // window.location.href = '/dashboard';
            alert('In a real application, you would be redirected to the dashboard.');
        }, 1500);

    } catch (error) {
        passwordError.textContent = 'Login failed. Please try again.';
        passwordError.classList.add('show');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign In';
    }
});

// Load remembered email
function loadRememberedEmail() {
    const rememberedEmail = localStorage.getItem('rememberedEmail');
    if (rememberedEmail) {
        emailInput.value = rememberedEmail;
        rememberMeCheckbox.checked = true;
    }
}

// Show success message
function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        font-weight: 500;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    successDiv.textContent = message;
    document.body.appendChild(successDiv);

    setTimeout(() => {
        successDiv.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => successDiv.remove(), 300);
    }, 3000);
}

// Social login handlers
document.querySelectorAll('.social-button').forEach(button => {
    button.addEventListener('click', (e) => {
        e.preventDefault();
        const provider = button.classList.contains('google') ? 'Google' : 'GitHub';
        alert(`Sign in with ${provider} - Not implemented in this demo`);
    });
});

// Forgot password handler
document.querySelector('.forgot-password').addEventListener('click', (e) => {
    e.preventDefault();
    alert('Forgot password functionality - Not implemented in this demo');
});

// Sign up link handler
document.querySelector('.signup-link a').addEventListener('click', (e) => {
    e.preventDefault();
    alert('Sign up page - Not implemented in this demo');
});

// Initialize on page load
window.addEventListener('load', () => {
    loadRememberedEmail();
    emailInput.focus();
});
