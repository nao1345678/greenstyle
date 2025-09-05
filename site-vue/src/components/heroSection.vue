<script setup>
import heels from '../assets/heels.png'
import ivy from '../assets/ivy.png'
import flower from '../assets/flower.png'
import kiss from '../assets/kiss.png'
import SearchBar from './SearchBar.vue'
import { ref } from 'vue'
const query = ref('')

const goSearch = () => console.log('TODO: router vers la page recherche')
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

/* contenu */
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
    bottom: -3%;
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
    top: -22%;
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

@media (max-width: 520px){
  .logo{ font-size: 64px; }
  .kiss{ right: 20px; bottom: 52px; height: 56px; }
}
</style>
