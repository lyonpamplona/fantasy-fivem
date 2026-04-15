<template>
  <div 
    class="relative w-full h-full rounded-xl transition-all duration-200 group perspective-1000 select-none overflow-hidden"
    @mousemove="handleHover"
    @mouseleave="resetHover"
    :style="cardStyle"
  >
    <div class="absolute inset-0 rounded-xl z-10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none hologram-layer"></div>
    
    <div class="relative z-20 h-full flex flex-col p-3 bg-slate-900/90 border border-white/10 rounded-xl overflow-hidden backdrop-blur-md shadow-xl">
      <div class="flex justify-between items-start mb-1">
        <div class="flex flex-col">
          <span class="text-[8px] font-black text-white/50 uppercase tracking-tighter">Nível</span>
          <span class="text-xl font-black text-white leading-none">{{ card.level || 1 }}</span>
        </div>
        <div class="px-1.5 py-0.5 rounded bg-black/60 border border-white/10">
           <span class="text-[8px] font-bold uppercase tracking-wider" :style="{ color: rarityColor }">{{ card.rarity }}</span>
        </div>
      </div>

      <div class="flex-1 flex items-center justify-center relative my-1 overflow-hidden rounded-md bg-gradient-to-br from-white/5 to-transparent border border-white/5">
        <div class="text-3xl font-black text-white/5 absolute uppercase rotate-[-25deg] w-[200%] text-center tracking-widest truncate">
          {{ card.player_nickname }}
        </div>
      </div>

      <div class="mt-auto relative z-20 bg-black/40 p-2 rounded-lg border border-white/5">
        <h3 class="text-sm font-black text-white truncate mb-1 uppercase">{{ card.player_nickname }}</h3>
        <div class="grid grid-cols-2 gap-1 border-t border-white/10 pt-1">
          <div class="text-center">
            <p class="text-[7px] text-slate-400 font-bold uppercase">Kills</p>
            <p class="text-[10px] font-black text-white">{{ card.kills || 0 }}</p>
          </div>
          <div class="text-center">
            <p class="text-[7px] text-slate-400 font-bold uppercase">HS Rate</p>
            <p class="text-[10px] font-black" :style="{ color: rarityColor }">
              {{ card.kills > 0 ? ((card.headshots / card.kills) * 100).toFixed(0) : 0 }}%
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({ card: { type: Object, required: true } })
const rotateX = ref(0)
const rotateY = ref(0)
const shineX = ref(50)
const shineY = ref(50)

const colors = { COMMON: '#94a3b8', RARE: '#0ea5e9', EPIC: '#a855f7', LEGENDARY: '#fbbf24' }
const rarityColor = computed(() => colors[props.card?.rarity] || '#ffffff')

const handleHover = (e) => {
  const { clientX, clientY, currentTarget } = e
  const { left, top, width, height } = currentTarget.getBoundingClientRect()
  const x = clientX - left
  const y = clientY - top
  rotateY.value = ((x / width) - 0.5) * 15
  rotateX.value = ((y / height) - 0.5) * -15
  shineX.value = (x / width) * 100
  shineY.value = (y / height) * 100
}

const resetHover = () => {
  rotateX.value = 0
  rotateY.value = 0
  shineX.value = 50
  shineY.value = 50
}

const cardStyle = computed(() => ({
  transform: `rotateX(${rotateX.value}deg) rotateY(${rotateY.value}deg) scale3d(1, 1, 1)`,
  '--shine-x': `${shineX.value}%`,
  '--shine-y': `${shineY.value}%`,
  '--glow-color': rarityColor.value
}))
</script>

<style scoped>
.perspective-1000 { perspective: 1000px; transform-style: preserve-3d; }
.hologram-layer {
  background: radial-gradient(circle at var(--shine-x) var(--shine-y), rgba(255,255,255,0.3) 0%, transparent 60%);
  box-shadow: inset 0 0 20px var(--glow-color);
  mix-blend-mode: overlay;
}
</style>