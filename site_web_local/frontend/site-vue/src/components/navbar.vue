<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  logoSrc: { type: String, default: '/src/assets/heel-plant.png' },
})

const authStore = useAuthStore()
</script>

<template>
  <header class="nav-root">
    <div class="nav-inner">
      <RouterLink :to="{ name: 'home' }">
        <img class="logo" :src="logoSrc" alt="Greenstyle" />
      </RouterLink>

      <nav aria-label="Navigation principale">
        <RouterLink class="link left-1" :to="{ name: 'recherche' }">Recherche détaillée</RouterLink>
        <RouterLink class="link left-2" :to="{ name: 'favorites' }">Tableau de bord</RouterLink>
        <RouterLink class="link right-1" :to="{ name: 'a-propos' }">À propos de nous</RouterLink>
        <template v-if="!authStore.isAuthenticated">
          <RouterLink class="link right-2" :to="{ name: 'login' }">Connexion</RouterLink>
        </template>
        <template v-else>
          <RouterLink class="link right-2" :to="{ name: 'favorites' }">Mes favoris</RouterLink>
          <button @click="authStore.logout(); $router.push({ name: 'home' })" class="link logout-btn">Déconnexion</button>
        </template>
      </nav>

      <div class="nav-rule" aria-hidden="true"></div>
    </div>
  </header>
</template>

<style scoped>
.nav-root{
  background: var(--page-bg);
  position: sticky; top:0; left:0; right:0; z-index:1000;
}

.nav-inner{
  width: 100%;
  height: 85px;
  position: relative;
}

.nav-rule{
  position: absolute;
  left: 5%;
  top: 80px;
  width: 90vw;
  height: 1px;
  background: #fff;
  transform: scaleY(.5);
  transform-origin: top left;
  z-index: 2;
  pointer-events: none;
}

.logo{
  position: absolute;
  top: 8px;
  width: 61px;
  height: auto;
}

.link{
  position: absolute;
  top: 34px;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 17px;
  line-height: 1;
  color: var(--green-dark);
  text-decoration: none;
  text-shadow: 5px 5px 8px #ffffff;
}
.link:hover{ text-decoration: underline; }
.link:focus-visible{ outline: 2px solid var(--green); outline-offset: 2px; }

.left-1 { left: 4.5%; }
.left-2 { left: 14.5%; }
.right-1{ right: 15%; }
.right-2{ right: 5%; }
.right-3{ right: 12%; }

.logout-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 17px;
  line-height: 1;
  color: var(--green-dark);
  text-decoration: none;
  text-shadow: 5px 5px 8px #ffffff;
  padding: 0;
}

.logout-btn:hover {
  text-decoration: underline;
}

/* Tablette */
@media (max-width: 1024px) {
  .nav-inner {
    height: 75px;
  }
  
  .logo {
    width: 55px;
    top: 6px;
  }
  
  .link {
    font-size: 15px;
    top: 30px;
  }
  
  .left-1 { left: 4%; }
  .left-2 { left: 13%; }
  .right-1 { right: 14%; }
  .right-2 { right: 4%; }
  
  .nav-rule {
    top: 72px;
  }
}

/* Mobile */
@media (max-width: 768px) {
  .nav-inner {
    height: 65px;
  }
  
  .logo {
    width: 48px;
    top: 5px;
  }
  
  .link {
    font-size: 13px;
    top: 28px;
  }
  
  .left-1 { left: 3.5%; }
  .left-2 { left: 12%; }
  .right-1 { right: 13%; }
  .right-2 { right: 3.5%; }
  
  .nav-rule {
    top: 62px;
    width: 95vw;
    left: 2.5%;
  }
}

/* Petit mobile - Menu compact */
@media (max-width: 520px) {
  .nav-inner {
    height: 60px;
  }
  
  .logo {
    width: 44px;
    top: 4px;
    left: 50%;
    transform: translateX(-50%);
  }
  
  .link {
    font-size: 11px;
    top: 36px;
    white-space: nowrap;
  }
  
  .left-1 { left: 3%; }
  .left-2 { left: 11%; }
  .right-1 { right: 12%; }
  .right-2 { right: 3%; }
  
  .nav-rule {
    top: 58px;
    width: 96vw;
    left: 2%;
  }
}

/* Très petit mobile */
@media (max-width: 380px) {
  .link {
    font-size: 10px;
  }
  
  .left-1 { left: 2%; }
  .left-2 { left: 10%; }
  .right-1 { right: 11%; }
  .right-2 { right: 2%; }
}
</style>
