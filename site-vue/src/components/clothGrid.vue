<script setup>
import { ref, computed } from 'vue'
import ClothCard from './clothCard.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => ([
      { name: 'People Tree',  rating: 2.5, priceLevel: 2, src: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1200' },
      { name: 'Pantagonia',   rating: 2.0, priceLevel: 3, src: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1200' },
      { name: 'Veja',         rating: 3.0, priceLevel: 3, src: 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?q=80&w=1200' },
      { name: 'Armed Angels', rating: 2.5, priceLevel: 2, src: 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?q=80&w=1200' },
      { name: 'KnowledgeCot', rating: 4.0, priceLevel: 4, src: 'https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1200' },
      { name: 'Organic Basics', rating: 3.5, priceLevel: 3, src: 'https://images.unsplash.com/photo-1514996937319-344454492b37?q=80&w=1200' },
      { name: 'Thinking Mu',  rating: 2.0, priceLevel: 1, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Veja Kids',    rating: 3.5, priceLevel: 2, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Nudie Jeans',  rating: 4.5, priceLevel: 4, src: 'https://images.unsplash.com/photo-1514996937319-344454492b37?q=80&w=1200' },
      { name: 'Rains',        rating: 3.0, priceLevel: 2, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Ecoalf',       rating: 4.0, priceLevel: 5, src: 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?q=80&w=1200' },
      { name: 'Girlfriend',   rating: 2.5, priceLevel: 1, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Maison Verde', rating: 3.0, priceLevel: 3, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Atelier 12',   rating: 1.5, priceLevel: 1, src: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1200' },
      { name: 'Bleu Forêt',   rating: 3.5, priceLevel: 2, src: 'https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1200' },
      { name: 'SlowWear',     rating: 5.0, priceLevel: 5, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Pact',         rating: 4.0, priceLevel: 2, src: 'https://images.unsplash.com/photo-1514996937319-344454492b37?q=80&w=1200' },
      { name: 'Jan n June',   rating: 2.0, priceLevel: 3, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Organic Lab',  rating: 1.0, priceLevel: 1, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200' },
      { name: 'Loop Studio',  rating: 4.5, priceLevel: 4, src: 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?q=80&w=1200' },
    ])
  },
  cols: { type: Number, default: 4 }
})

const openMenu = ref(null)
const sortKey  = ref(null) 
const sortDir  = ref('desc') 

const sortedItems = computed(() => {
  const arr = props.items.slice()
  if (!sortKey.value) return arr
  const key = sortKey.value === 'price' ? 'priceLevel' : 'rating'
  return arr.sort((a, b) => {
    const av = a[key] ?? 0
    const bv = b[key] ?? 0
    if (av === bv) return props.items.indexOf(a) - props.items.indexOf(b)
    return sortDir.value === 'asc' ? av - bv : bv - av
  })
})

function toggleMenu(which){ openMenu.value = openMenu.value === which ? null : which }
function applySort(which, dir){
  sortKey.value = which
  sortDir.value = dir
  openMenu.value = null
}
function resetSort(){
  sortKey.value = null
  sortDir.value = 'desc'
  openMenu.value = null
}
</script>

<template>
  <section class="cloth-grid-wrap">
    <!-- BARRE DE FILTRES -->
    <div class="toolbar">
      <div class="chip" :class="{ open: openMenu==='price', active: sortKey==='price' }">
        <button class="chip-btn" @click="toggleMenu('price')">
          <span class="label">Prix</span>
          <span class="caret" aria-hidden="true" />
        </button>
        <div v-if="openMenu==='price'" class="menu">
          <button @click="applySort('price','asc')">Du plus petit au plus grand</button>
          <button @click="applySort('price','desc')">Du plus grand au plus petit</button>
        </div>
      </div>

      <!-- Boutons “maquette” (visuels) -->
      <div class="chip"><button class="chip-btn" disabled><span class="label">Lieu de production</span><span class="caret" /></button></div>
      <div class="chip"><button class="chip-btn" disabled><span class="label">Travail</span><span class="caret" /></button></div>
      <div class="chip"><button class="chip-btn" disabled><span class="label">Pollution</span><span class="caret" /></button></div>
      <div class="chip"><button class="chip-btn" disabled><span class="label">Certifications</span><span class="caret" /></button></div>
      <div class="chip"><button class="chip-btn" disabled><span class="label">Taille</span><span class="caret" /></button></div>
      <div class="chip"><button class="chip-btn" disabled><span class="label">Catégories</span><span class="caret" /></button></div>

      <div class="chip" :class="{ open: openMenu==='rating', active: sortKey==='rating' }">
        <button class="chip-btn" @click="toggleMenu('rating')">
          <span class="label">Note</span>
          <span class="caret" aria-hidden="true" />
        </button>
        <div v-if="openMenu==='rating'" class="menu">
          <button @click="applySort('rating','asc')">Du plus petit au plus grand</button>
          <button @click="applySort('rating','desc')">Du plus grand au plus petit</button>
        </div>
      </div>

      <span class="divider" />
      <button class="reset" @click="resetSort">Réinitialiser les filtres</button>
    </div>

    <!-- GRILLE -->
    <div class="grid" :style="{ '--cols': cols }">
      <ClothCard
        v-for="(p, i) in sortedItems"
        :key="p.name + i"
        :name="p.name"
        :rating="p.rating"
        :priceLevel="p.priceLevel"
        :src="p.src"
      />
    </div>
  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Jersey+10&display=swap');

:root{
  --pill-color: #00320B;    /* couleur texte & border */
}

/* --- Toolbar --- */
.toolbar{
  display:flex;
  align-items:center;
  gap: 10px;
  margin: 8px 0 18px;
  flex-wrap: wrap;
  font-family: "Jersey 10", system-ui, sans-serif;
  line-height: 1;
}

.chip{
  position: relative;
}

/* “Pill” exact style */
.chip-btn{
  display:inline-flex;
  align-items:center;
  justify-content: center;
  gap: 8px;
  min-width: 122px;         
  height: 30px;                  
  padding: 0 14px;                  
  border-radius: 25px;              
  border: 1px solid #00320B;
  background: transparent;
  color: #00320B;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 15px;
  letter-spacing: 0;
  cursor: pointer;
}

.chip-btn[disabled]{
  opacity: 0.7;
  cursor: default;
}

.chip.active .label{
  text-decoration: underline;
}

.caret{
  width: 8px;
  height: 8px;
  border-right: 1px solid currentColor;
  border-bottom: 1px solid currentColor;
  transform: rotate(45deg);
  transition: transform .2s ease;
}
.chip.open .caret{ transform: rotate(-135deg); }

.menu{
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  min-width: 220px;
  background: #fff;
  border: 1px solid rgba(0,0,0,.12);
  box-shadow: 0 6px 20px rgba(0,0,0,.12);
  border-radius: 10px;
  overflow: hidden;
  z-index: 5;
}
.menu > button{
  display:block;
  width: 100%;
  text-align: left;
  padding: 10px 12px;
  background: #fff;
  border: none;
  cursor: pointer;
  font-family: system-ui, sans-serif;
}
.menu > button:hover{ background: #f6f6f6; }

.divider{
  width: 1px;
  height: 24px;
  background: rgba(0,0,0,.25);
  margin-left: 4px;
}
.reset{
  background: transparent;
  border: none;
  cursor: pointer;
  color: #808080;
  font-family: system-ui, sans-serif;
  text-decoration: none;
}

.grid{
  display: grid;
  grid-template-columns: repeat(var(--cols), minmax(0, 1fr));
  gap: 28px;
}

@media (max-width: 1200px){ .grid{ grid-template-columns: repeat(3, 1fr); } }
@media (max-width: 900px) { .grid{ grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 520px) { .grid{ grid-template-columns: 1fr; } }
</style>
