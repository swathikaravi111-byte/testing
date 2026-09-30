// Initialize the about page with interactive features
document.addEventListener('DOMContentLoaded', () => {
    initializeNavigation();
    initializeValueCards();
    initializeStatistics();
    initializeContactButton();
    initializeScrollAnimations();
});

/**
 * Initialize navigation functionality
 */
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            navLinks.forEach(l => l.classList.remove('active'));
            e.target.classList.add('active');
        });
    });

    // Update active link on scroll
    window.addEventListener('scroll', () => {
        updateActiveNavLink();
    });
}

/**
 * Update active navigation link based on scroll position
 */
function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-links a');
    
    let currentSection = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.scrollY >= sectionTop - 200) {
            currentSection = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').includes(currentSection)) {
            link.classList.add('active');
        }
    });
}

/**
 * Initialize value cards with hover and click effects
 */
function initializeValueCards() {
    const valueCards = document.querySelectorAll('.value-card');
    
    valueCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.animation = 'pulse 0.5s ease-out';
        });

        card.addEventListener('click', () => {
            const valueName = card.getAttribute('data-value');
            showValueDetail(valueName);
        });
    });
}

/**
 * Show detailed information about a value
 */
function showValueDetail(valueName) {
    const valueNames = {
        integrity: 'Integrity is the foundation of our business. We believe in being honest and transparent with our customers and team members at all times.',
        innovation: 'We constantly explore new ideas and technologies to improve our products and services.',
        excellence: 'Every detail matters. We maintain high standards in all aspects of our work.',
        teamwork: 'We accomplish more together. Our success is built on collaboration and mutual respect.'
    };

    const message = valueNames[valueName] || 'Thank you for your interest in our values!';
    console.log(`Value: ${valueName} - ${message}`);
    
    // Optional: Show a toast notification
    showNotification(`${valueName.toUpperCase()}: ${message}`);
}

/**
 * Initialize statistics with counter animation
 */
function initializeStatistics() {
    const stats = document.querySelectorAll('.stat');
    let hasAnimated = false;

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                animateStats();
            }
        });
    }, observerOptions);

    stats.forEach(stat => observer.observe(stat));
}

/**
 * Animate statistics counters
 */
function animateStats() {
    const stats = document.querySelectorAll('.stat-number');
    
    stats.forEach(stat => {
        const text = stat.textContent;
        const number = parseInt(text.replace(/\D/g, ''));
        const suffix = text.replace(/[0-9]/g, '');
        
        animateCounter(stat, number, suffix);
    });
}

/**
 * Animate a counter from 0 to target number
 */
function animateCounter(element, targetNumber, suffix) {
    let currentNumber = 0;
    const increment = Math.ceil(targetNumber / 50);
    const interval = setInterval(() => {
        currentNumber += increment;
        
        if (currentNumber >= targetNumber) {
            currentNumber = targetNumber;
            clearInterval(interval);
        }
        
        element.textContent = currentNumber + suffix;
    }, 30);
}

/**
 * Initialize contact button
 */
function initializeContactButton() {
    const contactBtn = document.getElementById('contactBtn');
    
    if (contactBtn) {
        contactBtn.addEventListener('click', () => {
            handleContactClick();
        });

        contactBtn.addEventListener('mouseover', () => {
            contactBtn.style.transform = 'scale(1.05)';
        });

        contactBtn.addEventListener('mouseout', () => {
            contactBtn.style.transform = 'scale(1)';
        });
    }
}

/**
 * Handle contact button click
 */
function handleContactClick() {
    const email = 'contact@myapp.com';
    showNotification(`Thank you for your interest! Please email us at ${email}`);
    
    // In a real application, you might navigate to a contact form
    console.log('Contact form would be displayed here');
}

/**
 * Initialize scroll animations for elements
 */
function initializeScrollAnimations() {
    const elements = document.querySelectorAll('.section, .value-card, .team-member');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.6s ease-out forwards';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    elements.forEach(element => observer.observe(element));
}

/**
 * Show a notification/toast message
 */
function showNotification(message) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: #2563eb;
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: slideInRight 0.3s ease-out;
        z-index: 1000;
        max-width: 400px;
        word-wrap: break-word;
    `;
    
    notification.textContent = message;
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Smooth scroll to section
 */
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Get page statistics
 */
function getPageStats() {
    return {
        totalSections: document.querySelectorAll('section').length,
        totalCards: document.querySelectorAll('.value-card').length,
        totalTeamMembers: document.querySelectorAll('.team-member').length,
        pageTitle: document.title,
        currentUrl: window.location.href
    };
}

// Export functions for external use if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        scrollToSection,
        getPageStats,
        showNotification
    };
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }

    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
`;
document.head.appendChild(style);

// Log initialization
console.log('About page initialized successfully');
console.log('Page stats:', getPageStats());
