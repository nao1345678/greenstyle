<script setup>
import { useRoute } from 'vue-router'
import { ref } from 'vue'
import NavBar from '../../components/navbar.vue'
import Intro from '../../components/intro.vue'
import clothGrid from '../../components/clothGrid.vue'
const route = useRoute()

const Marques = ref('Marques');
const text = ref("Notre mission est de vous offrir un classement éthique des marques de vêtements, en se basant sur une analyse sans précédent. Pour cela, nous avons développé une méthodologie rigoureuse, s'appuyant sur l'examen minutieux de données précises : le prix, la pollution générée, les pratiques de travail éthiques, mais aussi des critères fins comme la taille de l'entreprise, les catégories de vêtements proposées ou les certifications obtenues. Chaque marque est ainsi passée au crible pour vous offrir une transparence totale.");
</script>

<template>
  <navBar />
  <div class="page-bg">
    <div class="intro">
      <Intro :title="Marques" :text="text" />
    </div>
    <div class="clothGrid">
      <clothGrid />
    </div>
  </div>
</template>

<style scoped> 

.page-bg{
  background: #fff5e6;
  min-height: 100svh;
  padding: 16px 0;
}

.intro{
  max-width: 70vw;
  margin-left: 2.5vw;
  padding: 0 24px;
}

.clothGrid{
  max-width: 90vw;
  margin-left: 2.5vw;
  margin-top: 5vh;
  padding: 0 24px;
}

</style>
