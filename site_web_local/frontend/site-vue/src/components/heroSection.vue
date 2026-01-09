<script setup>
import heels from '../assets/heels.png'
import ivy from '../assets/ivy.png'
import flower from '../assets/flower.png'
import kiss from '../assets/kiss.png'
import SearchBar from './SearchBar.vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const query = ref('')

const goSearch = () => {
  if (query.value.trim()) {
    router.push({ name: 'recherche', query: { q: query.value } })
  } else {
    router.push({ name: 'recherche' })
  }
}

</script>

<template>
  <section class="hero">
    <div class="window">
      <div class="titlebar">
        <span class="title">Greenstyle</span>
        <div class="controls"><i></i><i></i></div>
      </div>

      <div class="window-body">
        
        <img class="decor ivy"    :src="ivy"    alt="" />
        <div class="decor heels">
            <img :src="heels" alt="">
        </div>
        <img class="decor flower" :src="flower" alt="" />
        <div class="decor kiss">
            <img :src="kiss" alt="">
        </div>

        
        <h1 class="logo">Greenstyle</h1>

        
        <button class="cta" @click="goSearch">Aller à la page recherche</button>
      </div>
    </div>
    <SearchBar v-model="query" @search="goSearch" />
  </section>
</template>

<style scoped>
.hero{
  position: relative;          
  background: var(--page-bg);   
  padding: 24px 16px 64px;
  overflow: visible;
}


.hero::before{
  content: "";
  position: absolute;
  left: 50%;
  top: -156px;               
  transform: translateX(-50%);
  width: min(1027px, 92vw);
  height: 400px; 
  background: url("/src/assets/glow-ellipse.png") no-repeat center / contain;
  opacity: 1;
  pointer-events: none;
  z-index: 0;
  transform: translateX(-50%) scale(1.6);
  transform-origin: center top;
  pointer-events: none;
  z-index: 0;
}

.window,
.searchbar { position: relative; z-index: 1; }
.window{
  width: min(510px, 92vw);
  margin: 0 auto;
  border: 3px solid var(--green-dark);
  border-radius: 8px;
  background: var(--panel-bg);
  box-shadow: 0 6px 0 rgba(1,119,64,.35);
}
.titlebar{
  height: 28px;
  display:flex; align-items:center; justify-content:space-between;
  padding: 0 10px;
  color: #e9ffef;
  background: linear-gradient(180deg, var(--green) 0%, var(--green-dark) 100%);
  border-bottom: 3px solid var(--green-dark);
  border-radius: 6px 6px 0 0;
  font-weight: 700;
  font-size: 12px;
}
.titlebar .controls i{
  display:inline-block;width:10px;height:10px;margin-left:6px;
  border:2px solid #0b5a34;border-radius:2px;background:#c7f7d5;
}
.title {
    font-family: "Jersey 10", system-ui, sans-serif;
    text-shadow: 4px 4px 10px #000000;
    font-weight: 400;
}

.window-body{
  position: relative;
  min-height: 260px;
  padding: 28px 18px 64px;
  background: transparent;;
  overflow: hidden;
}

.logo{
    font-family: "Jersey 10", system-ui, sans-serif;
    text-shadow: 11px 10px 12px #000000;
    font-weight: 400;
    font-size: 110px;
    line-height: 1;
    color: #ffffff;
    position: absolute;
    z-index: 10;
    bottom: 17%;
    right: 9%;
}

.decor { position: absolute; pointer-events: none; }
.heels {
    left: -5%;
    width: 34%;
    top: 11%;
    height: 33%;
}
.heels img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transform: rotate(31.34deg);
  transform-origin: center;
  display: block;
}


.cta{
  position: absolute;
  right: 18px; bottom: 16px;
  padding: 2.5px 14px;
  border: 2px solid var(--green-dark);
  height: 20px;
  background: var(--green);
  color: #fff;
  font-weight: 400;
  cursor: pointer;
  font-family: "Jersey 10", system-ui, sans-serif;
  text-shadow: 11px 10px 12px #000000;
}
.cta:hover{ filter: brightness(1.05); }


.decor{ position:absolute; pointer-events:none; }

.ivy{
    left: -15%;
    top: 45%;
    height: 172px;
}
.flower{ 
    right: -25%;
    top: -11%;
    height: 230px;
}
.kiss{
  left: 70%;
  width: 34%;
  top: 50%;
  height: 29%;
}

.kiss img{
  width: 100%;
  height: 100%;
  object-fit: contain;
  transform: rotate(-20deg);
  transform-origin: center;
  display: block;
}

/* Tablette */
@media (max-width: 768px) {
  .hero {
    padding: 20px 12px 48px;
  }
  
  .window {
    width: min(480px, 92vw);
  }
  
  .logo {
    font-size: 80px;
    bottom: 15%;
    right: 8%;
  }
  
  .window-body {
    min-height: 240px;
    padding: 24px 16px 56px;
  }
  
  .heels {
    width: 30%;
    left: -8%;
  }
  
  .ivy {
    left: -18%;
    height: 140px;
  }
  
  .flower {
    right: -28%;
    height: 200px;
  }
  
  .kiss {
    left: 65%;
    width: 30%;
  }
  
  .cta {
    font-size: 14px;
    padding: 2px 12px;
    height: 22px;
  }
  
  .hero::before {
    width: min(900px, 92vw);
    height: 350px;
    transform: translateX(-50%) scale(1.4);
  }
}

/* Mobile */
@media (max-width: 520px) {
  .hero {
    padding: 16px 8px 40px;
  }
  
  .window {
    width: min(420px, 94vw);
  }
  
  .titlebar {
    height: 26px;
    font-size: 11px;
    padding: 0 8px;
  }
  
  .titlebar .controls i {
    width: 8px;
    height: 8px;
  }
  
  .logo {
    font-size: 64px;
    bottom: 12%;
    right: 6%;
  }
  
  .window-body {
    min-height: 220px;
    padding: 20px 12px 48px;
  }
  
  .heels {
    width: 28%;
    left: -10%;
    top: 10%;
    height: 28%;
  }
  
  .ivy {
    left: -20%;
    top: 42%;
    height: 120px;
  }
  
  .flower {
    right: -30%;
    top: -15%;
    height: 180px;
  }
  
  .kiss {
    left: 60%;
    width: 28%;
    top: 48%;
    height: 25%;
  }
  
  .cta {
    font-size: 12px;
    padding: 2px 10px;
    height: 20px;
    right: 12px;
    bottom: 12px;
  }
  
  .hero::before {
    width: min(800px, 94vw);
    height: 300px;
    transform: translateX(-50%) scale(1.2);
    top: -120px;
  }
}

/* Petit mobile */
@media (max-width: 380px) {
  .logo {
    font-size: 52px;
    bottom: 10%;
    right: 4%;
  }
  
  .window-body {
    min-height: 200px;
    padding: 16px 10px 44px;
  }
  
  .heels {
    width: 25%;
    left: -12%;
  }
  
  .ivy {
    height: 100px;
  }
  
  .flower {
    height: 150px;
  }
  
  .kiss {
    width: 25%;
    height: 22%;
  }
  
  .cta {
    font-size: 11px;
    padding: 1px 8px;
    height: 18px;
  }
}
</style>
