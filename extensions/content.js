console.log('[GreenStyle] content.js chargé sur', location.href);

// Handshake vers la page
window.postMessage({ source: 'EXT', type: 'READY' }, '*');

// Injecte inpage.js (facultatif)
try {
  const s = document.createElement('script');
  s.src = chrome.runtime.getURL('inpage.js');
  (document.head || document.documentElement).appendChild(s);
  s.onload = () => s.remove();
} catch (e) {
  console.warn('Injection inpage.js échouée', e);
}

// Détection storage content + helpers fallback
const hasStorage = !!(chrome?.storage?.local);

function getSettingsSafe() {
  if (hasStorage) {
    return new Promise((resolve) =>
      chrome.storage.local.get('settings', (res) => resolve(res || {}))
    );
  }
  // fallback via background
  return new Promise((resolve) =>
    chrome.runtime.sendMessage({ type: 'BG_GET_SETTINGS' }, (res) => resolve(res || {}))
  );
}

function setPopupTextSafe(text) {
  if (hasStorage) {
    return new Promise((resolve) =>
      chrome.storage.local.set({ popupText: text }, resolve)
    ).then(() => chrome.runtime.sendMessage({ type: 'POPUP_TEXT_UPDATED', text }));
  }
  // fallback via background
  chrome.runtime.sendMessage({ type: 'BG_SET_POPUP_TEXT', text });
}

// Effet de surlignage
function highlight(selector = '.demo') {
  const el = document.querySelector(selector);
  if (!el) return console.warn('Élément non trouvé :', selector);
  el.style.transition = 'background 0.25s ease';
  el.style.background = 'yellow';
  window.postMessage({ source: 'EXT', type: 'HIGHLIGHT_DONE' }, '*');
}

// Messages de la page Vue
window.addEventListener('message', async (e) => {
  if (e.source !== window) return;
  const msg = e.data;
  if (!msg || msg.source !== 'VUE_APP') return;

  if (msg.type === 'GET_SETTINGS') {
    const { settings } = await getSettingsSafe();
    window.postMessage({ source: 'EXT', type: 'SETTINGS', payload: settings || {} }, '*');
  }

  if (msg.type === 'SET_POPUP_TEXT') {
    await setPopupTextSafe(msg.payload?.text ?? '');
  }

  if (msg.type === 'HIGHLIGHT_REQUEST') {
    highlight(msg.payload?.selector);
  }

  if (msg.type === 'PING') {
    window.postMessage({ source: 'EXT', type: 'PONG', t0: msg.t0 }, '*');
  }
});

// Messages du popup (optionnel)
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === 'HIGHLIGHT') {
    highlight(msg.payload?.selector);
    sendResponse({ ok: true });
    return true;
  }
});
