<script setup>
import { RouterLink } from 'vue-router'

const props = defineProps({
  id: { type: [String, Number], required: true },
  brand_name: { type: String, default: '' },
  logo: { type: String, default: null },
  final_score: { type: Number, default: null },
  score_label: { type: String, default: '' },
  score_color: { type: String, default: 'yellow' },
})

const getScoreColor = (score) => {
  if (score >= 8) return '#009C22' // green
  if (score >= 6) return '#FFC107' // yellow
  if (score >= 4) return '#FF9800' // orange
  return '#F44336' // red
}

const getScoreLabel = (score) => {
  if (score >= 8) return 'Excellent'
  if (score >= 6) return 'Bon'
  if (score >= 4) return 'Moyen'
  return 'Faible'
}

const displayScore = props.final_score !== null ? props.final_score : null
const displayLabel = props.score_label || (displayScore ? getScoreLabel(displayScore) : '')
const displayColor = props.score_color || (displayScore ? getScoreColor(displayScore) : '#999')
const imageSrc = props.logo || '/src/assets/product1.png'
</script>

<template>
  <RouterLink class="brand-card" :to="{ name: 'marque-detail', params: { id: id } }">
    <div class="image-container">
      <img :src="imageSrc" :alt="brand_name || 'Marque'" loading="lazy" @error="$event.target.src='/src/assets/product1.png'" />
      <div v-if="displayScore !== null" class="score-badge" :style="{ backgroundColor: displayColor }">
        {{ displayScore.toFixed(1) }}
      </div>
    </div>
    <div class="brand-info">
      <h3 class="brand-name">{{ brand_name || 'Marque' }}</h3>
      <div v-if="displayLabel" class="score-label" :style="{ color: displayColor }">
        {{ displayLabel }}
      </div>
    </div>
  </RouterLink>
</template>

<style scoped>
.brand-card {
  display: block;
  text-decoration: none;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid rgba(104,183,113,.3);
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  transition: transform .2s, box-shadow .2s, border-color .2s;
}

.brand-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 16px rgba(0,0,0,.15);
  border-color: var(--pink, #B70064);
}

.image-container {
  position: relative;
  width: 100%;
  aspect-ratio: 4/3;
  overflow: hidden;
  background: var(--product-bg, #FFF5E6);
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  padding: 12px;
  display: block;
}

.score-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 4px 10px;
  border-radius: 16px;
  color: white;
  font-weight: bold;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0,0,0,.2);
  font-family: system-ui, -apple-system, sans-serif;
}

.brand-info {
  padding: 12px;
  background: white;
}

.brand-name {
  margin: 0 0 6px;
  font-size: 16px;
  font-weight: 600;
  color: var(--green-dark, #017740);
  font-family: system-ui, -apple-system, sans-serif;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.score-label {
  font-size: 12px;
  font-weight: 500;
  font-family: system-ui, -apple-system, sans-serif;
}

@media (max-width: 768px) {
  .brand-card {
    border-radius: 6px;
  }
  
  .score-badge {
    font-size: 12px;
    padding: 3px 8px;
  }
  
  .brand-name {
    font-size: 14px;
  }
  
  .score-label {
    font-size: 11px;
  }
}
</style>


