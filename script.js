// ========== Smooth Scroll Navigation ==========
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
            // Close mobile menu if open
            closeMenu();
        }
    });
});

// ========== Mobile Menu Toggle ==========
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');

menuToggle.addEventListener('click', () => {
    menuToggle.classList.toggle('active');
    navMenu.classList.toggle('active');
});

// Close menu when a link is clicked
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        closeMenu();
    });
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.navbar-container')) {
        closeMenu();
    }
});

function closeMenu() {
    menuToggle.classList.remove('active');
    navMenu.classList.remove('active');
}

// ========== Contact Form Handling ==========
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');

contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = new FormData(contactForm);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        subject: formData.get('subject'),
        message: formData.get('message')
    };

    // Validate email format
    if (!isValidEmail(data.email)) {
        showFormMessage('Please enter a valid email address.', 'error');
        return;
    }

    // Validate message length
    if (data.message.trim().length < 10) {
        showFormMessage('Message must be at least 10 characters long.', 'error');
        return;
    }

    try {
        // Simulate form submission (in a real app, send to a backend)
        showFormMessage('Sending your message...', 'info');
        
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Success response
        showFormMessage('✓ Message sent successfully! I\'ll get back to you soon.', 'success');
        contactForm.reset();

        // Clear success message after 5 seconds
        setTimeout(() => {
            formMessage.textContent = '';
            formMessage.className = 'form-message';
        }, 5000);

    } catch (error) {
        showFormMessage('Failed to send message. Please try again later.', 'error');
    }
});

function showFormMessage(message, type) {
    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ========== Intersection Observer for Animations ==========
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe all project cards and about content
document.querySelectorAll('.project-card, .about-content').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ========== Navbar Background on Scroll ==========
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.15)';
    } else {
        navbar.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
    }
});

// ========== Active Navigation Link Indicator ==========
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (pageYOffset >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Add active link styling
const style = document.createElement('style');
style.textContent = `
    .nav-link.active {
        color: var(--primary-color);
    }
    
    .nav-link.active::after {
        width: 100%;
    }
`;
document.head.appendChild(style);

// ========== Project Card Click Handlers ==========
document.querySelectorAll('.project-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        // In a real app, this would navigate to the project details page
        const projectTitle = link.closest('.project-card').querySelector('h3').textContent;
        alert(`Navigating to: ${projectTitle}\n\nIn a real app, this would open the project details page.`);
    });
});

// ========== Scroll Progress Indicator ==========
function updateScrollProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;

    // You can use this value to create a progress bar
    // Example: progressBar.style.width = scrollPercent + '%';
}

window.addEventListener('scroll', updateScrollProgress);

// ========== Keyboard Navigation Support ==========
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeMenu();
    }
});

// ========== Page Load Animation ==========
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});

// ========== Performance: Debounce Scroll Events ==========
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Debounced scroll handler
const debouncedScroll = debounce(() => {
    updateScrollProgress();
}, 100);

window.addEventListener('scroll', debouncedScroll);

// ========== Back to Top Button (Optional Enhancement) ==========
function createBackToTopButton() {
    const button = document.createElement('button');
    button.id = 'backToTop';
    button.innerHTML = '↑';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        font-size: 20px;
        font-weight: bold;
        display: none;
        z-index: 999;
        box-shadow: var(--shadow-lg);
        transition: all 0.3s ease;
    `;

    document.body.appendChild(button);

    // Show button when scrolled down
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            button.style.display = 'flex';
            button.style.alignItems = 'center';
            button.style.justifyContent = 'center';
        } else {
            button.style.display = 'none';
        }
    });

    // Scroll to top on click
    button.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Hover effect
    button.addEventListener('mouseenter', () => {
        button.style.transform = 'translateY(-5px)';
    });

    button.addEventListener('mouseleave', () => {
        button.style.transform = 'translateY(0)';
    });
}

createBackToTopButton();

// ========== Console Welcome Message ==========
console.log('%c🎉 Welcome to John Doe\'s Portfolio!', 'font-size: 20px; color: #667eea; font-weight: bold;');
console.log('%cFeel free to explore my projects and get in touch!', 'font-size: 14px; color: #764ba2;');
