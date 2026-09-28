/**
 * Modern Login Page - JavaScript Functionality
 * Handles form validation, animations, accessibility, and user interactions
 */

// ============================================
// Utility Functions
// ============================================

/**
 * Utility class for common functions
 */
class Utils {
    /**
     * Validate email format
     * @param {string} email - Email to validate
     * @returns {boolean}
     */
    static isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate password strength
     * @param {string} password - Password to validate
     * @returns {object} - Validation result with score and feedback
     */
    static validatePasswordStrength(password) {
        const result = {
            score: 0,
            feedback: [],
            isStrong: false
        };

        if (password.length >= 8) {
            result.score++;
        } else {
            result.feedback.push('At least 8 characters');
        }

        if (/[a-z]/.test(password)) {
            result.score++;
        } else {
            result.feedback.push('One lowercase letter');
        }

        if (/[A-Z]/.test(password)) {
            result.score++;
        } else {
            result.feedback.push('One uppercase letter');
        }

        if (/[0-9]/.test(password)) {
            result.score++;
        } else {
            result.feedback.push('One number');
        }

        if (/[^a-zA-Z0-9]/.test(password)) {
            result.score++;
        }

        result.isStrong = result.score >= 4;
        return result;
    }

    /**
     * Debounce function to prevent excessive function calls
     * @param {function} func - Function to debounce
     * @param {number} delay - Delay in milliseconds
     * @returns {function}
     */
    static debounce(func, delay = 300) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func.apply(this, args), delay);
        };
    }

    /**
     * Check if device is touch-enabled
     * @returns {boolean}
     */
    static isTouchDevice() {
        return (('ontouchstart' in window) ||
                (navigator.maxTouchPoints > 0) ||
                (navigator.msMaxTouchPoints > 0));
    }

    /**
     * Generate random string for unique IDs
     * @param {number} length - Length of string
     * @returns {string}
     */
    static generateId(length = 8) {
        return Math.random().toString(36).substring(2, 2 + length);
    }
}

// ============================================
// Toast Notification Manager
// ============================================

/**
 * Manages toast notifications
 */
class ToastManager {
    constructor() {
        this.toastContainer = document.querySelector('.toast-container');
        this.successToast = document.getElementById('successToast');
        this.errorToast = document.getElementById('errorToast');
        this.hideTimeout = null;
    }

    /**
     * Show success toast
     * @param {string} message - Message to display
     * @param {number} duration - Duration to show (ms)
     */
    show(type, message, duration = 4000) {
        const toast = type === 'success' ? this.successToast : this.errorToast;
        const messageElement = toast.querySelector('span');

        messageElement.textContent = message;
        toast.classList.add('show');

        // Clear previous timeout
        if (this.hideTimeout) clearTimeout(this.hideTimeout);

        // Auto-hide after duration
        this.hideTimeout = setTimeout(() => this.hide(type), duration);
    }

    /**
     * Hide toast
     * @param {string} type - Toast type (success/error)
     */
    hide(type) {
        const toast = type === 'success' ? this.successToast : this.errorToast;
        toast.classList.remove('show');
    }

    /**
     * Show success message
     * @param {string} message - Message to display
     */
    success(message) {
        this.show('success', message);
    }

    /**
     * Show error message
     * @param {string} message - Message to display
     */
    error(message) {
        this.show('error', message);
    }
}

// ============================================
// Form Validator
// ============================================

/**
 * Manages form validation
 */
class FormValidator {
    constructor(form) {
        this.form = form;
        this.fields = {
            email: form.querySelector('#email'),
            password: form.querySelector('#password')
        };
        this.errors = {};
        this.touched = {};
    }

    /**
     * Validate email field
     * @returns {boolean}
     */
    validateEmail() {
        const email = this.fields.email.value.trim();
        const emailError = document.getElementById('emailError');

        if (!email) {
            this.errors.email = 'Email is required';
            emailError.textContent = this.errors.email;
            this.fields.email.classList.add('error');
            this.fields.email.classList.remove('success');
            return false;
        }

        if (!Utils.isValidEmail(email)) {
            this.errors.email = 'Please enter a valid email address';
            emailError.textContent = this.errors.email;
            this.fields.email.classList.add('error');
            this.fields.email.classList.remove('success');
            return false;
        }

        delete this.errors.email;
        emailError.textContent = '';
        this.fields.email.classList.remove('error');
        this.fields.email.classList.add('success');
        return true;
    }

    /**
     * Validate password field
     * @returns {boolean}
     */
    validatePassword() {
        const password = this.fields.password.value;
        const passwordError = document.getElementById('passwordError');

        if (!password) {
            this.errors.password = 'Password is required';
            passwordError.textContent = this.errors.password;
            this.fields.password.classList.add('error');
            this.fields.password.classList.remove('success');
            return false;
        }

        if (password.length < 6) {
            this.errors.password = 'Password must be at least 6 characters';
            passwordError.textContent = this.errors.password;
            this.fields.password.classList.add('error');
            this.fields.password.classList.remove('success');
            return false;
        }

        delete this.errors.password;
        passwordError.textContent = '';
        this.fields.password.classList.remove('error');
        this.fields.password.classList.add('success');
        return true;
    }

    /**
     * Validate all fields
     * @returns {boolean}
     */
    validateAll() {
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        return isEmailValid && isPasswordValid;
    }

    /**
     * Clear all errors
     */
    clearErrors() {
        this.errors = {};
        Object.values(this.fields).forEach(field => {
            field.classList.remove('error', 'success');
            const errorElement = field.parentElement.querySelector('.input-error');
            if (errorElement) errorElement.textContent = '';
        });
    }
}

// ============================================
// Theme Manager
// ============================================

/**
 * Manages light/dark theme
 */
class ThemeManager {
    constructor() {
        this.toggle = document.querySelector('.theme-toggle');
        this.prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        this.init();
    }

    init() {
        // Check saved theme preference
        const savedTheme = localStorage.getItem('theme');
        const systemTheme = this.prefersDark.matches ? 'dark' : 'light';
        const theme = savedTheme || systemTheme;

        this.setTheme(theme);

        // Listen for toggle
        this.toggle.addEventListener('click', () => this.toggleTheme());

        // Listen for system theme changes
        this.prefersDark.addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.setTheme(e.matches ? 'dark' : 'light');
            }
        });
    }

    /**
     * Set theme
     * @param {string} theme - 'light' or 'dark'
     */
    setTheme(theme) {
        const isDark = theme === 'dark';
        document.body.classList.toggle('dark-mode', isDark);
        localStorage.setItem('theme', theme);
        this.updateToggleIcon(isDark);
    }

    /**
     * Toggle between light and dark theme
     */
    toggleTheme() {
        const currentTheme = localStorage.getItem('theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }

    /**
     * Update toggle button icon
     * @param {boolean} isDark - Is dark mode enabled
     */
    updateToggleIcon(isDark) {
        const icon = this.toggle.querySelector('i');
        icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    }
}

// ============================================
// Password Visibility Toggle
// ============================================

/**
 * Manages password visibility toggle
 */
class PasswordToggle {
    constructor() {
        this.toggleButtons = document.querySelectorAll('.toggle-password');
        this.init();
    }

    init() {
        this.toggleButtons.forEach(button => {
            button.addEventListener('click', (e) => this.handleToggle(e));
        });
    }

    /**
     * Handle password visibility toggle
     * @param {event} e - Click event
     */
    handleToggle(e) {
        e.preventDefault();
        const button = e.currentTarget;
        const input = button.closest('.input-wrapper').querySelector('.form-input');
        const icon = button.querySelector('i');

        const isPassword = input.type === 'password';
        input.type = isPassword ? 'text' : 'password';
        icon.classList.toggle('fa-eye', isPassword);
        icon.classList.toggle('fa-eye-slash', !isPassword);

        // Update aria-label
        button.setAttribute('aria-label', 
            isPassword ? 'Hide password' : 'Show password'
        );

        // Focus input for better UX
        input.focus();
    }
}

// ============================================
// Login Form Handler
// ============================================

/**
 * Manages login form submission and interactions
 */
class LoginFormHandler {
    constructor() {
        this.form = document.getElementById('loginForm');
        this.validator = new FormValidator(this.form);
        this.toastManager = new ToastManager();
        this.submitButton = this.form.querySelector('.btn-primary');
        this.emailField = this.form.querySelector('#email');
        this.passwordField = this.form.querySelector('#password');
        this.rememberMeCheckbox = this.form.querySelector('#rememberMe');
        this.init();
    }

    init() {
        // Form submission
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));

        // Real-time validation
        this.emailField.addEventListener('blur', () => this.validator.validateEmail());
        this.passwordField.addEventListener('blur', () => this.validator.validatePassword());

        // Input event for real-time feedback
        this.emailField.addEventListener('input', Utils.debounce(() => {
            if (this.validator.touched.email) {
                this.validator.validateEmail();
            }
        }, 300));

        this.passwordField.addEventListener('input', Utils.debounce(() => {
            if (this.validator.touched.password) {
                this.validator.validatePassword();
            }
        }, 300));

        // Mark as touched on focus
        this.emailField.addEventListener('focus', () => {
            this.validator.touched.email = true;
        });

        this.passwordField.addEventListener('focus', () => {
            this.validator.touched.password = true;
        });

        // Load saved credentials if "Remember Me" was checked
        this.loadSavedCredentials();

        // Forgot Password link
        this.setupForgotPasswordLink();

        // Social login buttons
        this.setupSocialLogin();

        // Sign up link
        this.setupSignUpLink();
    }

    /**
     * Handle form submission
     * @param {event} e - Form submit event
     */
    handleSubmit(e) {
        e.preventDefault();

        // Validate form
        if (!this.validator.validateAll()) {
            this.toastManager.error('Please fix the errors in the form');
            return;
        }

        // Show loading state
        this.setLoadingState(true);

        // Simulate API call
        setTimeout(() => {
            this.handleLoginSuccess();
        }, 1500);
    }

    /**
     * Handle successful login
     */
    handleLoginSuccess() {
        const email = this.emailField.value;
        const rememberMe = this.rememberMeCheckbox.checked;

        // Save credentials if "Remember Me" is checked
        if (rememberMe) {
            localStorage.setItem('savedEmail', email);
            localStorage.setItem('rememberMe', 'true');
        } else {
            localStorage.removeItem('savedEmail');
            localStorage.removeItem('rememberMe');
        }

        // Show success message
        this.toastManager.success(`Welcome back, ${email.split('@')[0]}!`);

        // Reset loading state
        this.setLoadingState(false);

        // Reset form
        this.form.reset();
        this.validator.clearErrors();

        // Simulate redirect after 2 seconds
        setTimeout(() => {
            console.log('Redirecting to dashboard...');
            // window.location.href = '/dashboard';
        }, 2000);
    }

    /**
     * Set loading state on button
     * @param {boolean} isLoading - Is loading
     */
    setLoadingState(isLoading) {
        this.submitButton.classList.toggle('loading', isLoading);
        this.submitButton.disabled = isLoading;
        
        if (isLoading) {
            this.submitButton.setAttribute('aria-busy', 'true');
            this.submitButton.setAttribute('aria-label', 'Signing in...');
        } else {
            this.submitButton.setAttribute('aria-busy', 'false');
            this.submitButton.setAttribute('aria-label', 'Sign in to your account');
        }
    }

    /**
     * Load saved credentials from localStorage
     */
    loadSavedCredentials() {
        const savedEmail = localStorage.getItem('savedEmail');
        const rememberMe = localStorage.getItem('rememberMe') === 'true';

        if (savedEmail && rememberMe) {
            this.emailField.value = savedEmail;
            this.rememberMeCheckbox.checked = true;
            this.emailField.classList.add('success');
        }
    }

    /**
     * Setup forgot password link
     */
    setupForgotPasswordLink() {
        const forgotLink = this.form.querySelector('.forgot-password-link');
        forgotLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.toastManager.success('Password reset email sent to your email address');
        });
    }

    /**
     * Setup social login buttons
     */
    setupSocialLogin() {
        const socialButtons = this.form.querySelectorAll('.btn-social');
        socialButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const provider = button.textContent.trim();
                this.setLoadingState(true);

                setTimeout(() => {
                    this.setLoadingState(false);
                    this.toastManager.success(`Signing in with ${provider}...`);
                    console.log(`Redirecting to ${provider} OAuth...`);
                }, 1000);
            });
        });
    }

    /**
     * Setup sign up link
     */
    setupSignUpLink() {
        const signUpLink = this.form.querySelector('.signup-link a');
        signUpLink.addEventListener('click', (e) => {
            e.preventDefault();
            this.toastManager.success('Redirecting to sign up page...');
            console.log('Redirecting to /signup');
        });
    }
}

// ============================================
// Keyboard Navigation
// ============================================

/**
 * Manages keyboard navigation and shortcuts
 */
class KeyboardNavigation {
    constructor() {
        this.init();
    }

    init() {
        document.addEventListener('keydown', (e) => this.handleKeydown(e));
    }

    /**
     * Handle keyboard shortcuts
     * @param {event} e - Keyboard event
     */
    handleKeydown(e) {
        // Ctrl/Cmd + K for theme toggle
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const themeToggle = document.querySelector('.theme-toggle');
            themeToggle.click();
        }

        // Enter on password field to submit (if form is valid)
        if (e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement?.id === 'password') {
                e.preventDefault();
                const form = document.getElementById('loginForm');
                form.dispatchEvent(new Event('submit'));
            }
        }
    }
}

// ============================================
// Animation Observer
// ============================================

/**
 * Handles scroll and intersection animations
 */
class AnimationObserver {
    constructor() {
        this.init();
    }

    init() {
        // Create intersection observer for fade-in animations
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });

        // Observe all elements with fade-in animation
        document.querySelectorAll('.form-group, .btn').forEach(el => {
            observer.observe(el);
        });
    }
}

// ============================================
// Accessibility Enhancements
// ============================================

/**
 * Manages accessibility features
 */
class AccessibilityManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupAriaLabels();
        this.setupAriaDescribedBy();
        this.setupScreenReaderAnnouncements();
    }

    /**
     * Setup ARIA labels for better accessibility
     */
    setupAriaLabels() {
        const elements = {
            'loginForm': 'Login form',
            'email': 'Email address input',
            'password': 'Password input',
        };

        Object.entries(elements).forEach(([id, label]) => {
            const el = document.getElementById(id);
            if (el && !el.getAttribute('aria-label')) {
                el.setAttribute('aria-label', label);
            }
        });
    }

    /**
     * Setup ARIA described-by for error messages
     */
    setupAriaDescribedBy() {
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => {
            const errorElement = input.closest('.input-wrapper')?.querySelector('.input-error');
            if (errorElement) {
                input.setAttribute('aria-describedby', errorElement.id || `${input.id}-error`);
            }
        });
    }

    /**
     * Setup screen reader announcements
     */
    setupScreenReaderAnnouncements() {
        const announcer = document.createElement('div');
        announcer.setAttribute('aria-live', 'polite');
        announcer.setAttribute('aria-atomic', 'true');
        announcer.className = 'sr-only';
        document.body.appendChild(announcer);
    }
}

// ============================================
// Performance Optimization
// ============================================

/**
 * Manages performance optimizations
 */
class PerformanceOptimizer {
    constructor() {
        this.init();
    }

    init() {
        this.lazyLoadImages();
        this.optimizeCSSAnimations();
    }

    /**
     * Lazy load images
     */
    lazyLoadImages() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    /**
     * Optimize CSS animations based on system preferences
     */
    optimizeCSSAnimations() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        
        if (prefersReducedMotion.matches) {
            document.documentElement.style.setProperty('--transition-fast', '0ms');
            document.documentElement.style.setProperty('--transition-base', '0ms');
            document.documentElement.style.setProperty('--transition-slow', '0ms');
        }
    }
}

// ============================================
// Main Initialization
// ============================================

/**
 * Initialize all components when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers and handlers
    const themeManager = new ThemeManager();
    const passwordToggle = new PasswordToggle();
    const loginFormHandler = new LoginFormHandler();
    const keyboardNavigation = new KeyboardNavigation();
    const animationObserver = new AnimationObserver();
    const accessibilityManager = new AccessibilityManager();
    const performanceOptimizer = new PerformanceOptimizer();

    console.log('✓ Login page initialized successfully');
});

// ============================================
// Service Worker Registration (Optional)
// ============================================

/**
 * Register service worker for PWA support (optional)
 */
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable PWA support
        // navigator.serviceWorker.register('/sw.js').catch(err => {
        //     console.log('Service Worker registration failed:', err);
        // });
    });
}
