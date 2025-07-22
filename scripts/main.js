/**
 * Aslı Gibi Website - Main JavaScript
 * Modern, interactive functionality for the website
 * Author: TOZSolutions
 * Version: 1.0.0
 */

// Configuration object
const CONFIG = {
    animationDuration: 300,
    scrollOffset: 80,
    debounceDelay: 100,
    emailPattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    phonePattern: /^[\+]?[1-9][\d]{0,15}$/
};

// Utility functions
class Utils {
    static debounce(func, wait) {
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

    static throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    static isValidEmail(email) {
        return CONFIG.emailPattern.test(email);
    }

    static isValidPhone(phone) {
        return CONFIG.phonePattern.test(phone);
    }

    static sanitizeInput(str) {
        const div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    static showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    static async animateElement(element, animationClass, duration = 1000) {
        return new Promise((resolve) => {
            element.classList.add(animationClass);
            setTimeout(() => {
                element.classList.remove(animationClass);
                resolve();
            }, duration);
        });
    }
}

// Navigation functionality
class Navigation {
    constructor() {
        this.navbar = document.querySelector('.navbar');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.init();
    }

    init() {
        this.handleScroll();
        this.handleSmoothScrolling();
        this.handleActiveSection();
        this.handleMobileMenu();
    }

    handleScroll() {
        const scrollHandler = Utils.throttle(() => {
            if (window.scrollY > 50) {
                this.navbar.classList.add('scrolled');
            } else {
                this.navbar.classList.remove('scrolled');
            }
        }, 10);

        window.addEventListener('scroll', scrollHandler);
    }

    handleSmoothScrolling() {
        this.navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                if (href.startsWith('#')) {
                    e.preventDefault();
                    const target = document.querySelector(href);
                    if (target) {
                        const offsetTop = target.offsetTop - CONFIG.scrollOffset;
                        window.scrollTo({
                            top: offsetTop,
                            behavior: 'smooth'
                        });
                    }
                }
            });
        });
    }

    handleActiveSection() {
        const sections = document.querySelectorAll('section[id]');
        const scrollHandler = Utils.throttle(() => {
            const scrollPos = window.scrollY + CONFIG.scrollOffset + 100;
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.offsetHeight;
                const sectionId = section.getAttribute('id');
                
                if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
                    this.navLinks.forEach(link => {
                        link.classList.remove('active');
                        if (link.getAttribute('href') === `#${sectionId}`) {
                            link.classList.add('active');
                        }
                    });
                }
            });
        }, 50);

        window.addEventListener('scroll', scrollHandler);
    }

    handleMobileMenu() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            this.navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (navbarCollapse.classList.contains('show')) {
                        navbarToggler.click();
                    }
                });
            });
        }
    }
}

// Animation functionality
class Animations {
    constructor() {
        this.observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        this.init();
    }

    init() {
        this.setupIntersectionObserver();
        this.handleHoverAnimations();
        this.handleScrollAnimations();
    }

    setupIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animate-in');
                        observer.unobserve(entry.target);
                    }
                });
            }, this.observerOptions);

            // Observe elements that should animate on scroll
            const animateElements = document.querySelectorAll(
                '.feature-card, .service-card, .contact-form, .hero-card'
            );
            animateElements.forEach(el => observer.observe(el));
        }
    }

    handleHoverAnimations() {
        const cards = document.querySelectorAll('.feature-card, .service-card');
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-10px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    handleScrollAnimations() {
        const parallaxElements = document.querySelectorAll('.hero-section::before');
        const scrollHandler = Utils.throttle(() => {
            const scrolled = window.pageYOffset;
            parallaxElements.forEach(element => {
                const rate = scrolled * -0.5;
                element.style.transform = `translateY(${rate}px)`;
            });
        }, 16);

        window.addEventListener('scroll', scrollHandler);
    }
}

// Form functionality
class Forms {
    constructor() {
        this.contactForm = document.getElementById('contactForm');
        this.init();
    }

    init() {
        if (this.contactForm) {
            this.handleFormSubmission();
            this.handleRealTimeValidation();
        }
    }

    handleFormSubmission() {
        this.contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(this.contactForm);
            const data = Object.fromEntries(formData.entries());
            
            // Validate form data
            if (!this.validateForm(data)) {
                return;
            }

            // Show loading state
            const submitBtn = this.contactForm.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Gönderiliyor...';
            submitBtn.disabled = true;

            try {
                // Simulate form submission (replace with actual endpoint)
                await this.simulateFormSubmission(data);
                
                Utils.showNotification('Mesajınız başarıyla gönderildi!', 'success');
                this.contactForm.reset();
                
            } catch (error) {
                Utils.showNotification('Mesaj gönderilemedi. Lütfen tekrar deneyin.', 'danger');
                console.error('Form submission error:', error);
                
            } finally {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }

    handleRealTimeValidation() {
        const inputs = this.contactForm.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            const debouncedValidation = Utils.debounce(() => {
                this.validateField(input);
            }, CONFIG.debounceDelay);
            
            input.addEventListener('input', debouncedValidation);
            input.addEventListener('blur', () => this.validateField(input));
        });
    }

    validateField(field) {
        const value = field.value.trim();
        const fieldName = field.name;
        let isValid = true;
        let message = '';

        // Remove existing validation classes
        field.classList.remove('is-valid', 'is-invalid');
        
        // Remove existing feedback
        const existingFeedback = field.parentNode.querySelector('.invalid-feedback');
        if (existingFeedback) {
            existingFeedback.remove();
        }

        // Validate based on field type
        switch (fieldName) {
            case 'name':
                if (value.length < 2) {
                    isValid = false;
                    message = 'Ad soyad en az 2 karakter olmalıdır.';
                }
                break;
                
            case 'email':
                if (!Utils.isValidEmail(value)) {
                    isValid = false;
                    message = 'Geçerli bir e-posta adresi giriniz.';
                }
                break;
                
            case 'subject':
                if (value.length < 5) {
                    isValid = false;
                    message = 'Konu en az 5 karakter olmalıdır.';
                }
                break;
                
            case 'message':
                if (value.length < 10) {
                    isValid = false;
                    message = 'Mesaj en az 10 karakter olmalıdır.';
                }
                break;
        }

        // Apply validation styles
        if (value && !isValid) {
            field.classList.add('is-invalid');
            const feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            feedback.textContent = message;
            field.parentNode.appendChild(feedback);
        } else if (value) {
            field.classList.add('is-valid');
        }

        return isValid;
    }

    validateForm(data) {
        let isValid = true;
        
        // Validate all fields
        Object.keys(data).forEach(key => {
            const field = this.contactForm.querySelector(`[name="${key}"]`);
            if (field && !this.validateField(field)) {
                isValid = false;
            }
        });

        // Check required fields
        const requiredFields = ['name', 'email', 'subject', 'message'];
        requiredFields.forEach(fieldName => {
            if (!data[fieldName] || data[fieldName].trim() === '') {
                isValid = false;
                const field = this.contactForm.querySelector(`[name="${fieldName}"]`);
                if (field) {
                    field.classList.add('is-invalid');
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = 'Bu alan zorunludur.';
                    field.parentNode.appendChild(feedback);
                }
            }
        });

        return isValid;
    }

    async simulateFormSubmission(data) {
        // Simulate API call delay
        return new Promise((resolve) => {
            setTimeout(() => {
                console.log('Form submitted with data:', data);
                resolve();
            }, 2000);
        });
    }
}

// Performance optimization
class Performance {
    constructor() {
        this.init();
    }

    init() {
        this.lazyLoadImages();
        this.preloadCriticalResources();
        this.setupServiceWorker();
    }

    lazyLoadImages() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        imageObserver.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }

    preloadCriticalResources() {
        const criticalResources = [
            'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
            'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
        ];

        criticalResources.forEach(resource => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'style';
            link.href = resource;
            document.head.appendChild(link);
        });
    }

    setupServiceWorker() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/sw.js')
                    .then(registration => {
                        console.log('SW registered: ', registration);
                    })
                    .catch(registrationError => {
                        console.log('SW registration failed: ', registrationError);
                    });
            });
        }
    }
}

// Accessibility features
class Accessibility {
    constructor() {
        this.init();
    }

    init() {
        this.handleKeyboardNavigation();
        this.setupAriaLabels();
        this.handleFocusManagement();
        this.setupReducedMotion();
    }

    handleKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', () => {
            document.body.classList.remove('keyboard-navigation');
        });

        // Skip to main content
        const skipLink = document.createElement('a');
        skipLink.href = '#main';
        skipLink.className = 'skip-link position-absolute';
        skipLink.textContent = 'Ana içeriğe geç';
        skipLink.style.cssText = 'top: -40px; left: 6px; background: #000; color: #fff; padding: 8px; z-index: 9999; text-decoration: none;';
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });
        
        document.body.insertBefore(skipLink, document.body.firstChild);
    }

    setupAriaLabels() {
        // Add ARIA labels to interactive elements
        const buttons = document.querySelectorAll('button:not([aria-label])');
        buttons.forEach(button => {
            if (!button.getAttribute('aria-label')) {
                const text = button.textContent.trim() || button.title || 'Button';
                button.setAttribute('aria-label', text);
            }
        });

        // Add ARIA labels to form fields
        const formFields = document.querySelectorAll('input, textarea, select');
        formFields.forEach(field => {
            const label = document.querySelector(`label[for="${field.id}"]`);
            if (label && !field.getAttribute('aria-label')) {
                field.setAttribute('aria-label', label.textContent.trim());
            }
        });
    }

    handleFocusManagement() {
        // Trap focus in modals
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.addEventListener('shown.bs.modal', () => {
                const focusableElements = modal.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                if (focusableElements.length > 0) {
                    focusableElements[0].focus();
                }
            });
        });
    }

    setupReducedMotion() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.style.setProperty('--transition-base', 'none');
            document.documentElement.style.setProperty('--transition-fast', 'none');
        }
    }
}

// Theme management
class Theme {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        this.applyTheme();
        this.createThemeToggle();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.currentTheme);
        
        // Update theme color meta tag
        const themeColorMeta = document.querySelector('meta[name="theme-color"]');
        if (themeColorMeta) {
            themeColorMeta.content = this.currentTheme === 'dark' ? '#212529' : '#ffffff';
        }
    }

    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', this.currentTheme);
        this.applyTheme();
        
        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('themeChanged', { 
            detail: { theme: this.currentTheme } 
        }));
    }

    createThemeToggle() {
        const themeToggle = document.createElement('button');
        themeToggle.className = 'btn btn-outline-secondary theme-toggle position-fixed';
        themeToggle.style.cssText = 'bottom: 20px; left: 20px; z-index: 9999; border-radius: 50%; width: 50px; height: 50px;';
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        themeToggle.setAttribute('aria-label', 'Tema değiştir');
        
        themeToggle.addEventListener('click', () => {
            this.toggleTheme();
            themeToggle.innerHTML = this.currentTheme === 'dark' ? 
                '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
        });
        
        document.body.appendChild(themeToggle);
    }
}

// Main application class
class WebsiteApp {
    constructor() {
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeComponents());
        } else {
            this.initializeComponents();
        }
    }

    initializeComponents() {
        try {
            // Initialize all components
            this.navigation = new Navigation();
            this.animations = new Animations();
            this.forms = new Forms();
            this.performance = new Performance();
            this.accessibility = new Accessibility();
            this.theme = new Theme();

            // Add loading complete class
            document.body.classList.add('loaded');
            
            // Log successful initialization
            console.log('🚀 Aslı Gibi Website initialized successfully!');
            
        } catch (error) {
            console.error('❌ Error initializing website:', error);
        }
    }
}

// Initialize the application
const app = new WebsiteApp();