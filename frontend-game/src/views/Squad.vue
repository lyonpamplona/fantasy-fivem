<template>
  <div class="flex flex-col lg:flex-row gap-6 h-full min-h-[calc(100vh-100px)] pb-6">
    <div class="flex-1 relative bg-slate-900/60 backdrop-blur-xl rounded-[30px] border border-white/10 flex flex-col p-6 shadow-2xl">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-black text-white uppercase tracking-widest">Escalação Ativa</h2>
        <button @click="clearSquad" class="text-[10px] font-bold uppercase text-rose-500 bg-rose-500/10 hover:bg-rose-500 hover:text-white transition-all px-4 py-2 rounded-lg">Limpar</button>
      </div>

      <div class="grid grid-cols-5 grid-rows-3 gap-4 h-full w-full max-w-3xl mx-auto items-center justify-items-center">
        <div v-for="(role, key) in roles" :key="key" :class="role.colRow" class="flex flex-col items-center gap-2 w-full max-w-[140px]" @dragover.prevent @drop="onDrop(key)">
          <div class="text-[9px] font-black uppercase tracking-widest bg-black/50 px-3 py-1 rounded-full" :class="role.color">{{ role.label }}</div>
          <div class="w-full aspect-[3/4] border-2 border-dashed border-white/20 rounded-xl flex items-center justify-center relative transition-all" :class="{'bg-white/5 border-[var(--md-sys-color-primary)] scale-105': draggingCard}">
            <div v-if="squad[key]" class="absolute inset-0 w-full h-full cursor-pointer group" draggable="true" @dragstart="startDrag(squad[key], key)">
              <FantasyCard :card="squad[key]" />
              <button @click="removeFromSquad(key)" class="absolute -top-2 -right-2 bg-rose-500 text-white rounded-full w-6 h-6 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity z-50 shadow-lg"><span class="material-symbols-rounded text-xs">close</span></button>
            </div>
            <span v-else class="material-symbols-rounded text-white/10 text-3xl pointer-events-none">add</span>
          </div>
        </div>
      </div>
    </div>

    <div class="w-full lg:w-[320px] bg-slate-900 border border-white/10 rounded-[30px] flex flex-col overflow-hidden shadow-2xl">
      <div class="p-5 border-b border-white/10 bg-slate-950 flex justify-between items-center">
        <div>
          <h2 class="text-lg font-black text-white uppercase tracking-tighter">Reservas</h2>
          <p class="text-[10px] text-slate-500 font-bold mt-1 uppercase">Arraste para o campo</p>
        </div>
        <span class="bg-white/10 text-white px-3 py-1 rounded-md text-xs font-bold">{{ benchCards.length }}</span>
      </div>
      
      <div class="flex-1 overflow-y-auto p-4 space-y-3 bg-black/20 custom-scrollbar" @dragover.prevent @drop="onDropToBench">
        <div v-if="benchCards.length === 0" class="text-center text-slate-500 mt-10 text-xs font-bold">Sem reservas.</div>
        <div v-for="card in benchCards" :key="card.id" draggable="true" @dragstart="startDrag(card, 'bench')" @dragend="endDrag" class="w-full bg-slate-800/80 rounded-xl border border-white/10 p-3 flex gap-4 cursor-grab active:cursor-grabbing hover:bg-slate-700 transition-colors items-center">
          <div class="w-[60px] aspect-[3/4] shrink-0 pointer-events-none"><FantasyCard :card="card" /></div>
          <div class="flex flex-col justify-center flex-1 min-w-0">
            <h4 class="font-black text-white text-sm truncate uppercase tracking-tighter">{{ card.player_nickname }}</h4>
            <span class="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 bg-black/50 rounded w-max mt-1" :style="{ color: rarityColors[card.rarity] || '#fff' }">{{ card.rarity }}</span>
          </div>
          <span class="material-symbols-rounded opacity-30 text-white/50 px-1 text-sm">drag_indicator</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFantasyStore } from '../stores/fantasy'
import FantasyCard from '../components/FantasyCard.vue'

const store = useFantasyStore()
const rarityColors = { COMMON: '#94a3b8', RARE: '#0ea5e9', EPIC: '#a855f7', LEGENDARY: '#fbbf24' }

const roles = {
  awper: { label: 'AWPer', colRow: 'col-start-3 row-start-1', color: 'text-amber-400' },
  entry: { label: 'Entry', colRow: 'col-start-1 row-start-2', color: 'text-slate-300' },
  lurker: { label: 'Lurker', colRow: 'col-start-5 row-start-2', color: 'text-slate-300' },
  support: { label: 'Support', colRow: 'col-start-2 row-start-3', color: 'text-slate-300' },
  igl: { label: 'IGL', colRow: 'col-start-4 row-start-3', color: 'text-slate-300' }
}

const squad = ref({ awper: null, entry: null, lurker: null, support: null, igl: null })
const draggingCard = ref(null)
const sourceSlot = ref(null)

const benchCards = computed(() => {
  const squadIds = Object.values(squad.value).filter(c => c !== null).map(c => c.id)
  return store.cards.filter(card => !squadIds.includes(card.id))
})

const startDrag = (card, source) => { draggingCard.value = card; sourceSlot.value = source }
const endDrag = () => { draggingCard.value = null; sourceSlot.value = null }

const onDrop = (targetSlot) => {
  if (!draggingCard.value) return
  const cardInTarget = squad.value[targetSlot]
  if (sourceSlot.value !== 'bench') squad.value[sourceSlot.value] = cardInTarget
  squad.value[targetSlot] = draggingCard.value
  endDrag()
  saveSquad()
}

const onDropToBench = () => {
  if (sourceSlot.value !== 'bench' && sourceSlot.value !== null) removeFromSquad(sourceSlot.value)
}

const removeFromSquad = (slot) => { squad.value[slot] = null; saveSquad() }
const clearSquad = () => { squad.value = { awper: null, entry: null, lurker: null, support: null, igl: null }; saveSquad() }

const saveSquad = () => {
  const squadData = {}
  for (const key in squad.value) squadData[key] = squad.value[key] ? squad.value[key].id : null
  localStorage.setItem('my_saved_squad', JSON.stringify(squadData))
}

onMounted(async () => {
  await store.fetchCards()
  const saved = localStorage.getItem('my_saved_squad')
  if (saved && store.cards.length > 0) {
    const parsed = JSON.parse(saved)
    for (const key in parsed) if (parsed[key]) {
      const f = store.cards.find(c => c.id === parsed[key])
      if (f) squad.value[key] = f
    }
  }
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.1); border-radius: 4px; }
</style>