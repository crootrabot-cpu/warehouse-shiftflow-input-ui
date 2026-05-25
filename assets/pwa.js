const SW_URL = '/sw.js?v=3';
let deferredInstallPrompt = null;

const shell = document.getElementById('installShell');
const button = document.getElementById('installAppButton');

function showInstallShell(message) {
  if (!shell) return;
  const meta = shell.querySelector('.install-shell__meta');
  if (meta && message) meta.textContent = message;
  shell.classList.add('is-visible');
}

function hideInstallShell() {
  if (!shell) return;
  shell.classList.remove('is-visible');
}

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register(SW_URL).catch((error) => console.error('service worker registration failed', error));
  });
}

window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault();
  deferredInstallPrompt = event;
  showInstallShell('Install this on your phone for one-tap launch and a native-feeling shell.');
});

window.addEventListener('appinstalled', () => {
  deferredInstallPrompt = null;
  showInstallShell('Installed. Open it from your home screen like a normal app.');
  window.setTimeout(hideInstallShell, 3200);
});

if (button) {
  button.addEventListener('click', async () => {
    if (deferredInstallPrompt) {
      deferredInstallPrompt.prompt();
      await deferredInstallPrompt.userChoice.catch(() => null);
      deferredInstallPrompt = null;
      return;
    }

    showInstallShell('On iPhone: Share -> Add to Home Screen. On Android Chrome: menu -> Install app.');
  });
}

if (window.matchMedia('(display-mode: standalone)').matches) {
  showInstallShell('Installed app mode active.');
  window.setTimeout(hideInstallShell, 1800);
}
