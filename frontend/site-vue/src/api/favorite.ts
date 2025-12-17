import { http } from "./http"
import type { BrandOut } from "./brand" // Assurez-vous que BrandOut est importé

// Correspond au FavoriteOut de votre modèle backend
export interface FavoriteOut {
    id: string
    user_id: string
    brand_id: string
    name?: string | null
    cover_url?: string | null
    content?: string | null
    brand_name?: string | null // Important pour l'affichage
}

/**
 * Récupère la liste des favoris pour un utilisateur spécifique.
 * @param userId 
 */
export async function listFavorites(userId: string) {
    const { data } = await http.get<FavoriteOut[]>(`/favorites/?user_id=${userId}`)
    return data
}

