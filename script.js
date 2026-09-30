/**
 * About Page JavaScript
 * Handles interactivity and animations for the about page
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initializeNavigation();
    initializeScrollAnimations();
    initializeValueCards();
    initializeStatistics();
    initializeContactButton();
});

/**
 * Navigation functionality
 */
function initializeNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
}

/**
 * Scroll-based animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe team members and stats
    document.querySelectorAll('.team-member, .stat, .value-card').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Add interactivity to value cards
 */
function initializeValueCards() {
    const valueCards = document.querySelectorAll('.value-card');
    
    valueCards.forEach(card => {
        // Add hover effect
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.boxShadow = '0 10px 25px rgba(37, 99, 235, 0.2)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = 'none';
        });

        // Add click feedback
        card.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            console.log(`Selected value: ${value}`);
            showValueDetail(value);
        });
    });
}

/**
 * Show value card details (can be extended with modal or tooltip)
 */
function showValueDetail(value) {
    const details = {
        integrity: 'We operate with honesty and transparency in all our dealings, building trust with our customers and partners.',
        innovation: 'We embrace creativity and continuously improve our offerings to stay ahead of the curve.',
        excellence: 'We strive for the highest quality in everything we do, never compromising on standards.',
        teamwork: 'We believe in collaboration and mutual support, knowing that together we achieve more.'
    };
    
    alert(`${value.charAt(0).toUpperCase() + value.slice(1)}: ${details[value]}`);
}

/**
 * Animate statistics on scroll
 */
function initializeStatistics() {
    const stats = document.querySelectorAll('.stat-number');
    let statsAnimated = false;
    
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !statsAnimated) {
                statsAnimated = true;
                stats.forEach(stat => {
                    animateCounter(stat);
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    // Observe the stats section
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
}

/**
 * Animate counter from 0 to target number
 */
function animateCounter(element) {
    const target = parseInt(element.textContent);
    const duration = 1500;
    const increment = target / (duration / 16); // 16ms per frame (60fps)
    let current = 0;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = element.textContent; // Keep original format
            clearInterval(timer);
        } else {
            const numericValue = Math.floor(current);
            element.textContent = element.textContent.replace(/\d+/g, numericValue);
        }
    }, 16);
}

/**
 * Contact button functionality
 */
function initializeContactButton() {
    const contactBtn = document.getElementById('contactBtn');
    
    if (contactBtn) {
        contactBtn.addEventListener('click', function() {
            handleContactButtonClick();
        });

        // Add hover effect
        contactBtn.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });

        contactBtn.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    }
}

/**
 * Handle contact button click
 */
function handleContactButtonClick() {
    const message = 'Thank you for your interest! We will contact you soon.';
    console.log(message);
    alert(message);
    // You can replace this with a modal or form submission
}

/**
 * Utility: Smooth scroll to section
 */
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Utility: Log page analytics (for tracking)
 */
function logPageAnalytics() {
    console.log('About page loaded');
    console.log('User agent:', navigator.userAgent);
    console.log('Timestamp:', new Date().toISOString());
}

// Log analytics on page load
logPageAnalytics();
