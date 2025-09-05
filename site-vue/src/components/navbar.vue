<script setup>
const props = defineProps({
  logoSrc: { type: String, default: '/src/assets/heel-plant.png' },
})
</script>

<template>
  <header class="nav-root">
    <div class="nav-inner">
      <img class="logo" :src="logoSrc" alt="Greenstyle" />

      <nav aria-label="Navigation principale">
        <a class="link left-1" href="#">Recherche détaillée</a>
        <a class="link left-2" href="#">Tableau de bord</a>
        <a class="link right-1" href="#">À propos de nous</a>
        <a class="link right-2" href="#">Mon compte</a>
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
</style>
