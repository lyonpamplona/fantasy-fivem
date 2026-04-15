<template>
  <div class="fixed inset-0 z-[999] flex items-center justify-center p-4 bg-black/80 backdrop-blur-xl overflow-hidden" @click.self="$emit('close')">
    <div class="relative w-full max-w-4xl bg-slate-900 rounded-[30px] border border-white/10 shadow-[0_0_100px_rgba(0,0,0,0.8)] flex flex-col md:flex-row overflow-hidden animate-zoom-in max-h-[90vh]">
      
      <button @click="$emit('close')" class="absolute top-4 right-4 z-50 w-10 h-10 rounded-full bg-white/10 text-white flex items-center justify-center hover:bg-rose-500 transition-all border border-white/10">
        <span class="material-symbols-rounded">close</span>
      </button>

      <div class="p-8 md:w-1/2 flex items-center justify-center bg-black/40 border-r border-white/5">
        <div class="w-[240px] aspect-[3/4]">
          <FantasyCard :card="card" />
        </div>
      </div>

      <div class="p-8 md:w-1/2 flex flex-col justify-center overflow-y-auto">
        <div class="mb-6">
          <span class="px-3 py-1 rounded-full bg-white/5 text-[10px] font-black text-slate-400 uppercase tracking-widest border border-white/5">
            Edição #{{ card.serial_number }}
          </span>
          <h2 class="text-4xl font-black text-white mt-4 uppercase tracking-tighter truncate" :style="{ color: rarityColor }">
            {{ card.player_nickname }}
          </h2>
        </div>
        
        <div class="space-y-6">
          <div>
            <div class="flex justify-between text-xs font-bold text-slate-500 uppercase mb-2 tracking-wider">
              <span>Qualidade (Float)</span>
              <span class="text-white">{{ card.float_value?.toFixed(4) || '0.5000' }}</span>
            </div>
            <div class="h-2 w-full bg-black/50 rounded-full overflow-hidden border border-white/5">
               <div class="h-full transition-all duration-1000 bg-gradient-to-r from-emerald-400 via-amber-400 to-rose-500" :style="{ width: (card.float_value * 100) + '%' }"></div>
            </div>
            <p class="text-[10px] font-bold uppercase tracking-widest mt-1 text-slate-400">{{ floatLabel }}</p>
          </div>

          <div class="grid grid-cols-2 gap-3 pt-4 border-t border-white/5">
             <div class="bg-black/30 p-4 rounded-xl border border-white/5">
                <p class="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">Kills</p>
                <p class="text-2xl font-black text-white">{{ card.kills || 0 }}</p>
             </div>
             <div class="bg-black/30 p-4 rounded-xl border border-white/5">
                <p class="text-[9px] font-bold text-slate-500 uppercase tracking-widest mb-1">HS Rate</p>
                <p class="text-2xl font-black" :style="{ color: rarityColor }">
                  {{ card.kills > 0 ? ((card.headshots / card.kills) * 100).toFixed(1) : 0 }}%
                </p>
             </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import FantasyCard from './FantasyCard.vue'

const props = defineProps({ card: { type: Object, required: true } })
defineEmits(['close'])

const colors = { COMMON: '#94a3b8', RARE: '#0ea5e9', EPIC: '#a855f7', LEGENDARY: '#fbbf24' }
const rarityColor = computed(() => colors[props.card.rarity] || '#ffffff')

const floatLabel = computed(() => {
  const f = props.card.float_value || 0.5
  if (f <= 0.07) return 'Factory New'
  if (f <= 0.15) return 'Minimal Wear'
  if (f <= 0.38) return 'Field-Tested'
  if (f <= 0.45) return 'Well-Worn'
  return 'Battle-Scarred'
})
</script>

<style scoped>
@keyframes zoom-in {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}
.animate-zoom-in {
  animation: zoom-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}
</style>