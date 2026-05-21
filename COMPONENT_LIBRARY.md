# Modern Component Library Reference

## 🎨 Quick Component Guide

This is a practical reference for using the new modern design system components.

---

## 🔘 Buttons

### Primary Button
```html
<button class="modern-btn modern-btn-primary">
    <i class="fas fa-save"></i>
    <span>Save Changes</span>
</button>
```

### Secondary Button
```html
<button class="modern-btn modern-btn-secondary">
    <span>Cancel</span>
</button>
```

### Success Button
```html
<button class="modern-btn modern-btn-success">
    <i class="fas fa-check"></i>
    <span>Confirm</span>
</button>
```

### Outline Button
```html
<button class="modern-btn modern-btn-outline">
    <span>Learn More</span>
    <i class="fas fa-arrow-right"></i>
</button>
```

### Ghost Button
```html
<button class="modern-btn modern-btn-ghost">
    <i class="fas fa-times"></i>
    <span>Clear</span>
</button>
```

### Button Sizes
```html
<!-- Small -->
<button class="modern-btn modern-btn-primary modern-btn-sm">Small</button>

<!-- Default (no size class needed) -->
<button class="modern-btn modern-btn-primary">Default</button>

<!-- Large -->
<button class="modern-btn modern-btn-primary modern-btn-lg">Large</button>

<!-- Block (full width) -->
<button class="modern-btn modern-btn-primary modern-btn-block">Full Width</button>
```

### Icon Only Button
```html
<button class="modern-btn modern-btn-primary modern-btn-icon">
    <i class="fas fa-search"></i>
</button>
```

---

## 🎴 Cards

### Standard Card
```html
<div class="modern-card">
    <h3>Card Title</h3>
    <p>Card content goes here.</p>
</div>
```

### Card with Header, Body, Footer
```html
<div class="modern-card">
    <div class="modern-card-header">
        <h3 class="modern-card-title">Investment Details</h3>
    </div>
    <div class="modern-card-body">
        <p>Your investment information...</p>
    </div>
    <div class="modern-card-footer">
        <button class="modern-btn modern-btn-primary">View Details</button>
    </div>
</div>
```

### Glass Effect Card
```html
<div class="modern-card modern-card-glass">
    <p>Card with glassmorphism effect</p>
</div>
```

### Elevated Card
```html
<div class="modern-card modern-card-elevated">
    <p>Card with enhanced shadow</p>
</div>
```

### Gradient Card
```html
<div class="modern-card modern-card-gradient">
    <h3>Premium Feature</h3>
    <p>White text on gradient background</p>
</div>
```

### Hoverable Card
```html
<div class="modern-card hover-lift">
    <p>Card lifts on hover</p>
</div>
```

---

## 📝 Forms

### Form Group (Standard)
```html
<div class="modern-form-group">
    <label for="email" class="modern-form-label">Email Address</label>
    <input 
        type="email" 
        id="email" 
        name="email" 
        class="modern-form-input" 
        placeholder="your@email.com"
    >
</div>
```

### Required Field
```html
<div class="modern-form-group">
    <label for="name" class="modern-form-label modern-form-label-required">
        Full Name
    </label>
    <input 
        type="text" 
        id="name" 
        name="name" 
        class="modern-form-input" 
        required
    >
</div>
```

### Input with Icon
```html
<div class="modern-form-group">
    <label for="email" class="modern-form-label">Email</label>
    <div class="modern-input-wrapper">
        <i class="fas fa-envelope modern-input-icon"></i>
        <input 
            type="email" 
            id="email" 
            class="modern-form-input modern-input-with-icon" 
            placeholder="your@email.com"
        >
    </div>
</div>
```

### Input with Right Icon (e.g., Password Toggle)
```html
<div class="modern-form-group">
    <label for="password" class="modern-form-label">Password</label>
    <div class="modern-input-wrapper">
        <i class="fas fa-lock modern-input-icon"></i>
        <input 
            type="password" 
            id="password" 
            class="modern-form-input modern-input-with-icon modern-input-icon-right-active" 
            placeholder="Enter password"
        >
        <button type="button" class="modern-input-icon modern-input-icon-right" id="togglePassword">
            <i class="fas fa-eye"></i>
        </button>
    </div>
</div>

<script>
document.getElementById('togglePassword').addEventListener('click', function() {
    const input = document.getElementById('password');
    const icon = this.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
});
</script>
```

### Form Hint
```html
<div class="modern-form-group">
    <label for="phone" class="modern-form-label">Phone Number</label>
    <input type="tel" id="phone" class="modern-form-input">
    <div class="modern-form-hint">Format: 08012345678</div>
</div>
```

### Form Error
```html
<div class="modern-form-group">
    <label for="amount" class="modern-form-label">Amount</label>
    <input type="number" id="amount" class="modern-form-input modern-form-input-error">
    <div class="modern-form-error">
        <i class="fas fa-exclamation-circle"></i>
        <span>Amount must be at least ₦1,000</span>
    </div>
</div>
```

### Select Dropdown
```html
<div class="modern-form-group">
    <label for="bank" class="modern-form-label">Bank</label>
    <div class="modern-input-wrapper">
        <i class="fas fa-university modern-input-icon"></i>
        <select id="bank" class="modern-form-input modern-input-with-icon">
            <option value="">Select bank</option>
            <option value="gtbank">GTBank</option>
            <option value="access">Access Bank</option>
        </select>
    </div>
</div>
```

---

## 🏷️ Badges

### Status Badges
```html
<!-- Success -->
<span class="modern-badge modern-badge-success">Approved</span>

<!-- Error -->
<span class="modern-badge modern-badge-error">Rejected</span>

<!-- Warning -->
<span class="modern-badge modern-badge-warning">Pending</span>

<!-- Info -->
<span class="modern-badge modern-badge-info">Processing</span>

<!-- Primary -->
<span class="modern-badge modern-badge-primary">Featured</span>

<!-- Neutral -->
<span class="modern-badge modern-badge-neutral">Draft</span>
```

---

## 🚨 Alerts

### Success Alert
```html
<div class="modern-alert modern-alert-success">
    <div class="modern-alert-icon">
        <i class="fas fa-check-circle"></i>
    </div>
    <div class="modern-alert-content">
        <div class="modern-alert-title">Success!</div>
        <div>Your withdrawal request has been submitted.</div>
    </div>
</div>
```

### Error Alert
```html
<div class="modern-alert modern-alert-error">
    <div class="modern-alert-icon">
        <i class="fas fa-exclamation-circle"></i>
    </div>
    <div class="modern-alert-content">
        <div class="modern-alert-title">Error</div>
        <div>Invalid credentials. Please try again.</div>
    </div>
</div>
```

### Warning Alert
```html
<div class="modern-alert modern-alert-warning">
    <div class="modern-alert-icon">
        <i class="fas fa-exclamation-triangle"></i>
    </div>
    <div class="modern-alert-content">
        <div class="modern-alert-title">Warning</div>
        <div>Your session will expire in 5 minutes.</div>
    </div>
</div>
```

### Info Alert
```html
<div class="modern-alert modern-alert-info">
    <div class="modern-alert-icon">
        <i class="fas fa-info-circle"></i>
    </div>
    <div class="modern-alert-content">
        <div class="modern-alert-title">Info</div>
        <div>Withdrawals are processed within 24 hours.</div>
    </div>
</div>
```

---

## 📊 Stats & Metrics

### Stat Card
```html
<div class="modern-stat-card">
    <div class="modern-stat-icon" style="background: var(--gradient-primary);">
        <i class="fas fa-wallet"></i>
    </div>
    <div class="modern-stat-label">Total Balance</div>
    <div class="modern-stat-value">₦125,500.00</div>
    <div class="modern-stat-change modern-stat-change-positive">
        <i class="fas fa-arrow-up"></i> +12.5%
    </div>
</div>
```

---

## 📱 Navigation

### Mobile Bottom Navigation (Already in base_modern.html)
```html
<nav class="modern-mobile-nav">
    <a href="/dashboard" class="modern-mobile-nav-item active">
        <i class="fas fa-home modern-mobile-nav-icon"></i>
        <span>Home</span>
    </a>
    <a href="/packages" class="modern-mobile-nav-item">
        <i class="fas fa-box modern-mobile-nav-icon"></i>
        <span>Packages</span>
    </a>
    <!-- Add more items -->
</nav>
```

### Desktop Navbar (Already in base_modern.html)
```html
<nav class="modern-navbar">
    <div class="modern-container">
        <div class="modern-navbar-container">
            <a href="/" class="modern-navbar-brand">
                <div class="modern-navbar-logo">
                    <i class="fas fa-gem"></i>
                </div>
                <span>Max Wealth</span>
            </a>
            <div>
                <!-- Navigation items -->
            </div>
        </div>
    </div>
</nav>
```

---

## 📐 Layout

### Container
```html
<div class="modern-container">
    <p>Content with max-width and auto margins</p>
</div>
```

### Section
```html
<section class="modern-section">
    <div class="modern-container">
        <h2>Section Title</h2>
        <p>Section content...</p>
    </div>
</section>
```

### Grid Layout
```html
<!-- 2 Column Grid -->
<div class="modern-grid modern-grid-2">
    <div class="modern-card">Card 1</div>
    <div class="modern-card">Card 2</div>
</div>

<!-- 3 Column Grid -->
<div class="modern-grid modern-grid-3">
    <div class="modern-card">Card 1</div>
    <div class="modern-card">Card 2</div>
    <div class="modern-card">Card 3</div>
</div>

<!-- 4 Column Grid -->
<div class="modern-grid modern-grid-4">
    <div class="modern-card">Card 1</div>
    <div class="modern-card">Card 2</div>
    <div class="modern-card">Card 3</div>
    <div class="modern-card">Card 4</div>
</div>
```

### Flexbox Layout
```html
<!-- Basic Flex -->
<div class="modern-flex">
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<!-- Centered -->
<div class="modern-flex-center">
    <p>Centered content</p>
</div>

<!-- Space Between -->
<div class="modern-flex-between">
    <div>Left</div>
    <div>Right</div>
</div>
```

---

## 🎭 Effects

### Glassmorphism
```html
<div class="glass-effect" style="padding: var(--space-6); border-radius: var(--radius-xl);">
    <h3>Glass Effect</h3>
    <p>Semi-transparent with blur</p>
</div>
```

### Dark Glass
```html
<div class="glass-dark" style="padding: var(--space-6); border-radius: var(--radius-xl);">
    <h3>Dark Glass</h3>
    <p>Dark semi-transparent with blur</p>
</div>
```

### Hover Lift
```html
<div class="modern-card hover-lift">
    <p>Card lifts 4px on hover</p>
</div>
```

---

## 🎬 Animations

### Fade In
```html
<div class="animate-fade-in">
    <p>Fades in on load</p>
</div>
```

### Slide In
```html
<div class="animate-slide-in">
    <p>Slides in from right</p>
</div>
```

### Pulse
```html
<div class="animate-pulse">
    <p>Pulsing animation</p>
</div>
```

---

## 🔄 Loading States

### Spinner
```html
<div class="modern-spinner"></div>

<!-- Custom size -->
<div class="modern-spinner" style="width: 24px; height: 24px; border-width: 2px;"></div>
```

### Skeleton Loader
```html
<div class="modern-skeleton" style="height: 20px; margin-bottom: 10px;"></div>
<div class="modern-skeleton" style="height: 20px; width: 80%;"></div>
```

---

## 🧰 Utility Classes

### Spacing
```html
<!-- Margin -->
<div class="mt-4">Margin top</div>
<div class="mb-6">Margin bottom</div>

<!-- Padding -->
<div class="p-4">Padding all sides</div>
<div class="p-6">More padding</div>
```

### Text
```html
<!-- Alignment -->
<p class="text-center">Centered</p>
<p class="text-left">Left aligned</p>
<p class="text-right">Right aligned</p>

<!-- Size -->
<p class="text-xs">Extra small text</p>
<p class="text-sm">Small text</p>
<p class="text-base">Base text</p>
<p class="text-lg">Large text</p>
<p class="text-xl">Extra large text</p>

<!-- Weight -->
<p class="font-normal">Normal weight</p>
<p class="font-medium">Medium weight</p>
<p class="font-semibold">Semibold</p>
<p class="font-bold">Bold</p>

<!-- Color -->
<p class="text-primary">Primary color</p>
<p class="text-success">Success color</p>
<p class="text-error">Error color</p>
<p class="text-neutral">Neutral color</p>
```

### Display
```html
<div class="hidden">Hidden</div>
<div class="block">Block display</div>
<div class="flex">Flex display</div>
<div class="grid">Grid display</div>
```

### Flexbox
```html
<div class="flex flex-row items-center justify-between gap-4">
    <div>Left</div>
    <div>Right</div>
</div>
```

### Width
```html
<div class="w-full">Full width</div>
<div class="w-auto">Auto width</div>
```

### Border Radius
```html
<div class="rounded-sm">Small radius</div>
<div class="rounded">Medium radius</div>
<div class="rounded-lg">Large radius</div>
<div class="rounded-xl">Extra large radius</div>
<div class="rounded-full">Full circle</div>
```

### Shadows
```html
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Medium shadow</div>
<div class="shadow-lg">Large shadow</div>
<div class="shadow-xl">Extra large shadow</div>
```

---

## 🎨 Color Palette

### CSS Variables
```css
/* Primary Colors */
var(--color-primary-50)   /* Lightest */
var(--color-primary-100)
var(--color-primary-500)  /* Main gold */
var(--color-primary-600)  /* Darker gold */
var(--color-primary-900)  /* Darkest */

/* Semantic Colors */
var(--color-success-500)  /* Green */
var(--color-error-500)    /* Red */
var(--color-warning-500)  /* Orange */
var(--color-info-500)     /* Blue */

/* Neutrals */
var(--color-neutral-50)   /* Lightest gray */
var(--color-neutral-600)  /* Dark gray */
var(--color-neutral-900)  /* Darkest */

/* Gradients */
var(--gradient-primary)   /* Primary gradient */
var(--gradient-success)   /* Success gradient */
```

### Usage Example
```html
<div style="background: var(--color-primary-500); color: white; padding: var(--space-4);">
    <h3>Custom Styled Box</h3>
</div>
```

---

## 📦 Complete Page Example

```html
{% extends "base_modern.html" %}

{% block title %}My Page - Max Wealth{% endblock %}

{% block extra_styles %}
<style>
    /* Page-specific styles */
    body {
        background: var(--color-neutral-50);
        padding-top: calc(var(--nav-height) + var(--space-4));
    }
</style>
{% endblock %}

{% block content %}
<div class="modern-container" style="padding: var(--space-6) var(--container-padding);">
    <!-- Page Header -->
    <div class="modern-flex-between" style="margin-bottom: var(--space-6);">
        <h1>Page Title</h1>
        <a href="/back" class="modern-btn modern-btn-outline">
            <i class="fas fa-arrow-left"></i>
            <span>Back</span>
        </a>
    </div>
    
    <!-- Alert -->
    <div class="modern-alert modern-alert-info">
        <div class="modern-alert-icon">
            <i class="fas fa-info-circle"></i>
        </div>
        <div class="modern-alert-content">
            <div class="modern-alert-title">Information</div>
            <div>This is an important message.</div>
        </div>
    </div>
    
    <!-- Content Grid -->
    <div class="modern-grid modern-grid-2" style="margin-top: var(--space-6);">
        <div class="modern-card">
            <div class="modern-card-header">
                <h3 class="modern-card-title">Card Title</h3>
            </div>
            <div class="modern-card-body">
                <p>Card content goes here.</p>
            </div>
            <div class="modern-card-footer">
                <button class="modern-btn modern-btn-primary modern-btn-block">
                    <span>Action</span>
                </button>
            </div>
        </div>
        
        <div class="modern-card">
            <form method="POST">
                <div class="modern-form-group">
                    <label class="modern-form-label modern-form-label-required">
                        Name
                    </label>
                    <input type="text" class="modern-form-input" required>
                </div>
                
                <button type="submit" class="modern-btn modern-btn-primary modern-btn-block">
                    Submit
                </button>
            </form>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_scripts %}
<script>
    // Page-specific JavaScript
    console.log('Page loaded');
</script>
{% endblock %}
```

---

## 🎯 Best Practices

### 1. Consistent Spacing
Always use spacing variables:
```html
<!-- Good -->
<div style="padding: var(--space-4); margin-bottom: var(--space-6);">

<!-- Avoid -->
<div style="padding: 15px; margin-bottom: 25px;">
```

### 2. Semantic HTML
Use appropriate elements:
```html
<!-- Good -->
<button class="modern-btn modern-btn-primary">Click Me</button>

<!-- Avoid -->
<div class="modern-btn modern-btn-primary" onclick="...">Click Me</div>
```

### 3. Responsive Design
Test on multiple screen sizes:
```html
<!-- Mobile-first approach -->
<div class="modern-grid modern-grid-2">
    <!-- Automatically responsive -->
</div>
```

### 4. Accessibility
Include proper labels and ARIA attributes:
```html
<!-- Good -->
<label for="email" class="modern-form-label">Email</label>
<input type="email" id="email" class="modern-form-input" aria-required="true">

<!-- Better -->
<div class="modern-form-group">
    <label for="email" class="modern-form-label modern-form-label-required">
        Email
    </label>
    <input type="email" id="email" class="modern-form-input" required>
</div>
```

---

## 📚 Additional Resources

- **Full Documentation**: `UI_REDESIGN_DOCUMENTATION.md`
- **Quick Start**: `QUICK_START_UI_REDESIGN.md`
- **Design System CSS**: `static/css/modern-design-system.css`

---

**Need help?** Check the comments in `modern-design-system.css` for more details on each component!
