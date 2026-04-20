<template>
  <div class="relative w-full h-full perspective-1000 transform-gpu will-change-transform group" @click="handleClick">
    
    <div v-if="localIsFlipped" class="absolute -inset-6 blur-[40px] rounded-full opacity-0 group-hover:opacity-40 transition-opacity duration-700 pointer-events-none z-0" :class="theme.glowBg"></div>

    <div class="w-full h-full transition-transform duration-700 transform-style-3d relative z-10" :class="{'rotate-y-180': localIsFlipped}">
      
      <div class="absolute inset-0 backface-hidden bg-[#0a0a0c] flex flex-col items-center justify-center border border-zinc-800 clip-esports shadow-[inset_0_0_30px_rgba(0,0,0,1)]">
        <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_2px,rgba(255,255,255,0.02)_2px,rgba(255,255,255,0.02)_4px)] pointer-events-none"></div>
        <div class="w-12 h-12 border-2 border-zinc-700 flex items-center justify-center bg-[#050505] relative z-10 rotate-45">
          <span class="material-symbols-rounded text-2xl text-zinc-600 -rotate-45">lock</span>
        </div>
      </div>

      <div class="absolute inset-0 backface-hidden rotate-y-180 flex flex-col overflow-visible bg-zinc-950/40 backdrop-blur-md clip-esports border-l-2 border-b-2 shadow-2xl transition-colors duration-500" :class="theme.borderClass">
        
        <div class="absolute inset-y-4 left-1.5 w-[3px] opacity-30" style="background: repeating-linear-gradient(to bottom, currentColor 0, currentColor 2px, transparent 2px, transparent 4px);" :class="theme.textColor"></div>
        <div class="absolute inset-y-4 right-1.5 w-[3px] opacity-30" style="background: repeating-linear-gradient(to bottom, currentColor 0, currentColor 2px, transparent 2px, transparent 4px);" :class="theme.textColor"></div>
        
        <div class="absolute top-8 left-1/2 -translate-x-1/2 text-[5px] font-black tracking-[0.5em] text-white/10 uppercase pointer-events-none">TACTICAL_INTERFACE_v4.2</div>

        <div class="absolute top-1.5 left-2 right-2 flex justify-between items-start z-30">
          <span class="text-2xl font-black font-mono text-white leading-none italic drop-shadow-[0_2px_10px_rgba(0,0,0,1)]">{{ card.level || 1 }}</span>
          <div class="flex flex-col items-end gap-0.5">
            <span class="text-[6px] font-black uppercase tracking-widest px-1.5 py-0.5 bg-black/80 border" :class="[theme.borderClass, theme.textColor]">{{ card.rarity }}</span>
            <span class="text-[4px] font-mono text-white/30 uppercase tracking-tighter">EXP_LEVEL_0{{ card.level }}</span>
          </div>
        </div>

        <div class="absolute inset-0 z-20 flex items-center justify-center pointer-events-none overflow-visible">
          <img :src="`https://api.dicebear.com/8.x/bottts/svg?seed=${card.serial_number}&baseColor=3f3f46,18181b,09090b`" alt="Operator" class="w-full h-full object-contain scale-[1.25] -translate-y-6 drop-shadow-[0_20px_20px_rgba(0,0,0,0.9)] transition-transform duration-500 group-hover:scale-[1.35]" />
        </div>

        <div class="absolute bottom-0 left-0 w-full z-30 flex flex-col">
          <div class="w-full bg-zinc-950/90 py-1.5 flex justify-center items-center border-t border-white/5 backdrop-blur-md">
            <h3 class="text-[9px] font-black text-white uppercase tracking-[0.3em] truncate px-2 italic drop-shadow-md">{{ card.player_nickname }}</h3>
          </div>
          <div class="grid grid-cols-2 bg-black/90 p-1 gap-1 clip-esports-bottom border-t border-zinc-900">
            <div class="flex flex-col items-center py-1 border-r border-zinc-900/50">
              <span class="text-[5px] font-bold text-zinc-500 uppercase tracking-widest mb-px">Kills</span>
              <span class="text-sm font-mono font-black text-white leading-none">{{ card.kills }}</span>
            </div>
            <div class="flex flex-col items-center py-1">
              <span class="text-[5px] font-bold text-zinc-500 uppercase tracking-widest mb-px">Precision</span>
              <span class="text-sm font-mono font-black text-white leading-none">{{ card.headshots }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <div v-if="isFlashing" class="absolute inset-0 bg-white z-50 clip-esports animate-flash pointer-events-none"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  card: Object,
  forceReveal: { type: Boolean, default: true },
  isInteractive: { type: Boolean, default: false }
})

const emit = defineEmits(['cardClick'])

const localIsFlipped = ref(props.forceReveal)
const isFlashing = ref(false)

watch(() => props.forceReveal, (newVal) => { 
  if (newVal && !localIsFlipped.value && props.isInteractive) {
    triggerEpicReveal()
  } else {
    localIsFlipped.value = newVal 
  }
})

const handleClick = () => {
  if (props.isInteractive && !localIsFlipped.value) {
    triggerEpicReveal()
    emit('cardClick', props.card)
  } else if (!props.isInteractive) {
    emit('cardClick', props.card)
  }
}

const triggerEpicReveal = () => {
  isFlashing.value = true
  setTimeout(() => {
    localIsFlipped.value = true
  }, 150)
  setTimeout(() => {
    isFlashing.value = false
  }, 800)
}

const theme = computed(() => {
  const themes = {
    COMMON: { borderClass: 'border-zinc-500', textColor: 'text-zinc-400', glowBg: 'bg-zinc-500' },
    RARE: { borderClass: 'border-blue-500', textColor: 'text-blue-400', glowBg: 'bg-blue-600' },
    EPIC: { borderClass: 'border-purple-600', textColor: 'text-purple-400', glowBg: 'bg-purple-600' },
    LEGENDARY: { borderClass: 'border-emerald-500', textColor: 'text-emerald-400', glowBg: 'bg-emerald-500' }
  }
  return themes[props.card.rarity] || themes.COMMON
})
</script>

<style scoped>
.perspective-1000 { perspective: 1000px; }
.transform-style-3d { transform-style: preserve-3d; }
.backface-hidden { backface-visibility: hidden; }
.rotate-y-180 { transform: rotateY(180deg); }
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-bottom { clip-path: polygon(0 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%); }

.animate-flash {
  animation: flashBurst 0.8s ease-out forwards;
}

@keyframes flashBurst {
  0% { opacity: 0; transform: scale(0.9); }
  20% { opacity: 1; transform: scale(1.1); box-shadow: 0 0 100px rgba(255,255,255,1); }
  100% { opacity: 0; transform: scale(1); }
}
</style>