<script setup>
const props = defineProps({
  modelValue: { type: String, default: "" },
  placeholder: { type: String, default: "Rechercher une marque…" },
  width: { type: Number, default: 695 },
  height: { type: Number, default: 42 },
})
const emit = defineEmits(["update:modelValue", "search"])

const onInput = (e) => emit("update:modelValue", e.target.value)
const onSubmit = () => emit("search", props.modelValue)
</script>

<template>
  <form
    class="searchbar"
    role="search"
    aria-label="Recherche"
    :style="{ '--w': width + 'px', '--h': height + 'px' }"
    @submit.prevent="onSubmit"
  >
    <span class="icon" aria-hidden="true">
      <!-- loupe SVG -->
      <svg viewBox="0 0 24 24">
        <circle cx="11" cy="11" r="7" />
        <line x1="16.65" y1="16.65" x2="21" y2="21" />
      </svg>
    </span>

    <input
      type="search"
      :placeholder="placeholder"
      :value="modelValue"
      @input="onInput"
    />

    <!-- accesibilité -->
    <button type="submit" class="visually-hidden">Rechercher</button>
  </form>
</template>

<style scoped>
.searchbar{
  width: min(var(--w), 92vw);
  height: var(--h);
  margin: 24px auto 0;                   /* centrée sous le hero */
  padding: 0 16px 0 14px;
  display: flex; align-items: center; gap: 10px;

  background: rgba(255,255,255,0.9);      /* 90% blanc */
  border: 1px solid #68B771;             /* bordure figma */
  border-radius: 50px;                    /* rayon 50px */
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);             /* blur 2 */

  /* petite ombre très légère optionnelle */
  box-shadow: 0 1px 0 rgba(0,0,0,.04);
}

.icon{
  width: 22px; height: 22px;
  display: inline-flex; align-items: center; justify-content: center;
  flex: 0 0 auto;
}
.icon svg{
  width: 22px; height: 22px;
  stroke: #2B6A33; stroke-width: 2; fill: none; stroke-linecap: round;
}

input{
  flex: 1; height: 100%;
  border: 0; outline: 0; background: transparent;
  font: 16px/1 system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color: #1f2937;
}
input::placeholder{ color: #8ea58f; opacity: 1; }

.visually-hidden{
  position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden;
}
</style>
