<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createUser, listUsers } from '@/api/users'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)
const error = ref(null)

const form = ref({
  username: '',
  firstname: '',
  email: '',
  password: ''
})

const switchMode = () => {
  isLogin.value = !isLogin.value
  error.value = null
  form.value = { username: '', firstname: '', email: '', password: '' }
}

const handleSubmit = async () => {
  loading.value = true
  error.value = null

  try {
    if (isLogin.value) {
      // Connexion : chercher l'utilisateur par email
      const users = await listUsers()
      const user = users.find(u => u.email === form.value.email)
      
      if (!user) {
        throw new Error('Email ou mot de passe incorrect')
      }
      
      // En production, il faudrait vérifier le mot de passe côté backend
      // Pour l'instant, on simule la connexion
      authStore.login(user)
      router.push({ name: 'home' })
    } else {
      // Inscription : créer un nouvel utilisateur
      if (!form.value.firstname) {
        throw new Error('Le prénom est requis')
      }
      
      const newUser = await createUser({
        username: form.value.username,
        firstname: form.value.firstname,
        email: form.value.email,
        password: form.value.password
      })
      
      authStore.login(newUser)
      router.push({ name: 'home' })
    }
  } catch (err) {
    console.error('Erreur:', err)
    error.value = err.message || 'Une erreur est survenue'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="container">
      <div class="form-card">
        <h1 class="title">{{ isLogin ? 'Connexion' : 'Inscription' }}</h1>
        
        <form @submit.prevent="handleSubmit" class="form">
          <div v-if="!isLogin" class="form-group">
            <label for="firstname">Prénom</label>
            <input
              id="firstname"
              v-model="form.firstname"
              type="text"
              required
              placeholder="Votre prénom"
            />
          </div>
          
          <div class="form-group">
            <label for="username">Nom d'utilisateur</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              placeholder="Votre nom d'utilisateur"
            />
          </div>
          
          <div class="form-group">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              placeholder="votre@email.com"
            />
          </div>
          
          <div class="form-group">
            <label for="password">Mot de passe</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              :placeholder="isLogin ? 'Votre mot de passe' : 'Minimum 6 caractères'"
              :minlength="isLogin ? undefined : 6"
            />
          </div>
          
          <div v-if="error" class="error-message">
            {{ error }}
          </div>
          
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? 'Chargement...' : (isLogin ? 'Se connecter' : 'Créer mon compte') }}
          </button>
        </form>
        
        <div class="switch-mode">
          <p>
            {{ isLogin ? "Pas encore de compte ?" : "Déjà un compte ?" }}
            <button @click="switchMode" class="switch-btn">
              {{ isLogin ? "S'inscrire" : "Se connecter" }}
            </button>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: calc(100vh - 85px);
  background: var(--page-bg, #DBC9AF);
  padding: 40px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  width: 100%;
  max-width: 450px;
}

.form-card {
  background: var(--panel-bg, #F4E8D7);
  border: 3px solid var(--green-dark, #017740);
  border-radius: 8px;
  padding: 32px;
  box-shadow: 0 6px 0 rgba(1,119,64,.35);
}

.title {
  font-family: "Jersey 10", system-ui, sans-serif;
  font-size: 36px;
  color: var(--green-dark, #017740);
  margin-bottom: 24px;
  text-align: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-family: system-ui, sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--green-dark, #017740);
}

.form-group input {
  padding: 12px;
  border: 2px solid var(--green-dark, #017740);
  border-radius: 4px;
  font-size: 16px;
  font-family: system-ui, sans-serif;
  background: white;
  transition: border-color .2s;
}

.form-group input:focus {
  outline: none;
  border-color: var(--green, #009C22);
}

.submit-btn {
  padding: 14px;
  background: var(--green, #009C22);
  color: white;
  border: 2px solid var(--green-dark, #017740);
  border-radius: 4px;
  font-size: 16px;
  font-weight: 600;
  font-family: "Jersey 10", system-ui, sans-serif;
  cursor: pointer;
  transition: background .2s;
  margin-top: 8px;
}

.submit-btn:hover:not(:disabled) {
  background: var(--green-dark, #017740);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  padding: 12px;
  background: #fee;
  border: 2px solid var(--pink, #B70064);
  border-radius: 4px;
  color: var(--pink, #B70064);
  font-size: 14px;
  text-align: center;
}

.switch-mode {
  margin-top: 24px;
  text-align: center;
  font-family: system-ui, sans-serif;
  color: var(--green-dark, #017740);
}

.switch-btn {
  background: none;
  border: none;
  color: var(--green, #009C22);
  text-decoration: underline;
  cursor: pointer;
  font-size: inherit;
  font-weight: 600;
  padding: 0;
  margin-left: 4px;
}

.switch-btn:hover {
  color: var(--green-dark, #017740);
}
</style>


