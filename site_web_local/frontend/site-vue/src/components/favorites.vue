<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import ProductCard from '../components/ProductCard.vue'
import { listFavorites } from '../api/favorite'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const favorites = ref([])
const isLoading = ref(true)
const error = ref(null)

// Fonction pour récupérer les favoris
async function fetchFavorites() {
    if (!authStore.isAuthenticated || !authStore.currentUser) {
        error.value = "Vous devez être connecté pour voir vos favoris."
        isLoading.value = false
        return
    }
    
    isLoading.value = true
    error.value = null
    try {
        // Appelle la fonction API pour récupérer les favoris de l'utilisateur connecté
        favorites.value = await listFavorites(authStore.currentUser.id)
    } catch (err) {
        console.error("Erreur lors de la récupération des favoris:", err)
        error.value = "Impossible de charger les marques favorites."
    } finally {
        isLoading.value = false
    }
}

// Rediriger vers login si non connecté
onMounted(() => {
    if (!authStore.isAuthenticated) {
        router.push({ name: 'login' })
        return
    }
    fetchFavorites()
})


const favoriteBrands = computed(() => {
    // Pour l'affichage, nous prenons toutes les marques enregistrées comme favoris
    return favorites.value.map(fav => ({
        id: fav.brand_id,
        name: fav.brand_name || fav.name || 'Marque Inconnue',
        cover_url: fav.cover_url || '/src/assets/default-brand-cover.jpg', // Image par défaut
        to: { name: 'marque-detail', params: { id: fav.brand_id } }
    }))
})

// Groupement par catégories (inspiré par l'image du tableau de bord: Vêtements, Bijoux, Chaussures)
// C'est une simulation car FavoriteOut n'a pas la catégorie.
const favoriteCategories = [
    {
        name: 'Toutes les Marques Favorites',
        icon: '⭐️',
        items: favoriteBrands
    },
]

</script>

<template>
    <main class="favorites-page">
        <h1 class="page-title">Mes Marques Favorites</h1>
        
        <div v-if="authStore.currentUser" class="user-info">
            <p>Connecté en tant que <strong>{{ authStore.currentUser.firstname }} ({{ authStore.currentUser.username }})</strong></p>
        </div>

        <div v-if="isLoading" class="loading-message">Chargement des favoris...</div>
        <div v-else-if="error" class="error-message">{{ error }}</div>
        <div v-else-if="favorites.length === 0" class="empty-message">
            Vous n'avez pas encore de marques favorites.
        </div>

        <section v-else class="favorites-list">
            <div v-for="category in favoriteCategories" :key="category.name" class="category-section">
                <h2 class="category-title">{{ category.icon }} {{ category.name }} ({{ category.items.length }}
                    enregistrements)</h2>
                <div class="cards-grid">
                    <div class="new-list-card">
                        <span class="plus-icon">+</span>
                        <p>Nouvelle liste</p>
                    </div>

                    <ProductCard v-for="brand in category.items" :key="brand.id" :src="brand.cover_url"
                        :alt="brand.name" :to="brand.to" class="brand-favorite-card">
                        <div class="card-overlay">
                            <span class="card-name">{{ brand.name }}</span>
                        </div>
                    </ProductCard>
                </div>
            </div>
        </section>

    </main>
</template>

<style scoped>
.favorites-page {
    max-width: 90%;
    margin: 40px auto;
    padding: 0 10px;
}

.page-title {
    font-family: "Jersey 10", system-ui, sans-serif;
    font-weight: 400;
    font-size: 55px;
    color: #B70064;
    margin-bottom: 30px;
}

.category-title {
    font-family: Inter, system-ui, sans-serif;
    font-weight: 600;
    font-size: 20px;
    color: #000;
    margin-top: 40px;
    margin-bottom: 15px;
}

.cards-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
}

/* Style spécifique pour la carte des marques favorites */
.brand-favorite-card {
    position: relative;
}

.card-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(183, 0, 100, 0.85);
    /* Fond rose pour le texte */
    padding: 5px 10px;
    color: white;
    text-align: center;
}

.card-name {
    font-family: Inter, system-ui, sans-serif;
    font-weight: 400;
    font-size: 14px;
    display: block;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
}


/* Style de la carte "Nouvelle liste" (inspiré de l'image) */
.new-list-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 150px;
    /* Hauteur similaire aux ProductCard */
    background: #F8F5E8;
    border: 2px dashed #B70064;
    border-radius: 3px;
    cursor: pointer;
    transition: background .2s;
}

.new-list-card:hover {
    background: #F0EAD8;
}

.plus-icon {
    font-size: 40px;
    color: #B70064;
    line-height: 1;
}

.new-list-card p {
    margin: 5px 0 0;
    font-family: Inter, system-ui, sans-serif;
    font-size: 14px;
    font-weight: 500;
    color: #B70064;
}

.loading-message,
.error-message,
.empty-message {
    margin-top: 30px;
    text-align: center;
    font-family: Inter, system-ui, sans-serif;
    font-size: 18px;
    color: #B70064;
}

.error-message {
    color: red;
}
</style>