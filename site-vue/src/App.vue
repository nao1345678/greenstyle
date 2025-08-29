<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const settings = ref({})
const extDetected = ref(false)
const status = ref('')

const popupText = ref('')
function sendToPopup () {
  window.postMessage({
    source: 'VUE_APP',
    type: 'SET_POPUP_TEXT',
    payload: { text: popupText.value }
  }, '*')
}

function onMessage (e) {
  const d = e.data
  if (!d || d.source !== 'EXT') return
  if (d.type === 'READY') extDetected.value = true
  if (d.type === 'SETTINGS') { settings.value = d.payload || {}; extDetected.value = true }
  if (d.type === 'HIGHLIGHT_DONE') { status.value = 'Surlignage ok'; extDetected.value = true }
  if (d.type === 'PONG') {
    const ms = (performance.now() - d.t0).toFixed(1)
    status.value = `PONG en ${ms} ms`
    extDetected.value = true
  }
}

function askSettings () {
  window.postMessage({ source: 'VUE_APP', type: 'GET_SETTINGS' }, '*')
}
function requestHighlight () {
  window.postMessage({ source: 'VUE_APP', type: 'HIGHLIGHT_REQUEST', payload: { selector: '.demo' } }, '*')
}

onMounted(() => { window.addEventListener('message', onMessage); askSettings() })
onUnmounted(() => window.removeEventListener('message', onMessage))
</script>

<template>
  <main>
    <h1>Site Vue × Extension</h1>
    <p>Extension : <strong>{{ extDetected ? 'connectée' : 'non détectée' }}</strong></p>
    <pre>{{ settings }}</pre>
    <p>{{ status }}</p>
    <div class="row">
    <div class="row">
</div>

<label style="display:block;margin:.5rem 0;">Texte pour le popup :</label>
<input v-model="popupText" @input="sendToPopup" placeholder="Tape ici..." style="padding:.5rem;width:100%;" />

<p style="opacity:.7;font-size:.9rem;">Status : {{ status }}</p>
</div>
<p>{{ status }}</p>

  </main>
</template>

<style>
main { max-width: 720px; margin: 2rem auto; font-family: system-ui, sans-serif; }
.row { display:flex; gap:.5rem; margin:1rem 0; }
pre { background:#f6f8fa; padding:.75rem; border-radius:.5rem; }
.demo { padding:.25rem; }
button { padding:.5rem .75rem; border:1px solid #e2e8f0; border-radius:.5rem; cursor:pointer; }
button:hover { background:#f1f5f9; }
</style>