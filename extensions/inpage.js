window.__greenStyle = {
  askSettings() {
    window.postMessage({ source: 'VUE_APP', type: 'GET_SETTINGS' }, '*')
  },
  highlight(selector = '.demo') {
    window.postMessage(
      { source: 'VUE_APP', type: 'HIGHLIGHT_REQUEST', payload: { selector } },
      '*'
    )
  }
}

window.addEventListener('message', (e) => {
  if (e.data?.source !== 'EXT') return
  const evt = new CustomEvent('greenstyle:message', { detail: e.data })
  window.dispatchEvent(evt)
})
