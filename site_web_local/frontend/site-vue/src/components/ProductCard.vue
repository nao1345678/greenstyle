<script setup>
import { RouterLink } from 'vue-router'

const props = defineProps({
  src:  { type: String, required: true },
  alt:  { type: String, default: "" },
  to:   { type: [String, Object], required: true },
})
</script>

<template>
  <RouterLink class="card" :to="to">
    <img :src="src" :alt="alt" loading="lazy" />
  </RouterLink>
</template>

<style scoped>
.card{
  display:block; width:100%;
  aspect-ratio: 4/3;
  border-radius: 3px;
  overflow:hidden;
  background: transparent;
  border: 1px solid rgba(104,183,113,.45);
  box-shadow: 0 1px 0 rgba(0,0,0,.05);
  transition: transform .15s, box-shadow .15s, border-color .15s;
}
.card:hover{
  transform: translateY(-2px);
  box-shadow: 0 6px 14px rgba(0,0,0,.12);
  border-color: var(--pink);
}
.card img{ width:100%; height:100%; object-fit:cover; display:block; }

/* Mobile - Ajuster les effets hover */
@media (max-width: 768px) {
  .card {
    border-radius: 2px;
  }
  
  .card:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0,0,0,.1);
  }
  
  /* Sur mobile, utiliser :active au lieu de :hover */
  .card:active {
    transform: translateY(-1px);
    box-shadow: 0 4px 10px rgba(0,0,0,.1);
  }
}

@media (max-width: 480px) {
  .card {
    aspect-ratio: 3/2;
    border-radius: 2px;
  }
}

/* Petit mobile */
@media (max-width: 380px) {
  .card {
    aspect-ratio: 4/3;
  }
}
</style>
