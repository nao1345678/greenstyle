import { http } from "./http" // Assurez-vous que le chemin est correct

// Modèles basés sur votre schéma FavoriteOut
export interface FavoriteOut {
    id: string
    user_id: string
    brand_id: string
    name: string | null 
    cover_url: string | null
    content: string | null
    brand_name: string | null // Nom de la marque favorite
}

// Fonction pour lister les favoris d'un utilisateur spécifique
export const listUserFavorites = async (userId: string) => {
    // Appel à GET /favorites/?user_id={userId}
    const response = await http.get<FavoriteOut[]>(`/favorites/?user_id=${userId}`)
    return response.data
}