<script setup>
const props = defineProps({
  // mets ton image ici : /src/assets/heel-plant.png (ou autre)
  logoSrc: { type: String, default: '/src/assets/heel-plant.png' },
})
</script>

<template>
  <header class="nav-root">
    <div class="nav-inner">
      <img class="logo" :src="logoSrc" alt="Greenstyle" />

      <!-- LEFT -->
      <a class="link left-1" href="#">Recherche détaillée</a>
      <a class="link left-2" href="#">Tableau de bord</a>

      <!-- RIGHT -->
      <a class="link right-1" href="#">À propos de nous</a>
      <a class="link right-2" href="#">Mon compte</a>

      <div class="nav-rule" aria-hidden="true"></div>
    </div>
  </header>
</template>

<style>
:root{
  --bg: #DAC9AF;
  --green: #2F6A35;
}

/* barre entière */
.nav-root{
  background: var(--bg);
}

/* conteneur fixe 1280px pour coller aux positions Figma */
.nav-inner{
  width: 100vw;
  height:85px;             /* hauteur suffisante pour le "Top: 76px" visuel */
  margin: 0;
  position: relative;        /* permet les positions absolues des liens */
}

/* hairline sous la nav */
.nav-rule{
  position: absolute;
  left: 104px;      /* Figma */
  top: 80px;       /* Figma */
  width: 1100px;    /* Figma */
  height: 1px;      /* ligne pleine */
  background: #fff; /* BLANC */
  transform: scaleY(0.5);     /* rendu visuel 0.5 px */
  transform-origin: top left;
  z-index: 2;
  pointer-events: none;
}

/* logo à gauche (ajuste la taille si besoin) */
.logo{
  position: absolute;
  left: 24px;                /* marge visuelle à gauche */
  top: 0px;
  width: 61px;               /* ~taille perçue sur la capture */
  height: auto;
}

/* style commun des liens */
.link{
  position: absolute;
  top: 34px;                 /* aligne verticalement tous les items */
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 17px;           /* hauteur perçue 17px dans Figma */
  line-height: 1;
  color: var(--green);
  text-decoration: none;
  /* petit relief comme sur la capture */
  text-shadow: 5px 5px 8px #ffffff;
}

/* positions EXACTES (Left) issues de ta maquette */
.left-1 { left: 93px; }      /* Recherche détaillée */
.left-2 { left: 255px; }     /* Tableau de bord */
.right-1{ left: 1026px; }    /* À propos de nous */
.right-2{ left: 1175px; }    /* Mon compte */

.link:hover{ text-decoration: underline; }
</style>
