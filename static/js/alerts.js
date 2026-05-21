// FinTech custom alerts (toasts/snackbars)
// Injects minimal CSS and exposes window.showToast(message, type, options)
(function(){
  if (window.FinTechAlertsLoaded) return; // prevent double-load
  window.FinTechAlertsLoaded = true;

  const styles = `
  .ft-toast-container { position: fixed; top: 16px; left: 50%; transform: translateX(-50%); z-index: 20000; display: flex; flex-direction: column; gap: 10px; width: min(92vw, 420px); }
  .ft-toast { display: flex; align-items: start; gap: 10px; padding: 12px 14px; border-radius: 10px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); color: #0f172a; background: #fff; border-left: 4px solid #2563eb; opacity: 0; transform: translateY(-8px); animation: ft-toast-in 180ms ease-out forwards; }
  .ft-toast.success { border-left-color: #16a34a; }
  .ft-toast.warning { border-left-color: #f59e0b; }
  .ft-toast.danger { border-left-color: #ef4444; }
  .ft-toast .ft-icon { font-size: 18px; margin-top: 2px; }
  .ft-toast .ft-content { flex: 1; }
  .ft-toast .ft-title { font-weight: 700; font-size: 14px; margin: 0 0 2px; color: #0f172a; }
  .ft-toast .ft-message { font-size: 13px; margin: 0; color: #0f172a; }
  .ft-toast .ft-close { background: transparent; border: 0; color: #0f172a; opacity: .7; cursor: pointer; font-size: 18px; line-height: 1; padding: 0 2px; }
  .ft-toast .ft-close:hover { opacity: 1; }
  @keyframes ft-toast-in { to { opacity: 1; transform: translateY(0); } }
  @keyframes ft-toast-out { to { opacity: 0; transform: translateY(-6px); } }
  `;

  const styleEl = document.createElement('style');
  styleEl.textContent = styles;
  document.head.appendChild(styleEl);

  function ensureContainer(){
    let c = document.querySelector('.ft-toast-container');
    if (!c) {
      c = document.createElement('div');
      c.className = 'ft-toast-container';
      document.body.appendChild(c);
    }
    return c;
  }

  function iconFor(type){
    switch(type){
      case 'success': return '<i class="fas fa-check-circle ft-icon" style="color:#16a34a"></i>';
      case 'warning': return '<i class="fas fa-exclamation-triangle ft-icon" style="color:#f59e0b"></i>';
      case 'danger': return '<i class="fas fa-times-circle ft-icon" style="color:#ef4444"></i>';
      default: return '<i class="fas fa-info-circle ft-icon" style="color:#2563eb"></i>';
    }
  }

  window.showToast = function(message, type = 'info', options = {}){
    const { title = null, timeout = 3500 } = options;
    const container = ensureContainer();

    const toast = document.createElement('div');
    toast.className = `ft-toast ${type}`;
    toast.setAttribute('role', 'status');
    toast.setAttribute('aria-live', 'polite');

    toast.innerHTML = `
      ${iconFor(type)}
      <div class="ft-content">
        ${title ? `<div class="ft-title">${title}</div>` : ''}
        <div class="ft-message">${message}</div>
      </div>
      <button class="ft-close" aria-label="Close">&times;</button>
    `;

    const closeBtn = toast.querySelector('.ft-close');
    closeBtn.addEventListener('click', () => dismiss());

    container.appendChild(toast);

    let hideTimer;
    if (timeout > 0) {
      hideTimer = setTimeout(() => dismiss(), timeout);
    }

    function dismiss(){
      if (hideTimer) clearTimeout(hideTimer);
      toast.style.animation = 'ft-toast-out 160ms ease-in forwards';
      setTimeout(() => toast.remove(), 170);
    }

    return { dismiss };
  };
})();
