<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '@/components/navbar.vue'
import { getBrand } from '@/api/brand'
import { listFavorites, addFavorite, removeFavorite } from '@/api/favorite'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const brand = ref(null)
const loading = ref(true)
const error = ref(null)
const isFavorite = ref(false)
const favoriteId = ref(null)
const loadingFavorite = ref(false)

const brandId = computed(() => String(route.params.id || ''))

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

const checkFavorite = async () => {
  if (!authStore.isAuthenticated || !authStore.currentUser) {
    isFavorite.value = false
    return
  }

  try {
    const favorites = await listFavorites(authStore.currentUser.id)
    const favorite = favorites.find(f => f.brand_id === brandId.value)
    isFavorite.value = !!favorite
    favoriteId.value = favorite?.id || null
  } catch (err) {
    console.error('Erreur lors de la vérification des favoris:', err)
  }
}

const toggleFavorite = async () => {
  if (!authStore.isAuthenticated || !authStore.currentUser) {
    router.push({ name: 'login' })
    return
  }

  loadingFavorite.value = true
  try {
    if (isFavorite.value) {
      // Retirer des favoris
      if (favoriteId.value) {
        await removeFavorite(favoriteId.value)
        isFavorite.value = false
        favoriteId.value = null
      }
    } else {
      // Ajouter aux favoris
      const newFavorite = await addFavorite(
        authStore.currentUser.id,
        brandId.value,
        brand.value?.brand_name
      )
      isFavorite.value = true
      favoriteId.value = newFavorite.id
    }
  } catch (err) {
    console.error('Erreur lors de la modification des favoris:', err)
    error.value = 'Impossible de modifier les favoris'
  } finally {
    loadingFavorite.value = false
  }
}

onMounted(async () => {
  try {
    loading.value = true
    brand.value = await getBrand(brandId.value)
    await checkFavorite()
  } catch (err) {
    console.error('Erreur lors du chargement de la marque:', err)
    error.value = 'Marque non trouvée'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="marque-detail-page">
    <NavBar />
    <div v-if="loading" class="loading">
      Chargement de la marque...
    </div>
    
    <div v-else-if="error || !brand" class="error">
      {{ error || 'Marque non trouvée' }}
    </div>
    
    <div v-else class="container">
      <div class="header">
        <button @click="router.back()" class="back-btn">← Retour</button>
        <button
          v-if="authStore.isAuthenticated"
          @click="toggleFavorite"
          :disabled="loadingFavorite"
          class="favorite-btn"
          :class="{ active: isFavorite }"
        >
          {{ isFavorite ? '★ Retirer des favoris' : '☆ Ajouter aux favoris' }}
        </button>
        <button
          v-else
          @click="router.push({ name: 'login' })"
          class="favorite-btn"
        >
          Se connecter pour ajouter aux favoris
        </button>
      </div>

      <div class="brand-header">
        <div class="logo-section">
          <img
            v-if="brand.logo"
            :src="brand.logo"
            :alt="brand.brand_name"
            class="logo"
            @error="$event.target.src='/src/assets/product1.png'"
          />
          <div v-else class="logo-placeholder">
            {{ brand.brand_name?.charAt(0) || '?' }}
          </div>
        </div>
        
        <div class="brand-info">
          <h1 class="brand-name">{{ brand.brand_name }}</h1>
          
          <div v-if="brand.final_score !== null && brand.final_score !== undefined" class="score-section">
            <div class="score-badge" :style="{ backgroundColor: getScoreColor(brand.final_score) }">
              <span class="score-value">{{ brand.final_score.toFixed(1) }}</span>
              <span class="score-label">{{ getScoreLabel(brand.final_score) }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="details-grid">
        <div class="detail-card">
          <h3>Matières durables</h3>
          <p class="value">
            {{ brand.sustainable_materials !== null && brand.sustainable_materials !== undefined 
              ? `${brand.sustainable_materials}%` 
              : 'Non disponible' }}
          </p>
        </div>

        <div class="detail-card">
          <h3>Impact environnemental</h3>
          <p class="value">
            {{ brand.global_env_impact !== null && brand.global_env_impact !== undefined 
              ? brand.global_env_impact.toFixed(1) 
              : 'Non disponible' }}
          </p>
        </div>

        <div class="detail-card">
          <h3>Éthique du travail</h3>
          <p class="value">
            {{ brand.labor_ethics !== null && brand.labor_ethics !== undefined 
              ? brand.labor_ethics.toFixed(1) 
              : 'Non disponible' }}
          </p>
        </div>

        <div class="detail-card" v-if="brand.certifications">
          <h3>Certifications</h3>
          <p class="value">
            {{ typeof brand.certifications === 'string' 
              ? brand.certifications 
              : (Array.isArray(brand.certifications) ? brand.certifications.join(', ') : 'Aucune') }}
          </p>
        </div>

        <div class="detail-card" v-if="brand.country_production">
          <h3>Pays de production</h3>
          <p class="value">{{ brand.country_production }}</p>
        </div>

        <div class="detail-card" v-if="brand.website">
          <h3>Site web</h3>
          <a :href="brand.website" target="_blank" rel="noopener" class="website-link">
            {{ brand.website }}
          </a>
        </div>
      </div>

      <div v-if="brand.description" class="description-section">
        <h2>Description</h2>
        <p>{{ brand.description }}</p>
      </div>

      <!-- Section expliquant pourquoi la marque a cette note -->
      <div class="score-explanation-section">
        <h2>Pourquoi cette note ?</h2>
        <p class="score-summary">
          Le score final de <strong>{{ brand.final_score?.toFixed(1) || 'N/A' }}/10</strong> est calculé à partir de deux critères principaux :
          l'impact environnemental (<strong>{{ brand.global_env_impact?.toFixed(1) || 'N/A' }}/10</strong>) 
          et l'éthique du travail (<strong>{{ brand.labor_ethics?.toFixed(1) || 'N/A' }}/10</strong>).
        </p>
        
        <div class="criteria-grid">
          <div class="criterion-card">
            <h3>🌍 Impact Environnemental</h3>
            <div class="criterion-score">
              <span class="score-value">{{ brand.global_env_impact?.toFixed(1) || 'N/A' }}</span>
              <span class="score-max">/ 10</span>
            </div>
            <ul class="criterion-details">
              <li v-if="brand.country_production">
                <strong>Pays de production :</strong> {{ brand.country_production }}
                <span class="criterion-note">
                  (Production locale = +20pts, Europe = +10pts, Autres = +5pts)
                </span>
              </li>
              <li v-if="brand.sustainable_materials !== null && brand.sustainable_materials !== undefined">
                <strong>Matières durables :</strong> {{ brand.sustainable_materials }}%
                <span class="criterion-note">
                  (Max 20pts selon le pourcentage)
                </span>
              </li>
              <li v-if="brand.certifications">
                <strong>Certifications :</strong> {{ typeof brand.certifications === 'string' ? brand.certifications : (Array.isArray(brand.certifications) ? brand.certifications.join(', ') : 'Aucune') }}
                <span class="criterion-note">
                  (GOTS/B-Corp = +20pts, Bluesign = +15pts, etc.)
                </span>
              </li>
              <li v-if="brand.unsold_management">
                <strong>Gestion des invendus :</strong> {{ brand.unsold_management }}
                <span class="criterion-note">
                  (Pratiques positives = bonus, destruction = pénalité)
                </span>
              </li>
              <li v-if="brand.supply_chain_transparency">
                <strong>Transparence de la chaîne :</strong> {{ brand.supply_chain_transparency }}
                <span class="criterion-note">
                  (Transparence = bonus)
                </span>
              </li>
            </ul>
          </div>

          <div class="criterion-card">
            <h3>👷 Éthique du Travail</h3>
            <div class="criterion-score">
              <span class="score-value">{{ brand.labor_ethics?.toFixed(1) || 'N/A' }}</span>
              <span class="score-max">/ 10</span>
            </div>
            <ul class="criterion-details">
              <li>
                <strong>Conditions de travail :</strong>
                <span class="criterion-note">
                  Basé sur les rapports d'ONG, certifications Fair Trade, et transparence sur les salaires.
                </span>
              </li>
              <li v-if="brand.certifications && (typeof brand.certifications === 'string' ? brand.certifications.toLowerCase() : brand.certifications.join(',').toLowerCase()).includes('fair trade')">
                <strong>✓ Certification Fair Trade</strong>
                <span class="criterion-note">
                  (Commerce équitable = excellent score)
                </span>
              </li>
              <li v-if="brand.labor_badge">
                <strong>✓ Badge Éthique du Travail</strong>
                <span class="criterion-note">
                  (Marque reconnue pour ses pratiques éthiques)
                </span>
              </li>
            </ul>
          </div>
        </div>

        <div class="final-score-calculation">
          <h3>📊 Calcul du score final</h3>
          <p>
            Score final = (Impact Environnemental + Éthique du Travail) ÷ 2
          </p>
          <div class="calculation-formula">
            <span v-if="brand.global_env_impact !== null && brand.labor_ethics !== null">
              ({{ brand.global_env_impact.toFixed(1) }} + {{ brand.labor_ethics.toFixed(1) }}) ÷ 2 = 
              <strong>{{ brand.final_score?.toFixed(1) || 'N/A' }}/10</strong>
            </span>
            <span v-else>
              Score en cours de calcul...
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.marque-detail-page {
  min-height: calc(100vh - 85px);
  background: var(--page-bg, #DBC9AF);
  padding: 40px 20px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.back-btn {
  padding: 10px 20px;
  background: var(--panel-bg, #F4E8D7);
  border: 2px solid var(--green-dark, #017740);
  border-radius: 4px;
  color: var(--green-dark, #017740);
  font-family: system-ui, sans-serif;
  font-size: 16px;
  cursor: pointer;
  transition: background .2s;
}

.back-btn:hover {
  background: var(--green, #009C22);
  color: white;
}

.favorite-btn {
  padding: 10px 20px;
  background: var(--green, #009C22);
  border: 2px solid var(--green-dark, #017740);
  border-radius: 4px;
  color: white;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 16px;
  cursor: pointer;
  transition: background .2s;
}

.favorite-btn:hover:not(:disabled) {
  background: var(--green-dark, #017740);
}

.favorite-btn.active {
  background: var(--pink, #B70064);
  border-color: var(--pink, #B70064);
}

.favorite-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.brand-header {
  display: flex;
  gap: 32px;
  margin-bottom: 40px;
  background: var(--panel-bg, #F4E8D7);
  padding: 32px;
  border-radius: 8px;
  border: 3px solid var(--green-dark, #017740);
}

.logo-section {
  flex-shrink: 0;
}

.logo {
  width: 150px;
  height: 150px;
  object-fit: contain;
  border-radius: 8px;
  background: white;
  padding: 12px;
}

.logo-placeholder {
  width: 150px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--green, #009C22);
  color: white;
  font-size: 64px;
  font-weight: bold;
  border-radius: 8px;
  font-family: "Jersey 10", system-ui, sans-serif;
}

.brand-info {
  flex: 1;
}

.brand-name {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 48px;
  color: var(--green-dark, #017740);
  margin: 0 0 20px;
}

.score-section {
  margin-top: 16px;
}

.score-badge {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  padding: 16px 24px;
  border-radius: 8px;
  color: white;
  box-shadow: 0 4px 8px rgba(0,0,0,.2);
}

.score-value {
  font-size: 36px;
  font-weight: bold;
  font-family: system-ui, sans-serif;
}

.score-label {
  font-size: 14px;
  margin-top: 4px;
  font-family: system-ui, sans-serif;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.detail-card {
  background: var(--panel-bg, #F4E8D7);
  padding: 20px;
  border-radius: 8px;
  border: 2px solid var(--green-dark, #017740);
}

.detail-card h3 {
  font-family: system-ui, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--green-dark, #017740);
  margin: 0 0 8px;
  text-transform: uppercase;
}

.detail-card .value {
  font-family: system-ui, sans-serif;
  font-size: 18px;
  color: var(--green-dark, #017740);
  margin: 0;
}

.website-link {
  color: var(--green, #009C22);
  text-decoration: none;
  word-break: break-all;
}

.website-link:hover {
  text-decoration: underline;
}

.description-section {
  background: var(--panel-bg, #F4E8D7);
  padding: 32px;
  border-radius: 8px;
  border: 3px solid var(--green-dark, #017740);
}

.description-section h2 {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 32px;
  color: var(--green-dark, #017740);
  margin: 0 0 16px;
}

.description-section p {
  font-family: system-ui, sans-serif;
  font-size: 16px;
  line-height: 1.6;
  color: var(--green-dark, #017740);
  margin: 0;
}

.score-explanation-section {
  background: var(--panel-bg, #F4E8D7);
  padding: 32px;
  border-radius: 8px;
  border: 3px solid var(--green-dark, #017740);
  margin-top: 40px;
}

.score-explanation-section h2 {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 32px;
  color: var(--green-dark, #017740);
  margin: 0 0 20px;
}

.score-summary {
  font-family: system-ui, sans-serif;
  font-size: 18px;
  line-height: 1.6;
  color: var(--green-dark, #017740);
  margin-bottom: 32px;
  padding: 16px;
  background: rgba(1, 119, 64, 0.1);
  border-radius: 8px;
}

.criteria-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.criterion-card {
  background: white;
  padding: 24px;
  border-radius: 8px;
  border: 2px solid var(--green-dark, #017740);
}

.criterion-card h3 {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 24px;
  color: var(--green-dark, #017740);
  margin: 0 0 16px;
}

.criterion-score {
  display: flex;
  align-items: baseline;
  margin-bottom: 20px;
  padding: 12px;
  background: rgba(1, 119, 64, 0.1);
  border-radius: 6px;
}

.criterion-score .score-value {
  font-size: 32px;
  font-weight: bold;
  color: var(--green-dark, #017740);
  font-family: system-ui, sans-serif;
}

.criterion-score .score-max {
  font-size: 18px;
  color: var(--green-dark, #017740);
  margin-left: 4px;
  font-family: system-ui, sans-serif;
}

.criterion-details {
  list-style: none;
  padding: 0;
  margin: 0;
}

.criterion-details li {
  font-family: system-ui, sans-serif;
  font-size: 14px;
  line-height: 1.8;
  color: var(--green-dark, #017740);
  margin-bottom: 12px;
  padding-left: 20px;
  position: relative;
}

.criterion-details li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--green, #009C22);
  font-weight: bold;
}

.criterion-details li strong {
  color: var(--green-dark, #017740);
}

.criterion-note {
  display: block;
  font-size: 12px;
  color: #666;
  font-style: italic;
  margin-top: 4px;
}

.final-score-calculation {
  background: white;
  padding: 24px;
  border-radius: 8px;
  border: 2px solid var(--green-dark, #017740);
  margin-top: 24px;
}

.final-score-calculation h3 {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 24px;
  color: var(--green-dark, #017740);
  margin: 0 0 16px;
}

.final-score-calculation p {
  font-family: system-ui, sans-serif;
  font-size: 16px;
  color: var(--green-dark, #017740);
  margin-bottom: 12px;
}

.calculation-formula {
  font-family: system-ui, sans-serif;
  font-size: 18px;
  color: var(--green-dark, #017740);
  padding: 16px;
  background: rgba(1, 119, 64, 0.1);
  border-radius: 6px;
  text-align: center;
}

.calculation-formula strong {
  font-size: 24px;
  color: var(--green, #009C22);
}

.loading, .error {
  text-align: center;
  padding: 40px 20px;
  font-size: 18px;
  color: var(--green-dark, #017740);
}

.error {
  color: var(--pink, #B70064);
}

@media (max-width: 768px) {
  .brand-header {
    flex-direction: column;
    text-align: center;
  }
  
  .logo, .logo-placeholder {
    margin: 0 auto;
  }
  
  .brand-name {
    font-size: 36px;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }
}
</style>

