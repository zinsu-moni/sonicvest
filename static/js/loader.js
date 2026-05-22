// Loader JavaScript Functions

class FinTechLoader {
    constructor() {
        this.overlay = null;
        this.refCount = 0; // prevent flicker on rapid show/hide
        this.init();
    }

    init() {
        // Create loader overlay if it doesn't exist
        if (!document.getElementById('loader-overlay')) {
            this.createLoaderOverlay();
        }
        this.overlay = document.getElementById('loader-overlay');
    }

    createLoaderOverlay() {
        const overlay = document.createElement('div');
        overlay.id = 'loader-overlay';
        overlay.className = 'loader-overlay hidden';
        overlay.setAttribute('role', 'status');
        overlay.setAttribute('aria-live', 'polite');
        overlay.setAttribute('aria-busy', 'false');
        overlay.innerHTML = `
            <div class="loader-fintech" aria-hidden="false">
                <div class="loader-logo" aria-hidden="true">
                    <img src="/static/images/logo.svg" alt="" class="loader-logo-image">
                </div>
                <div class="loader" aria-hidden="true"></div>
                <div class="loader-text">Loading...</div>
                <div class="loader-subtitle">Please wait while we process your request</div>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    setState(stateClass) {
        if (!this.overlay) return;
        // remove possible state classes
        this.overlay.classList.remove('loader-success', 'loader-error');
        if (stateClass) this.overlay.classList.add(stateClass);
    }

    show(text = 'Loading...', subtitle = 'Please wait while we process your request') {
        if (this.overlay) {
            const textElement = this.overlay.querySelector('.loader-text');
            const subtitleElement = this.overlay.querySelector('.loader-subtitle');
            if (textElement) textElement.textContent = text;
            if (subtitleElement) subtitleElement.textContent = subtitle;

            this.setState(null);
            this.refCount = Math.max(0, this.refCount) + 1;
            this.overlay.classList.remove('hidden');
            this.overlay.setAttribute('aria-busy', 'true');
            document.body.style.overflow = 'hidden';
        }
    }

    hide(force = false) {
        if (!this.overlay) return;
        this.refCount = force ? 0 : Math.max(0, this.refCount - 1);
        if (this.refCount === 0) {
            this.overlay.classList.add('hidden');
            this.overlay.setAttribute('aria-busy', 'false');
            document.body.style.overflow = '';
            this.setState(null);
        }
    }

    // transient states
    success(text = 'Success!', subtitle = 'Operation completed') {
        this.show(text, subtitle);
        this.setState('loader-success');
        setTimeout(() => this.hide(true), 1200);
    }

    error(text = 'Error', subtitle = 'Something went wrong') {
        this.show(text, subtitle);
        this.setState('loader-error');
        setTimeout(() => this.hide(true), 1600);
    }

    // Show loader for a specific duration
    showFor(duration = 2000, text = 'Loading...', subtitle = 'Please wait...') {
        this.show(text, subtitle);
        setTimeout(() => {
            this.hide();
        }, duration);
    }
}

// Initialize global loader
let fintechLoader;

document.addEventListener('DOMContentLoaded', function () {
    fintechLoader = new FinTechLoader();
});

// Utility functions for easy access
function showLoader(text, subtitle) {
    if (fintechLoader) {
        fintechLoader.show(text, subtitle);
    }
}

function hideLoader() {
    if (fintechLoader) {
        fintechLoader.hide();
    }
}

function showLoaderFor(duration, text, subtitle) {
    if (fintechLoader) {
        fintechLoader.showFor(duration, text, subtitle);
    }
}

function showLoaderSuccess(text, subtitle) {
    if (fintechLoader) {
        fintechLoader.success(text, subtitle);
    }
}

function showLoaderError(text, subtitle) {
    if (fintechLoader) {
        fintechLoader.error(text, subtitle);
    }
}

// Button loading states
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.classList.add('btn-loading');
        button.disabled = true;
        // preserve full HTML so icons aren't lost
        button.dataset.originalHtml = button.innerHTML;
    } else {
        button.classList.remove('btn-loading');
        button.disabled = false;
        if (button.dataset.originalHtml) {
            button.innerHTML = button.dataset.originalHtml;
            delete button.dataset.originalHtml;
        }
    }
}

// Form submission with loader
function submitFormWithLoader(formElement, options = {}) {
    const {
        loadingText = 'Processing...',
        loadingSubtitle = 'Please wait while we process your request',
        submitButton = formElement.querySelector('button[type="submit"]'),
        onSuccess = null,
        onError = null
    } = options;

    // Show loader
    showLoader(loadingText, loadingSubtitle);

    // Set button loading state
    if (submitButton) {
        setButtonLoading(submitButton, true);
    }

    // Create FormData
    const formData = new FormData(formElement);

    // Submit form via fetch
    fetch(formElement.action, {
        method: formElement.method || 'POST',
        body: formData
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok');
        })
        .then(data => {
            hideLoader();
            if (submitButton) {
                setButtonLoading(submitButton, false);
            }

            if (onSuccess) {
                onSuccess(data);
            } else if (data.redirect) {
                window.location.href = data.redirect;
            }
        })
        .catch(error => {
            hideLoader();
            if (submitButton) {
                setButtonLoading(submitButton, false);
            }

            if (onError) {
                onError(error);
            } else {
                console.error('Error:', error);
                if (window.showToast) {
                    window.showToast('An error occurred. Please try again.', 'danger');
                } else {
                    console.error('An error occurred. Please try again.');
                }
            }
        });
}

// Page navigation with loader
function navigateWithLoader(url, text = 'Loading page...') {
    showLoader(text, 'Redirecting to your destination');

    // Add small delay to show loader
    setTimeout(() => {
        window.location.href = url;
    }, 500);
}

// AJAX request with loader
function ajaxWithLoader(url, options = {}) {
    const {
        method = 'GET',
        data = null,
        loadingText = 'Loading...',
        loadingSubtitle = 'Please wait...',
        onSuccess = null,
        onError = null
    } = options;

    showLoader(loadingText, loadingSubtitle);

    const fetchOptions = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        fetchOptions.body = JSON.stringify(data);
    }

    return fetch(url, fetchOptions)
        .then(response => {
            hideLoader();
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok');
        })
        .then(data => {
            if (onSuccess) {
                onSuccess(data);
            }
            return data;
        })
        .catch(error => {
            hideLoader();
            if (onError) {
                onError(error);
            } else {
                console.error('Error:', error);
            }
            throw error;
        });
}

// Auto-show loader on page load
window.addEventListener('beforeunload', function () {
    // Avoid showing loader for same-page hash changes
    if (location.hash) return;
    showLoader('Loading...', 'Please wait...');
});

// Hide loader when page is fully loaded
window.addEventListener('load', function () {
    // Small delay to ensure smooth transition
    setTimeout(() => {
        hideLoader(true);
    }, 300);
});

// Handle pageshow from bfcache (back/forward navigation)
window.addEventListener('pageshow', function (evt) {
    if (evt.persisted) {
        hideLoader(true);
    }
});

// Auto hooks via data attributes
document.addEventListener('DOMContentLoaded', function () {
    // Forms: add loader on submit when marked
    document.addEventListener('submit', function (e) {
        const form = e.target;
        if (form.matches('form[data-loader], form.use-loader, form[data-loading]')) {
            const text = form.getAttribute('data-loader-text') || 'Processing...';
            const subtitle = form.getAttribute('data-loader-subtitle') || 'Please wait while we process your request';
            showLoader(text, subtitle);
        }
    }, true);

    // Links/buttons: show loader when marked
    document.addEventListener('click', function (e) {
        const link = e.target.closest('a[data-loader], button[data-loader]');
        if (!link) return;

        const text = link.getAttribute('data-loader-text') || 'Loading...';
        const subtitle = link.getAttribute('data-loader-subtitle') || 'Please wait...';
        const isAnchor = link.tagName.toLowerCase() === 'a';
        const href = isAnchor ? link.getAttribute('href') : null;

        showLoader(text, subtitle);

        // For anchors without target _blank and with real href, navigate after a short delay
        if (isAnchor && href && href !== '#' && link.getAttribute('target') !== '_blank') {
            e.preventDefault();
            setTimeout(() => { window.location.href = href; }, 120);
        }
    });
});

// Export for use in other scripts
window.FinTechLoader = {
    show: showLoader,
    hide: hideLoader,
    showFor: showLoaderFor,
    success: showLoaderSuccess,
    error: showLoaderError,
    setButtonLoading: setButtonLoading,
    submitFormWithLoader: submitFormWithLoader,
    navigateWithLoader: navigateWithLoader,
    ajaxWithLoader: ajaxWithLoader
};
