import { ref, computed } from 'vue'

interface User {
  id: string
  username: string
  firstname: string
  email: string
}

const currentUser = ref<User | null>(null)

export function useAuthStore() {
  // Charger l'utilisateur depuis localStorage au démarrage
  const loadUser = () => {
    const stored = localStorage.getItem('greenstyle_user')
    if (stored) {
      try {
        currentUser.value = JSON.parse(stored)
      } catch (e) {
        console.error('Erreur lors du chargement de l\'utilisateur:', e)
        localStorage.removeItem('greenstyle_user')
      }
    }
  }

  // Sauvegarder l'utilisateur dans localStorage
  const saveUser = (user: User) => {
    localStorage.setItem('greenstyle_user', JSON.stringify(user))
    currentUser.value = user
  }

  // Se connecter
  const login = (user: User) => {
    saveUser(user)
  }

  // Se déconnecter
  const logout = () => {
    localStorage.removeItem('greenstyle_user')
    currentUser.value = null
  }

  // Vérifier si l'utilisateur est connecté
  const isAuthenticated = computed(() => currentUser.value !== null)

  // Initialiser au chargement
  loadUser()

  return {
    currentUser: computed(() => currentUser.value),
    isAuthenticated,
    login,
    logout,
    loadUser
  }
}


