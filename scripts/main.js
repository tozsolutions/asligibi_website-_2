/**
 * Aslı Gibi Website - Main JavaScript
 * Modern, interactive functionality for the website
 * Author: TOZSolutions
 * Version: 1.0.0
 */

// ===== GLOBAL VARIABLES =====
const CONFIG = {
    animationDuration: 300,
    scrollOffset: 80,
    debounceDelay: 100,
    emailPattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    phonePattern: /^[\+]?[1-9][\d]{0,15}$/
};

// ===== UTILITY FUNCTIONS =====
const Utils = {
    // Debounce function for performance optimization
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // Throttle function for scroll events
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        }
    },

    // Check if element is in viewport
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },

    // Smooth scroll to element
    scrollToElement: function(element, offset = CONFIG.scrollOffset) {
        const elementPosition = element.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - offset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    },

    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        `;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    },

    // Format phone number
    formatPhoneNumber: function(value) {
        const phoneNumber = value.replace(/\D/g, '');
        const phoneNumberLength = phoneNumber.length;
        
        if (phoneNumberLength < 4) return phoneNumber;
        if (phoneNumberLength < 7) {
            return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
        }
        return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6, 10)}`;
    }
};

// ===== NAVIGATION FUNCTIONALITY =====
const Navigation = {
    init: function() {
        this.setupSmoothScrolling();
        this.setupActiveNavigation();
        this.setupMobileMenu();
        this.setupScrollIndicator();
    },

    setupSmoothScrolling: function() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    Utils.scrollToElement(target);
                    
                    // Close mobile menu if open
                    const navbarCollapse = document.querySelector('.navbar-collapse');
                    if (navbarCollapse.classList.contains('show')) {
                        const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                        bsCollapse.hide();
                    }
                }
            });
        });
    },

    setupActiveNavigation: function() {
        const sections = document.querySelectorAll('section[id]');
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');

        const setActiveNav = Utils.throttle(() => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.getBoundingClientRect().top;
                if (sectionTop <= CONFIG.scrollOffset + 50) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        }, 100);

        window.addEventListener('scroll', setActiveNav);
    },

    setupMobileMenu: function() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');

        if (navbarToggler && navbarCollapse) {
            navbarToggler.addEventListener('click', function() {
                this.classList.toggle('active');
            });
        }
    },

    setupScrollIndicator: function() {
        const scrollIndicator = document.createElement('div');
        scrollIndicator.className = 'scroll-indicator';
        document.body.appendChild(scrollIndicator);

        const updateScrollIndicator = Utils.throttle(() => {
            const scrollTop = window.pageYOffset;
            const documentHeight = document.documentElement.scrollHeight - window.innerHeight;
            const scrollPercentage = (scrollTop / documentHeight) * 100;
            scrollIndicator.style.width = scrollPercentage + '%';
        }, 10);

        window.addEventListener('scroll', updateScrollIndicator);
    }
};

// ===== ANIMATION FUNCTIONALITY =====
const Animations = {
    init: function() {
        this.setupScrollAnimations();
        this.setupCounterAnimations();
        this.setupParallaxEffect();
    },

    setupScrollAnimations: function() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-on-scroll');
                }
            });
        }, observerOptions);

        // Observe elements for animation
        document.querySelectorAll('.card, .service-card, .contact-info').forEach((el, index) => {
            el.style.animationDelay = `${index * 0.1}s`;
            observer.observe(el);
        });
    },

    setupCounterAnimations: function() {
        const counters = document.querySelectorAll('[data-counter]');
        
        const animateCounter = (counter) => {
            const target = parseInt(counter.getAttribute('data-counter'));
            const duration = 2000;
            const increment = target / (duration / 16);
            let current = 0;

            const updateCounter = () => {
                current += increment;
                if (current < target) {
                    counter.textContent = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            updateCounter();
        };

        const counterObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    counterObserver.unobserve(entry.target);
                }
            });
        });

        counters.forEach(counter => counterObserver.observe(counter));
    },

    setupParallaxEffect: function() {
        const parallaxElements = document.querySelectorAll('[data-parallax]');
        
        const updateParallax = Utils.throttle(() => {
            const scrolled = window.pageYOffset;
            
            parallaxElements.forEach(element => {
                const rate = scrolled * -0.5;
                element.style.transform = `translateY(${rate}px)`;
            });
        }, 10);

        if (parallaxElements.length > 0) {
            window.addEventListener('scroll', updateParallax);
        }
    }
};

// ===== FORM FUNCTIONALITY =====
const Forms = {
    init: function() {
        this.setupContactForm();
        this.setupFormValidation();
        this.setupFormEnhancements();
    },

    setupContactForm: function() {
        const contactForm = document.getElementById('contactForm');
        
        if (contactForm) {
            contactForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = new FormData(contactForm);
                const formObject = Object.fromEntries(formData.entries());
                
                // Validate form
                if (this.validateContactForm(formObject)) {
                    await this.submitContactForm(formObject);
                }
            });
        }
    },

    validateContactForm: function(data) {
        const errors = [];

        // Name validation
        if (!data.name || data.name.trim().length < 2) {
            errors.push('Ad soyad en az 2 karakter olmalıdır.');
        }

        // Email validation
        if (!data.email || !CONFIG.emailPattern.test(data.email)) {
            errors.push('Geçerli bir e-posta adresi giriniz.');
        }

        // Subject validation
        if (!data.subject || data.subject.trim().length < 5) {
            errors.push('Konu en az 5 karakter olmalıdır.');
        }

        // Message validation
        if (!data.message || data.message.trim().length < 10) {
            errors.push('Mesaj en az 10 karakter olmalıdır.');
        }

        if (errors.length > 0) {
            Utils.showNotification(errors.join('<br>'), 'danger');
            return false;
        }

        return true;
    },

    submitContactForm: async function(data) {
        const submitButton = document.querySelector('#contactForm button[type="submit"]');
        const originalText = submitButton.innerHTML;
        
        try {
            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="loading"></span> Gönderiliyor...';

            // Simulate API call (replace with actual endpoint)
            await new Promise(resolve => setTimeout(resolve, 2000));

            // Success
            Utils.showNotification('Mesajınız başarıyla gönderildi! En kısa sürede size dönüş yapacağız.', 'success');
            document.getElementById('contactForm').reset();

        } catch (error) {
            console.error('Form submission error:', error);
            Utils.showNotification('Mesaj gönderilirken bir hata oluştu. Lütfen tekrar deneyiniz.', 'danger');
        } finally {
            // Reset button state
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
        }
    },

    setupFormValidation: function() {
        const inputs = document.querySelectorAll('input, textarea');
        
        inputs.forEach(input => {
            input.addEventListener('blur', (e) => {
                this.validateField(e.target);
            });

            input.addEventListener('input', (e) => {
                this.clearFieldError(e.target);
                
                // Format phone number if applicable
                if (e.target.type === 'tel') {
                    e.target.value = Utils.formatPhoneNumber(e.target.value);
                }
            });
        });
    },

    validateField: function(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        switch (field.type) {
            case 'email':
                isValid = CONFIG.emailPattern.test(value);
                errorMessage = 'Geçerli bir e-posta adresi giriniz.';
                break;
            case 'tel':
                isValid = CONFIG.phonePattern.test(value.replace(/\D/g, ''));
                errorMessage = 'Geçerli bir telefon numarası giriniz.';
                break;
            default:
                if (field.hasAttribute('required')) {
                    isValid = value.length > 0;
                    errorMessage = 'Bu alan zorunludur.';
                }
        }

        if (!isValid) {
            this.showFieldError(field, errorMessage);
        } else {
            this.clearFieldError(field);
        }

        return isValid;
    },

    showFieldError: function(field, message) {
        field.classList.add('is-invalid');
        
        let feedback = field.parentNode.querySelector('.invalid-feedback');
        if (!feedback) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            field.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    },

    clearFieldError: function(field) {
        field.classList.remove('is-invalid');
        const feedback = field.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    },

    setupFormEnhancements: function() {
        // Auto-resize textareas
        document.querySelectorAll('textarea').forEach(textarea => {
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        });

        // Add floating labels effect
        document.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('focus', function() {
                this.parentNode.classList.add('focused');
            });

            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentNode.classList.remove('focused');
                }
            });

            // Initialize focused state for pre-filled inputs
            if (input.value) {
                input.parentNode.classList.add('focused');
            }
        });
    }
};

// ===== PERFORMANCE OPTIMIZATION =====
const Performance = {
    init: function() {
        this.setupLazyLoading();
        this.setupImageOptimization();
        this.setupCacheManagement();
    },

    setupLazyLoading: function() {
        const images = document.querySelectorAll('img[data-src]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                });
            });

            images.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback for older browsers
            images.forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
            });
        }
    },

    setupImageOptimization: function() {
        // Add loading attribute to images
        document.querySelectorAll('img').forEach(img => {
            if (!img.hasAttribute('loading')) {
                img.setAttribute('loading', 'lazy');
            }
        });
    },

    setupCacheManagement: function() {
        // Service worker registration for caching
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
};

// ===== ACCESSIBILITY FEATURES =====
const Accessibility = {
    init: function() {
        this.setupKeyboardNavigation();
        this.setupFocusManagement();
        this.setupARIALabels();
    },

    setupKeyboardNavigation: function() {
        // Skip to main content link
        const skipLink = document.createElement('a');
        skipLink.href = '#main';
        skipLink.textContent = 'Ana içeriğe geç';
        skipLink.className = 'skip-link visually-hidden-focusable';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            z-index: 9999;
            padding: 8px 16px;
            background: #000;
            color: #fff;
            text-decoration: none;
            border-radius: 4px;
        `;
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Escape key functionality
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                // Close modals, menus, etc.
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    const bsModal = bootstrap.Modal.getInstance(openModal);
                    bsModal.hide();
                }
            }
        });
    },

    setupFocusManagement: function() {
        // Focus trap for modals
        const focusableElements = 'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])';
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                const modal = document.querySelector('.modal.show');
                if (modal) {
                    const focusableContent = modal.querySelectorAll(focusableElements);
                    const firstFocusable = focusableContent[0];
                    const lastFocusable = focusableContent[focusableContent.length - 1];

                    if (e.shiftKey) {
                        if (document.activeElement === firstFocusable) {
                            lastFocusable.focus();
                            e.preventDefault();
                        }
                    } else {
                        if (document.activeElement === lastFocusable) {
                            firstFocusable.focus();
                            e.preventDefault();
                        }
                    }
                }
            }
        });
    },

    setupARIALabels: function() {
        // Add ARIA labels to interactive elements
        document.querySelectorAll('button:not([aria-label])').forEach(button => {
            const text = button.textContent.trim();
            if (text) {
                button.setAttribute('aria-label', text);
            }
        });

        // Add role attributes
        document.querySelectorAll('.card').forEach(card => {
            card.setAttribute('role', 'article');
        });
    }
};

// ===== THEME MANAGEMENT =====
const Theme = {
    init: function() {
        this.setupThemeToggle();
        this.loadSavedTheme();
    },

    setupThemeToggle: function() {
        const themeToggle = document.createElement('button');
        themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        themeToggle.className = 'btn btn-outline-primary position-fixed';
        themeToggle.style.cssText = `
            bottom: 20px;
            left: 20px;
            z-index: 9999;
            width: 50px;
            height: 50px;
            border-radius: 50%;
        `;
        themeToggle.setAttribute('aria-label', 'Toggle dark mode');

        themeToggle.addEventListener('click', () => {
            this.toggleTheme();
        });

        document.body.appendChild(themeToggle);
    },

    toggleTheme: function() {
        const currentTheme = document.body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);

        const themeToggle = document.querySelector('button[aria-label="Toggle dark mode"]');
        const icon = themeToggle.querySelector('i');
        icon.className = newTheme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    },

    loadSavedTheme: function() {
        const savedTheme = localStorage.getItem('theme') || 'light';
        document.body.setAttribute('data-theme', savedTheme);
    }
};

// ===== MAIN INITIALIZATION =====
class WebsiteApp {
    constructor() {
        this.init();
    }

    init() {
        // Wait for DOM to be fully loaded
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.initializeModules());
        } else {
            this.initializeModules();
        }
    }

    initializeModules() {
        try {
            Navigation.init();
            Animations.init();
            Forms.init();
            Performance.init();
            Accessibility.init();
            Theme.init();

            // Custom initialization
            this.setupCustomFeatures();
            
            console.log('Website initialized successfully');
        } catch (error) {
            console.error('Error initializing website:', error);
        }
    }

    setupCustomFeatures() {
        // Add any custom features here
        this.setupBackToTop();
        this.setupTypingEffect();
        this.setupTooltips();
    }

    setupBackToTop() {
        const backToTop = document.createElement('button');
        backToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
        backToTop.className = 'btn btn-primary position-fixed';
        backToTop.style.cssText = `
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        `;
        backToTop.setAttribute('aria-label', 'Back to top');

        const toggleBackToTop = Utils.throttle(() => {
            if (window.pageYOffset > 300) {
                backToTop.style.opacity = '1';
                backToTop.style.visibility = 'visible';
            } else {
                backToTop.style.opacity = '0';
                backToTop.style.visibility = 'hidden';
            }
        }, 100);

        backToTop.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        window.addEventListener('scroll', toggleBackToTop);
        document.body.appendChild(backToTop);
    }

    setupTypingEffect() {
        const typingElements = document.querySelectorAll('[data-typing]');
        
        typingElements.forEach(element => {
            const text = element.textContent;
            const speed = parseInt(element.dataset.typing) || 100;
            
            element.textContent = '';
            let i = 0;
            
            const typeWriter = () => {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, speed);
                }
            };
            
            // Start typing when element is visible
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        typeWriter();
                        observer.unobserve(entry.target);
                    }
                });
            });
            
            observer.observe(element);
        });
    }

    setupTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
}

// ===== START APPLICATION =====
const app = new WebsiteApp();

// ===== EXPORT FOR MODULE USAGE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        WebsiteApp,
        Utils,
        Navigation,
        Animations,
        Forms,
        Performance,
        Accessibility,
        Theme
    };
}