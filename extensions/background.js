chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === 'BG_GET_SETTINGS') {
    chrome.storage.local.get('settings', (res) => {
      sendResponse({ settings: res?.settings || {} });
    });
    return true;
  }
  if (msg?.type === 'BG_SET_POPUP_TEXT') {
    const text = msg.text || '';
    chrome.storage.local.set({ popupText: text }, () => {
      chrome.runtime.sendMessage({ type: 'POPUP_TEXT_UPDATED', text });
      sendResponse({ ok: true });
    });
    return true;
  }
});
