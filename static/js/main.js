/**
 * Main JavaScript for Fintech Finance
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize all popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Countdown timer for next income drop
    initializeCountdown();
    
    // Copy referral link to clipboard
    initializeReferralCopy();
    
    // Initialize form validations
    initializeFormValidations();
});

/**
 * Initialize countdown timer for next income drop
 */
function initializeCountdown() {
    const countdownElement = document.getElementById('income-countdown');
    if (!countdownElement) return;
    
    const targetTime = new Date(countdownElement.dataset.target).getTime();
    
    // Update the countdown every second
    const countdown = setInterval(function() {
        const now = new Date().getTime();
        const distance = targetTime - now;
        
        // Time calculations
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        // Display the result
        countdownElement.innerHTML = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // If the countdown is finished
        if (distance < 0) {
            clearInterval(countdown);
            countdownElement.innerHTML = "Income Ready!";
            countdownElement.classList.add('text-success');
        }
    }, 1000);
}

/**
 * Initialize copy functionality for referral link
 */
function initializeReferralCopy() {
    const copyButton = document.getElementById('copy-referral');
    if (!copyButton) return;
    
    copyButton.addEventListener('click', function() {
        const referralLink = document.getElementById('referral-link').value;
        
        navigator.clipboard.writeText(referralLink).then(function() {
            // Show success message
            const originalText = copyButton.innerHTML;
            copyButton.innerHTML = '<i class="fas fa-check"></i> Copied!';
            copyButton.classList.remove('btn-primary');
            copyButton.classList.add('btn-success');
            
            // Revert button after 2 seconds
            setTimeout(function() {
                copyButton.innerHTML = originalText;
                copyButton.classList.remove('btn-success');
                copyButton.classList.add('btn-primary');
            }, 2000);
        });
    });
}

/**
 * Initialize form validations
 */
function initializeFormValidations() {
    // Withdrawal form validation
    const withdrawalForm = document.getElementById('withdrawal-form');
    if (withdrawalForm) {
        withdrawalForm.addEventListener('submit', function(event) {
            const amount = parseFloat(document.getElementById('amount').value);
            const minAmount = parseFloat(withdrawalForm.dataset.minimum || 1000);
            const maxAmount = parseFloat(withdrawalForm.dataset.maximum || 0);
            
            if (amount < minAmount) {
                event.preventDefault();
                showAlert(`Minimum withdrawal amount is ₦${minAmount}`, 'danger');
                return false;
            }
            
            if (maxAmount > 0 && amount > maxAmount) {
                event.preventDefault();
                showAlert(`Maximum withdrawal amount is ₦${maxAmount}`, 'danger');
                return false;
            }
        });
    }
    
    // Payment form validation
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(event) {
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked');
            
            if (!paymentMethod) {
                event.preventDefault();
                showAlert('Please select a payment method', 'danger');
                return false;
            }
            
            if (paymentMethod.value === 'bank_transfer') {
                const proofFile = document.getElementById('payment_proof').files[0];
                if (!proofFile) {
                    event.preventDefault();
                    showAlert('Please upload payment proof', 'danger');
                    return false;
                }
            }
        });
    }
}

/**
 * Show alert message
 */
function showAlert(message, type = 'info') {
    const alertPlaceholder = document.getElementById('alert-placeholder');
    if (!alertPlaceholder) return;
    
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    alertPlaceholder.appendChild(wrapper);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        const alert = wrapper.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 5000);
}
