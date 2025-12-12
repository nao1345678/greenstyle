<script setup lang="ts">
import NavBar from '../components/navbar.vue'
import { onMounted, ref, computed } from 'vue'
import { listUserFavorites, FavoriteOut } from '../api/favorites' // 💡 NOUVEL IMPORT

// Le `userId` doit être dynamique. Pour l'exemple, nous utilisons un ID fixe.
// En réalité, cet ID viendrait d'un store Vuex/Pinia ou d'un système d'authentification.
const USER_ID_MOCK = "60c72b2f8e12d5001f8b4567"; // Remplacer par un ID utilisateur valide si possible

const allFavorites = ref<FavoriteOut[]>([]) // Pour stocker tous les favoris
const isLoading = ref(true)

// --- Logique pour agréger les favoris par "liste" (name) ---
// Cette fonction regroupe les marques favorites par leur champ 'name' (ex: Vêtements, Bijoux).
const groupedFavorites = computed(() => {
    const groups: Record<string, FavoriteOut[]> = {}

    // 1. Initialiser une liste "Nouvelle liste" (comme dans la maquette)
    groups['Nouvelle liste'] = []

    // 2. Grouper les favoris existants par leur nom de liste (name)
    allFavorites.value.forEach(fav => {
        const listName = fav.name || 'Divers'; // Utiliser 'Divers' ou une autre valeur si 'name' est null

        if (!groups[listName]) {
            groups[listName] = []
        }
        groups[listName].push(fav)
    })

    // 3. Convertir l'objet en un tableau de listes pour l'affichage
    const categories = Object.keys(groups).map(name => ({
        name: name,
        count: groups[name].length,
        brands: groups[name]
    }));

    // Assurer que "Nouvelle liste" est toujours en premier (et n'a pas de marques)
    const newList = categories.find(c => c.name === 'Nouvelle liste') || { name: 'Nouvelle liste', count: 0, brands: [] }
    const otherLists = categories.filter(c => c.name !== 'Nouvelle liste' && c.count > 0);

    return [newList, ...otherLists].sort((a, b) => {
        // Garder "Nouvelle liste" en tête, puis trier les autres par nom
        if (a.name === 'Nouvelle liste') return -1;
        if (b.name === 'Nouvelle liste') return 1;
        return a.name.localeCompare(b.name);
    });
})

// --- Données pour l'historique (maintenu statique ou à remplacer par une autre API si nécessaire) ---
const history = ref([
    { brand: 'Louis Vuitton', url: 'www.louisvuitton.com' },
    { brand: 'Hermes', url: 'www.hermes.com' },
    { brand: 'Louis Vuitton', url: 'www.louisvuitton.com' },
    { brand: 'Hermes', url: 'www.hermes.com' },
    { brand: 'Louis Vuitton', url: 'www.louisvuitton.com' },
])

// --- Chargement des données au montage ---
onMounted(async () => {
    try {
        // Récupération des favoris de l'utilisateur
        const data = await listUserFavorites(USER_ID_MOCK)
        allFavorites.value = data
    } catch (error) {
        console.error("Erreur lors du chargement des favoris:", error)
        // Vous pouvez afficher un message d'erreur à l'utilisateur ici
    } finally {
        isLoading.value = false
    }
})
</script>

<template>
    <NavBar />
    <main class="dashboard-page">
        <h1 class="page-title">Tableau de bord</h1>

        <div v-if="isLoading" class="loading-message">Chargement des favoris...</div>

        <div v-else>
            <section class="history-section">
                <h2 class="section-title">Historique</h2>
                <table class="history-table">
                    <tbody>
                        <tr v-for="(item, index) in history" :key="index">
                            <td class="brand-name">{{ item.brand }}</td>
                            <td class="brand-url">{{ item.url }}</td>
                        </tr>
                    </tbody>
                </table>
            </section>

            <section class="favorites-section">
                <h2 class="section-title">Listes de marques favorites</h2>
                <div class="category-grid">
                    <div v-for="category in groupedFavorites" :key="category.name" class="category-card"
                        :class="{ 'new-list-card': category.name === 'Nouvelle liste' }">
                        <div class="card-content">
                            <span v-if="category.name === 'Nouvelle liste'" class="card-icon new-list-icon">+</span>
                            <span v-else class="card-icon category-icon">📁</span>

                            <p class="card-name">{{ category.name }}</p>
                            <p v-if="category.count > 0" class="card-count">{{ category.count }} enregistrements</p>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    </main>
</template>

<style scoped>
/* Utilisation des variables de style définies dans index.vue et style.css */

.dashboard-page {
    padding: 24px 16px;
    max-width: 1000px;
    margin: 0 auto;
}

.page-title {
    color: var(--pink);
    /* #B70064 */
    font-family: "Jersey 10", system-ui, sans-serif;
    font-size: 40px;
    margin-top: 0;
    border-bottom: 3px solid var(--pink);
    display: inline-block;
    padding-bottom: 5px;
}

.section-title {
    font-family: Inter, sans-serif;
    font-weight: 600;
    font-size: 18px;
    margin-top: 30px;
    margin-bottom: 10px;
    color: #000;
}

/* --- Styles Historique --- */
.history-section {
    margin-bottom: 40px;
}

.history-table {
    width: min(500px, 100%);
    /* Limiter la largeur de l'historique comme dans la maquette */
    border-collapse: collapse;
    margin-top: 10px;
}

.history-table td {
    padding: 5px 15px;
    border: none;
    font-family: Inter, sans-serif;
    font-size: 14px;
}

/* Couleurs de fond pour l'alternance (Louis Vuitton / Hermes) */
.history-table tr:nth-child(2n+1) td {
    background-color: #F8D8E0;
    /* Rose clair */
}

.history-table tr:nth-child(2n) td {
    background-color: #F8C6D4;
    /* Rose légèrement plus foncé */
}

.brand-url {
    font-weight: 300;
}

/* --- Styles Listes de favoris (Cartes) --- */
.category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 20px;
    margin-top: 15px;
}

.category-card {
    background-color: var(--panel-bg);
    /* #F4E8D7 */
    border: 3px solid var(--page-bg);
    /* #DBC9AF */
    border-radius: 8px;
    padding: 20px;
    height: 180px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    box-shadow: 0 4px 0 rgba(0, 0, 0, 0.1);
    /* Simulation de l'ombre portée */
}

.card-content {
    /* Center all content inside the card */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.card-icon {
    font-size: 30px;
    font-weight: 100;
    line-height: 1;
}

.new-list-icon {
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
    font-weight: 300;
    border: 3px solid #000;
    border-radius: 50%;
    margin-bottom: 10px;
}

.new-list-card {
    cursor: pointer;
    opacity: 0.8;
}

.category-icon {
    font-size: 50px;
    /* Taille plus grande pour l'icône de dossier générique */
    margin-bottom: 5px;
}

.card-name {
    font-weight: 600;
    margin: 5px 0 0;
}

.card-count {
    font-size: 12px;
    color: #555;
    margin-top: 2px;
}

.loading-message {
    text-align: center;
    margin-top: 50px;
    font-size: 18px;
    color: #555;
}
</style>