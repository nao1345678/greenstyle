<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: { type: String, required: true },
  text:  { type: String, required: true },
  defaultOpen: { type: Boolean, default: true },
})

const open = ref(props.defaultOpen)
const panelId = `brand-intro-${Math.random().toString(36).slice(2, 9)}`
</script>

<template>
  <section class="brand-intro">
    <div class="title-row">
      <h2 class="title">{{ title }}</h2>

      <button
        class="toggle"
        type="button"
        @click="open = !open"
        :aria-expanded="open"
        :aria-controls="panelId"
      >
        <span class="chev" :class="{ open }" aria-hidden="true"></span>
      </button>
    </div>

    <transition name="collapse">
      <p
        v-show="open"
        :id="panelId"
        class="desc"
      >
        {{ text }}
      </p>
    </transition>
  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Jersey+10&display=swap');

.brand-intro{
  background: transparent;
}

.title-row{
  display: flex;
  align-items: center;
  gap: 10px;
}

.title{
  margin: 0;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 45px; 
  line-height: 1;
  letter-spacing: 0;
  color: #B70064; 
}

.toggle{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  cursor: pointer;
  padding: 2px;
}

.chev{
  width: 12px;
  height: 12px;
  border-right: 2px solid currentColor;
  border-bottom: 2px solid currentColor;
  transform: rotate(45deg);
  transition: transform .2s ease;
  color: #B70064;
}
.chev.open{
  transform: rotate(-135deg);
}

.desc{
  margin: 8px 0 0;
  color: #000;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, "Helvetica Neue", Arial, "Noto Sans", "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji", sans-serif;
  font-weight: 300;
  font-size: 12px;
  line-height: 1;
  letter-spacing: 0;
}

.collapse-enter-from,
.collapse-leave-to { height: 0; opacity: 0; }
.collapse-enter-to,
.collapse-leave-from { height: auto; opacity: 1; }
.collapse-enter-active,
.collapse-leave-active {
  overflow: hidden;
  transition: height .18s ease, opacity .18s ease;
}
</style>
