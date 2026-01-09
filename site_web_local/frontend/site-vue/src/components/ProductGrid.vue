<script setup>
import ProductCard from './ProductCard.vue'
import BrandCard from './BrandCard.vue'

const props = defineProps({
  title: { type: String, default: 'Catégories de marques' },
  items: {
    type: Array,
    default: () => []
  },
  cols: { type: Number, default: 4 },
  useBrandCard: { type: Boolean, default: false },
  loading: { type: Boolean, default: false },
  error: { type: String, default: null }
})
</script>

<template>
  <section class="product-bleed"> 
    <div class="grid-wrap">
      <h2 class="heading">{{ title }}</h2>
      <div v-if="loading" class="loading">
        Chargement des marques...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else class="grid" :style="{ '--cols': cols }">
        <BrandCard
          v-if="useBrandCard"
          v-for="p in items"
          :key="p.id"
          :id="p.id"
          :brand_name="p.brand_name"
          :logo="p.logo || p.src"
          :final_score="p.final_score || p.score"
          :score_label="p.score_label"
          :score_color="p.score_color"
        />
        <ProductCard
          v-else
          v-for="p in items"
          :key="p.id ?? p.src"
          :src="p.logo || p.src || '/src/assets/product1.png'"
          :alt="p.brand_name || p.alt || 'Marque'"
          :to="{ name: 'marque-detail', params: { id: p.id } }"
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

/* Tablette large */
@media (max-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
  }
  
  .heading {
    font-size: 24px;
    margin-bottom: 16px;
  }
  
  .grid-wrap {
    padding: 0 20px;
  }
}

/* Tablette */
@media (max-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }
  
  .heading {
    font-size: 22px;
    margin-bottom: 14px;
  }
  
  .grid-wrap {
    padding: 0 16px;
  }
  
  .product-bleed {
    padding: 14px 0 28px;
  }
}

/* Mobile */
@media (max-width: 480px) {
  .grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
  
  .heading {
    font-size: 20px;
    margin-bottom: 12px;
  }
  
  .grid-wrap {
    padding: 0 12px;
  }
  
  .product-bleed {
    padding: 12px 0 24px;
  }
}

/* Petit mobile */
@media (max-width: 380px) {
  .heading {
    font-size: 18px;
    margin-bottom: 10px;
  }
  
  .grid {
    gap: 14px;
  }
  
  .grid-wrap {
    padding: 0 10px;
  }
}
</style>

