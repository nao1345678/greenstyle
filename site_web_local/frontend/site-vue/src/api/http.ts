import axios from 'axios'

// Configuration de l'URL du backend
// En développement : utilise le proxy Vite (/api -> http://localhost:8000)
// En production : utilise VITE_API_URL ou par défaut http://localhost:8000
const getBaseURL = () => {
  // Si VITE_API_URL est définie (production), l'utiliser
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // En mode développement, utiliser le proxy Vite
  if (import.meta.env.DEV) {
    return '/api'
  }
  
  // Par défaut (production sans variable), utiliser localhost:8000
  return 'http://localhost:8000'
}

export const http = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
})

// Ajouter un intercepteur pour gérer les erreurs
http.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('Erreur API:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)
