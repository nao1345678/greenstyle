<script setup>
import { computed } from 'vue'

const props = defineProps({
  name:        { type: String, required: true },
  rating:      { type: Number, default: 0 },
  priceLevel:  { type: Number, default: 1 },
  src:         { type: String, default: '' },
  alt:         { type: String, default: '' },
})

const stars = computed(() => {
  const out = []
  const r = Math.max(0, Math.min(5, props.rating))
  for (let i = 0; i < 5; i++) {
    const diff = r - i
    if (diff >= 1) out.push('full')
    else if (diff >= 0.5) out.push('half')
    else out.push('empty')
  }
  return out
})
</script>

<template>
  <article class="card">
    <div v-if="src" class="thumb">
      <img :src="src" :alt="alt || name" loading="lazy" />
    </div>

    <div class="body">
      <h3 class="title">{{ name }}</h3>

      <div class="row">
        <div class="stars" aria-label="note">
          <svg v-for="(t, i) in stars" :key="i" viewBox="0 0 24 24" class="star">
            <!-- étoile vide -->
            <path
              v-if="t==='empty'"
              d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.46 4.73L5.82 21z"
              class="empty"
            />
            <!-- étoile pleine -->
            <path
              v-else-if="t==='full'"
              d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.46 4.73L5.82 21z"
              class="full"
            />
            <!-- demi étoile -->
            <g v-else>
              <defs>
                <clipPath :id="`half-${i}`">
                  <rect x="0" y="0" width="12" height="24" />
                </clipPath>
              </defs>
              <path
                d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.46 4.73L5.82 21z"
                class="empty"
              />
              <path
                d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.62L12 2 9.19 8.62 2 9.24l5.46 4.73L5.82 21z"
                class="full"
                :clip-path="`url(#half-${i})`"
              />
            </g>
          </svg>
        </div>
      </div>

      <div class="row price" aria-label="prix">
        <span
          v-for="i in 5"
          :key="i"
          :class="['dollar', { on: i <= Math.max(1, Math.min(5, priceLevel)) }]"
        >
          $
        </span>
      </div>
    </div>
  </article>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400&family=Jersey+10&display=swap');

.card{
  background:#fff5e6;
  border-radius:10px;
  overflow:hidden;
  border:1px solid rgba(0,0,0,.06);
  width: 100%;
}


.thumb{
  aspect-ratio: 4/3;
  overflow:hidden;
}
.thumb img{
  width:100%;
  height:100%;
  object-fit:cover;
  display:block;
}

.body{
  padding:10px 12px 12px;
}

.title{
  margin: 6px 0 6px;
  font-family: "Jersey 10", system-ui, sans-serif;
  font-weight: 400;
  font-size: 24px;
  line-height: 1;
  letter-spacing: 0;
  color:#000;
}

.row{ display:flex; align-items:center; gap:8px; }

.stars{ display:flex; gap:2px; }
.star{ width:18px; height:18px; flex:0 0 18px; }
.full{ fill:#FFC107; } 
.empty{ fill:#E0E0E0; }

.price{ margin-top:2px; }
.dollar{
  font-family: Inter, system-ui, sans-serif;
  font-weight: 700;
  color:#B3B3B3;
  margin-right:2px;
}
.dollar.on{ color:#333; }
</style>
