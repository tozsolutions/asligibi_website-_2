/**
 * Test suite for Aslı Gibi Website
 * Tests basic functionality and utilities
 */

// Mock DOM environment
const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
global.document = dom.window.document;
global.window = dom.window;
global.navigator = dom.window.navigator;

describe('Website Basic Tests', () => {
  test('should have correct page title structure', () => {
    document.title = 'Aslı Gibi - Ana Sayfa';
    expect(document.title).toContain('Aslı Gibi');
  });

  test('should create HTML elements correctly', () => {
    const div = document.createElement('div');
    div.className = 'test-element';
    div.textContent = 'Test Content';
    
    expect(div.className).toBe('test-element');
    expect(div.textContent).toBe('Test Content');
  });

  test('should handle CSS classes', () => {
    const element = document.createElement('div');
    element.classList.add('btn', 'btn-primary');
    
    expect(element.classList.contains('btn')).toBe(true);
    expect(element.classList.contains('btn-primary')).toBe(true);
  });
});

describe('Utility Functions', () => {
  test('should validate email format', () => {
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    expect(emailPattern.test('test@example.com')).toBe(true);
    expect(emailPattern.test('invalid-email')).toBe(false);
    expect(emailPattern.test('test@')).toBe(false);
  });

  test('should validate phone number format', () => {
    const phonePattern = /^[\+]?[1-9][\d]{0,15}$/;
    
    expect(phonePattern.test('1234567890')).toBe(true);
    expect(phonePattern.test('+1234567890')).toBe(true);
    expect(phonePattern.test('invalid-phone')).toBe(false);
  });

  test('should format phone numbers correctly', () => {
    const formatPhoneNumber = (value) => {
      const phoneNumber = value.replace(/\D/g, '');
      const phoneNumberLength = phoneNumber.length;
      
      if (phoneNumberLength < 4) return phoneNumber;
      if (phoneNumberLength < 7) {
        return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3)}`;
      }
      return `(${phoneNumber.slice(0, 3)}) ${phoneNumber.slice(3, 6)}-${phoneNumber.slice(6, 10)}`;
    };

    expect(formatPhoneNumber('1234567890')).toBe('(123) 456-7890');
    expect(formatPhoneNumber('123456')).toBe('(123) 456');
    expect(formatPhoneNumber('123')).toBe('123');
  });
});

describe('Form Validation', () => {
  test('should validate required fields', () => {
    const validateRequired = (value) => {
      return value && value.trim().length > 0;
    };

    expect(validateRequired('test')).toBe(true);
    expect(validateRequired('')).toBe(false);
    expect(validateRequired('   ')).toBe(false);
    expect(validateRequired(null)).toBe(false);
    expect(validateRequired(undefined)).toBe(false);
  });

  test('should validate minimum length', () => {
    const validateMinLength = (value, minLength) => {
      return value && value.trim().length >= minLength;
    };

    expect(validateMinLength('test', 3)).toBe(true);
    expect(validateMinLength('te', 3)).toBe(false);
    expect(validateMinLength('test', 5)).toBe(false);
  });
});

describe('Responsive Design', () => {
  test('should handle different screen sizes', () => {
    const getDeviceType = (width) => {
      if (width < 768) return 'mobile';
      if (width < 1024) return 'tablet';
      return 'desktop';
    };

    expect(getDeviceType(320)).toBe('mobile');
    expect(getDeviceType(768)).toBe('tablet');
    expect(getDeviceType(1024)).toBe('desktop');
    expect(getDeviceType(1920)).toBe('desktop');
  });
});

describe('Performance', () => {
  test('should debounce function calls', (done) => {
    let callCount = 0;
    
    const debounce = (func, wait) => {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    };

    const debouncedFunction = debounce(() => {
      callCount++;
    }, 50);

    // Call function multiple times quickly
    debouncedFunction();
    debouncedFunction();
    debouncedFunction();

    // Should only be called once after delay
    setTimeout(() => {
      expect(callCount).toBe(1);
      done();
    }, 100);
  });

  test('should throttle function calls', (done) => {
    let callCount = 0;
    
    const throttle = (func, limit) => {
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
    };

    const throttledFunction = throttle(() => {
      callCount++;
    }, 50);

    // Call function multiple times quickly
    throttledFunction();
    throttledFunction();
    throttledFunction();

    // Should only be called once immediately
    expect(callCount).toBe(1);
    
    setTimeout(() => {
      throttledFunction();
      expect(callCount).toBe(2);
      done();
    }, 100);
  });
});

describe('Accessibility', () => {
  test('should have proper ARIA attributes', () => {
    const button = document.createElement('button');
    button.setAttribute('aria-label', 'Close dialog');
    
    expect(button.getAttribute('aria-label')).toBe('Close dialog');
  });

  test('should support keyboard navigation', () => {
    const link = document.createElement('a');
    link.href = '#section';
    link.setAttribute('tabindex', '0');
    
    expect(link.getAttribute('tabindex')).toBe('0');
    expect(link.href).toContain('#section');
  });
});

describe('Security', () => {
  test('should sanitize user input', () => {
    const sanitizeInput = (input) => {
      return input.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
    };

    const maliciousInput = '<script>alert("xss")</script>Hello World';
    const sanitizedInput = sanitizeInput(maliciousInput);
    
    expect(sanitizedInput).toBe('Hello World');
    expect(sanitizedInput).not.toContain('<script>');
  });
});