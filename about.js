/**
 * About Page - Main JavaScript Module
 * Handles about page functionality, animations, and interactions
 */

// About Page Controller
const AboutPage = {
  // Configuration
  config: {
    animationDuration: 300,
    fadeInDuration: 500,
  },

  // Initialize the about page
  init() {
    this.setupEventListeners();
    this.loadAboutContent();
    this.initializeAnimations();
  },

  // Setup event listeners
  setupEventListeners() {
    // Listen for scroll events to trigger animations
    window.addEventListener('scroll', () => this.handleScroll());

    // Listen for DOM ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.init());
    }

    // Setup button interactions
    const ctaButtons = document.querySelectorAll('[data-about-cta]');
    ctaButtons.forEach(btn => {
      btn.addEventListener('click', (e) => this.handleCTAClick(e));
    });
  },

  // Load about page content
  loadAboutContent() {
    const aboutContent = {
      title: 'About Us',
      mission: 'Our mission is to create meaningful experiences and deliver exceptional value to our community.',
      vision: 'We envision a world where technology empowers everyone to achieve their goals.',
      values: [
        { name: 'Innovation', description: 'We continuously seek new and better ways to solve problems.' },
        { name: 'Integrity', description: 'We believe in transparency and honest communication.' },
        { name: 'Community', description: 'We foster collaboration and support one another.' },
        { name: 'Excellence', description: 'We strive for the highest quality in everything we do.' },
      ],
      team: [
        { name: 'John Smith', role: 'Founder & CEO', bio: 'Visionary leader with 10+ years of industry experience.' },
        { name: 'Sarah Johnson', role: 'CTO', bio: 'Tech pioneer passionate about building scalable solutions.' },
        { name: 'Mike Chen', role: 'Head of Design', bio: 'Creative mind focused on user-centered design.' },
        { name: 'Emily Davis', role: 'Community Manager', bio: 'Dedicated to building strong community connections.' },
      ],
    };

    this.displayAboutContent(aboutContent);
  },

  // Display about content on page
  displayAboutContent(content) {
    const container = document.getElementById('about-container');
    
    if (!container) {
      console.warn('About container not found');
      return;
    }

    // Create about sections
    const html = `
      <section class="about-hero">
        <h1>${content.title}</h1>
      </section>

      <section class="about-mission">
        <div class="content-block">
          <h2>Our Mission</h2>
          <p>${content.mission}</p>
        </div>
        <div class="content-block">
          <h2>Our Vision</h2>
          <p>${content.vision}</p>
        </div>
      </section>

      <section class="about-values">
        <h2>Our Core Values</h2>
        <div class="values-grid">
          ${content.values.map(value => `
            <div class="value-card" data-value="${value.name}">
              <h3>${value.name}</h3>
              <p>${value.description}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <section class="about-team">
        <h2>Our Team</h2>
        <div class="team-grid">
          ${content.team.map(member => `
            <div class="team-card" data-team-member="${member.name}">
              <div class="team-avatar"></div>
              <h3>${member.name}</h3>
              <p class="role">${member.role}</p>
              <p class="bio">${member.bio}</p>
            </div>
          `).join('')}
        </div>
      </section>

      <section class="about-cta">
        <h2>Get In Touch</h2>
        <button class="btn btn-primary" data-about-cta="contact">Contact Us</button>
        <button class="btn btn-secondary" data-about-cta="join">Join Our Team</button>
      </section>
    `;

    container.innerHTML = html;
    this.attachCardEventListeners();
  },

  // Attach event listeners to dynamically created cards
  attachCardEventListeners() {
    const valueCards = document.querySelectorAll('.value-card');
    valueCards.forEach(card => {
      card.addEventListener('mouseenter', () => this.highlightCard(card));
      card.addEventListener('mouseleave', () => this.unhighlightCard(card));
    });

    const teamCards = document.querySelectorAll('.team-card');
    teamCards.forEach((card, index) => {
      card.addEventListener('click', () => this.expandTeamCard(card));
      card.style.animationDelay = `${index * 0.1}s`;
    });
  },

  // Initialize fade-in animations
  initializeAnimations() {
    const elements = document.querySelectorAll('[data-animate]');
    elements.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(20px)';
      el.style.transition = `opacity ${this.config.fadeInDuration}ms, transform ${this.config.fadeInDuration}ms`;
    });

    this.triggerIntersectionObserver();
  },

  // Trigger animations on scroll
  triggerIntersectionObserver() {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.1 });

      document.querySelectorAll('[data-animate]').forEach(el => {
        observer.observe(el);
      });
    }
  },

  // Handle scroll events
  handleScroll() {
    const scrollPosition = window.scrollY;
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    parallaxElements.forEach(el => {
      const offset = scrollPosition * 0.5;
      el.style.transform = `translateY(${offset}px)`;
    });
  },

  // Highlight value card on hover
  highlightCard(card) {
    card.style.transform = 'scale(1.05)';
    card.style.boxShadow = '0 8px 16px rgba(0, 0, 0, 0.2)';
  },

  // Remove highlight from value card
  unhighlightCard(card) {
    card.style.transform = 'scale(1)';
    card.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.1)';
  },

  // Expand team card on click
  expandTeamCard(card) {
    const isExpanded = card.classList.contains('expanded');
    
    // Collapse other cards
    document.querySelectorAll('.team-card').forEach(c => {
      if (c !== card) {
        c.classList.remove('expanded');
        c.style.maxHeight = '400px';
      }
    });

    if (!isExpanded) {
      card.classList.add('expanded');
      card.style.maxHeight = '600px';
    } else {
      card.classList.remove('expanded');
      card.style.maxHeight = '400px';
    }
  },

  // Handle CTA button clicks
  handleCTAClick(event) {
    const action = event.target.getAttribute('data-about-cta');
    
    switch (action) {
      case 'contact':
        this.navigateTo('/contact');
        break;
      case 'join':
        this.navigateTo('/careers');
        break;
      default:
        console.warn(`Unknown CTA action: ${action}`);
    }
  },

  // Navigate to page
  navigateTo(path) {
    console.log(`Navigating to: ${path}`);
    // window.location.href = path; // Uncomment in production
  },
};

// Start the about page when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => AboutPage.init());
} else {
  AboutPage.init();
}

// Export for use as module (if needed)
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AboutPage;
}
