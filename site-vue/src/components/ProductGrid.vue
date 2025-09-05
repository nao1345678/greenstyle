<script setup>
import ProductCard from './ProductCard.vue'

const props = defineProps({
  title: { type: String, default: 'Catégories de marques' },
  items: {
    type: Array,
    default: () => ([
      { id: 1, src: 'https://images.unsplash.com/photo-1520975979651-c0d61a6d3b98?q=80&w=1200', alt: 'Baskets blanches' },
      { id: 2, src: 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1200', alt: 'T-shirt' },
      { id: 3, src: 'https://images.unsplash.com/photo-1520975916090-3105956dac38?q=80&w=1200', alt: 'Veste' },
      { id: 4, src: 'https://images.unsplash.com/photo-1503341455253-b2e723bb3dbb?q=80&w=1200', alt: 'Sac' },
      { id: 5, src: 'https://images.unsplash.com/photo-1514996937319-344454492b37?q=80&w=1200', alt: 'Pantalon' },
      { id: 6, src: 'https://images.unsplash.com/photo-1522906456132-bac22adad33e?q=80&w=1200', alt: 'Chemise' },
      { id: 7, src: 'https://images.unsplash.com/photo-1503342394128-c104d54dba01?q=80&w=1200', alt: 'Manteau' },
      { id: 8, src: 'https://images.unsplash.com/photo-1520975922323-270b3fb3a8ca?q=80&w=1200', alt: 'Robe' },
    ])
  },
  cols: { type: Number, default: 4 }
})
</script>

<template>
  <section class="product-bleed"> 
    <div class="grid-wrap">
      <h2 class="heading">{{ title }}</h2>
      <div class="grid" :style="{ '--cols': cols }">
        <ProductCard
          v-for="p in items"
          :key="p.id ?? p.src"
          v-bind="p"
        />
      </div>
    </div>
  </section>
</template>

<style scoped>
.product-bleed{
  background: var(--product-bg, #FFF5E6);
  position: relative;

  left: 50%;
  right: 50%;
  margin-left: -50vw;
  margin-right: -50vw;
  width: 100vw;

  padding: 16px 0 32px;
}

.grid-wrap{
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.heading{
  margin: 0 0 18px;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 26px;
  color: var(--pink, #B70064);
}

.grid{
  display: grid;
  grid-template-columns: repeat(var(--cols), minmax(0,1fr));
  gap: 28px;
}

@media (max-width: 1024px){ .grid{ grid-template-columns: repeat(3,1fr); } }
@media (max-width: 768px) { .grid{ grid-template-columns: repeat(2,1fr); } }
@media (max-width: 480px) { .grid{ grid-template-columns: 1fr; } }
</style>

