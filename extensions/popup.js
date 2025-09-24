(function () {
  const el = document.getElementById('mirror');
  const setText = (t) => { el.textContent = (t && String(t).length) ? t : '(aucun texte)'; };

  const hasStorage = !!(chrome?.storage?.local);

  if (hasStorage) {
    chrome.storage.local.get('popupText', (res) => setText(res?.popupText || ''));
    chrome.storage.onChanged.addListener((changes, area) => {
      if (area === 'local' && changes.popupText) {
        setText(changes.popupText.newValue || '');
      }
    });
  } else {
    chrome.runtime.sendMessage({ type: 'BG_GET_POPUP_TEXT' }, (res) => {
      setText(res?.popupText || '');
    });
  }

  chrome.runtime.onMessage.addListener((msg) => {
    if (msg?.type === 'POPUP_TEXT_UPDATED') {
      setText(msg.text || '');
    }
  });
})();
