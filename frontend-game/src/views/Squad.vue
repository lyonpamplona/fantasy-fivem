<template>
  <div class="h-full flex flex-col pb-10">
    
    <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between mb-8 pb-6 border-b border-zinc-900 gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center clip-esports shadow-[0_0_15px_rgba(0,0,0,1)]">
          <span class="material-symbols-rounded text-emerald-500 text-2xl">shield</span>
        </div>
        <div>
          <h1 class="text-4xl font-black text-white tracking-tighter uppercase italic leading-none drop-shadow-md">Roster Tático</h1>
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">Configuração de Deploy</p>
        </div>
      </div>
      <button @click="saveSquad" :disabled="isSaving || currentBudget > 100 || squadSlots.filter(s => s.card !== null).length === 0" class="px-10 py-4 bg-emerald-600 text-black font-black text-[10px] uppercase tracking-[0.2em] transition-colors hover:bg-emerald-500 clip-esports-small disabled:opacity-30 disabled:bg-zinc-900 disabled:text-zinc-600 disabled:cursor-not-allowed flex items-center gap-3">
        <span class="material-symbols-rounded text-sm" :class="{'animate-spin': isSaving}">{{ isSaving ? 'sync' : 'gavel' }}</span>
        {{ isSaving ? 'Sincronizando...' : 'Autorizar Deploy' }}
      </button>
    </div>

    <div class="mb-10 bg-[#0a0a0c] border-l-4 border-y border-r border-zinc-900 p-6 flex flex-col md:flex-row justify-between items-center gap-8 shadow-[inset_0_0_20px_rgba(0,0,0,0.8)]" :class="currentBudget > 100 ? 'border-l-rose-600' : (currentBudget >= 85 ? 'border-l-yellow-500' : 'border-l-emerald-600')">
      <div class="flex flex-col w-full md:w-1/3">
        <span class="text-[9px] font-black text-zinc-500 uppercase tracking-[0.3em] mb-2">Orçamento Salarial</span>
        <div class="flex items-baseline gap-3">
          <span class="text-5xl font-mono font-black leading-none" :class="budgetColorClass">{{ currentBudget }}</span>
          <span class="text-sm font-bold text-zinc-700 uppercase tracking-widest">/ 100 Pts</span>
        </div>
      </div>
      <div class="w-full md:w-2/3 h-2 bg-[#050505] border border-zinc-800 overflow-hidden clip-esports-small">
        <div class="h-full transition-all duration-500 ease-out" :class="budgetBarColorClass" :style="`width: ${Math.min((currentBudget / 100) * 100, 100)}%`"></div>
      </div>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-6 mb-16">
      <div v-for="(slot, index) in squadSlots" :key="index" class="w-full max-w-[190px] mx-auto flex flex-col relative group transform-gpu">
        
        <div class="aspect-[2/3] w-full relative mb-3">
          <div v-if="!slot.card" class="absolute inset-0 border-2 border-dashed border-zinc-800 bg-[#0a0a0c] flex flex-col items-center justify-center hover:border-zinc-500 transition-colors cursor-pointer clip-esports" @click="removeFromSquad(index)">
            <div class="w-10 h-10 border border-zinc-700 flex items-center justify-center mb-3 bg-[#050505] rotate-45">
              <span class="material-symbols-rounded text-zinc-600 -rotate-45">add</span>
            </div>
            <span class="text-[9px] font-black text-zinc-600 tracking-[0.2em] uppercase">Slot 0{{ index + 1 }}</span>
          </div>
          
          <div v-else class="absolute inset-0 cursor-pointer">
            <FantasyCard :card="slot.card" :force-reveal="true" :is-interactive="false" @cardClick="removeFromSquad(index)" />
            
            <div class="absolute top-2 left-2 bg-[#050505] border border-zinc-800 px-2 py-1 z-50 flex items-center gap-1 clip-esports-small">
               <span class="material-symbols-rounded text-[10px] text-emerald-500">toll</span>
               <span class="text-[10px] font-mono font-black text-white">{{ slot.card.deployment_cost }}</span>
            </div>
            <div class="absolute bottom-2 right-2 bg-[#050505] border border-zinc-800 px-2 py-1 z-50 flex items-center gap-1 clip-esports-small" :class="slot.card.contract_points <= 1 ? 'text-rose-500 border-rose-900' : 'text-zinc-400'">
               <span class="material-symbols-rounded text-[10px]">contract</span>
               <span class="text-[10px] font-mono font-black">{{ slot.card.contract_points }}</span>
            </div>
            
            <div class="absolute inset-0 bg-[#050505]/90 flex flex-col items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-40 clip-esports border border-rose-900" @click="removeFromSquad(index)">
               <div class="w-12 h-12 bg-rose-950 border border-rose-800 flex items-center justify-center mb-2 rotate-45">
                 <span class="material-symbols-rounded text-2xl text-rose-500 -rotate-45">close</span>
               </div>
               <span class="text-[9px] font-black text-rose-500 uppercase tracking-[0.2em]">Dispensar</span>
            </div>
          </div>
        </div>

        <select v-model="slot.role" :disabled="!slot.card" class="appearance-none w-full bg-[#0a0a0c] border border-zinc-800 text-zinc-400 text-[9px] font-black uppercase tracking-[0.15em] py-3 text-center focus:outline-none focus:border-emerald-600 disabled:opacity-30 cursor-pointer transition-colors clip-esports-small">
          <option value="entry" class="bg-[#050505] text-white">Entry Fragger</option>
          <option value="support" class="bg-[#050505] text-white">Suporte</option>
          <option value="awper" class="bg-[#050505] text-white">AWPer</option>
          <option value="igl" class="bg-[#050505] text-white">Líder (IGL)</option>
          <option value="lurker" class="bg-[#050505] text-white">Lurker</option>
        </select>
      </div>
    </div>

    <div class="flex-1 bg-[#0a0a0c] border-t border-zinc-900 pt-8">
      <div class="flex items-center gap-4 mb-8 px-4">
        <span class="text-[10px] font-black text-zinc-500 uppercase tracking-[0.3em] bg-[#050505] px-4 py-2 border border-zinc-800 clip-esports-small">Reserva Tática</span>
        <div class="flex-1 h-[1px] bg-zinc-900"></div>
      </div>
      
      <div v-if="availableCards.length === 0" class="flex flex-col items-center justify-center h-[20vh] opacity-30">
        <span class="material-symbols-rounded text-5xl mb-4 text-zinc-600">group_off</span>
        <span class="text-[10px] font-black text-zinc-500 uppercase tracking-widest">Nenhum operador disponível</span>
      </div>

      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-5 px-4 pb-4">
        <div v-for="card in availableCards" :key="card.id" class="w-full aspect-[2/3] relative cursor-pointer transition-transform duration-300 transform-gpu" :class="card.contract_points === 0 ? 'opacity-40 grayscale cursor-not-allowed scale-95' : 'hover:-translate-y-2'" @click="card.contract_points > 0 ? addToSquad(card) : null">
          <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" @cardClick="card.contract_points > 0 ? addToSquad(card) : null" />
          
          <div class="absolute top-2 left-2 bg-[#050505] border border-zinc-800 px-2 py-1 z-50 flex items-center gap-1 pointer-events-none clip-esports-small">
             <span class="material-symbols-rounded text-[10px] text-emerald-500">toll</span>
             <span class="text-[10px] font-mono font-black text-white">{{ card.deployment_cost }}</span>
          </div>
          
          <div v-if="card.contract_points === 0" class="absolute inset-0 bg-[#050505]/80 flex items-center justify-center z-40 pointer-events-none clip-esports border border-zinc-800">
             <div class="flex flex-col items-center">
               <span class="material-symbols-rounded text-zinc-500 text-3xl mb-2">lock</span>
               <span class="text-[8px] text-zinc-500 font-black tracking-[0.2em] uppercase bg-black px-3 py-1 border border-zinc-800 clip-esports-small">Inativo</span>
             </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFantasyStore } from '../stores/fantasy'
import { useToastStore } from '../stores/toast'
import FantasyCard from '../components/FantasyCard.vue'

const store = useFantasyStore()
const toastStore = useToastStore()

const squadSlots = ref([
  { card: null, role: 'entry' },
  { card: null, role: 'support' },
  { card: null, role: 'awper' },
  { card: null, role: 'igl' },
  { card: null, role: 'lurker' }
])
const isSaving = ref(false)

const currentBudget = computed(() => {
  return squadSlots.value.reduce((total, slot) => {
    return total + (slot.card ? slot.card.deployment_cost : 0)
  }, 0)
})

const budgetColorClass = computed(() => {
  if (currentBudget.value > 100) return 'text-rose-600 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)] animate-pulse'
  if (currentBudget.value >= 85) return 'text-yellow-500'
  return 'text-white'
})

const budgetBarColorClass = computed(() => {
  if (currentBudget.value > 100) return 'bg-rose-600 shadow-[0_0_15px_rgba(225,29,72,1)]'
  if (currentBudget.value >= 85) return 'bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,1)]'
  return 'bg-emerald-600 shadow-[0_0_10px_rgba(5,150,105,1)]'
})

const availableCards = computed(() => {
  const slottedIds = squadSlots.value.filter(s => s.card !== null).map(s => s.card.id)
  return store.cards.filter(c => !slottedIds.includes(c.id))
})

const loadSavedSquad = () => {
  const saved = store.cards.filter(c => c.squad_position !== null).sort((a, b) => a.squad_position - b.squad_position)
  saved.forEach(card => {
    if (card.squad_position >= 1 && card.squad_position <= 5) {
      squadSlots.value[card.squad_position - 1].card = card
      if (card.squad_role) {
        squadSlots.value[card.squad_position - 1].role = card.squad_role
      }
    }
  })
}

const addToSquad = (card) => {
  if (card.contract_points === 0) return
  
  const isAlreadyInSquad = squadSlots.value.some(slot => slot.card && slot.card.id === card.id)
  if (isAlreadyInSquad) {
    toastStore.showToast('Operação Negada', 'Este operador já está posicionado no esquadrão.', 'error')
    return
  }

  const emptyIndex = squadSlots.value.findIndex(slot => slot.card === null)
  if (emptyIndex !== -1) {
    squadSlots.value[emptyIndex].card = card
  } else {
    toastStore.showToast('Roster Lotado', 'Remova um operador antes de prosseguir.', 'warning')
  }
}

const removeFromSquad = (index) => {
  if (squadSlots.value[index].card) {
    squadSlots.value[index].card = null
  }
}

const saveSquad = async () => {
  const payloadSquad = squadSlots.value
    .filter(s => s.card !== null)
    .map(s => ({ card_id: s.card.id, role: s.role }))
    
  if (payloadSquad.length === 0) return
  
  isSaving.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/cards/user/me/squad`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify({ squad: payloadSquad })
    })
    
    if (res.ok) {
      toastStore.showToast('Deploy Finalizado', 'Esquadrão sincronizado com os servidores.', 'success')
      await store.fetchCards()
      loadSavedSquad()
    } else {
      toastStore.showToast('Deploy Abortado', 'Verifique os fundos salariais.', 'error')
    }
  } catch (error) {
  } finally {
    isSaving.value = false
  }
}

onMounted(async () => {
  await store.fetchCards()
  loadSavedSquad()
})
</script>

<style scoped>
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }
</style>