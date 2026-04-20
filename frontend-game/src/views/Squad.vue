<template>
  <div class="h-full flex flex-col pb-10 bg-[#050505]">
    
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-6 border-b border-zinc-900 gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-emerald-950/30 border border-emerald-900/50 flex items-center justify-center clip-esports shadow-[0_0_20px_rgba(16,185,129,0.15)]">
          <span class="material-symbols-rounded text-2xl text-emerald-500">shield</span>
        </div>
        <div>
          <h1 class="text-4xl font-black text-white tracking-tighter uppercase italic leading-none drop-shadow-md">Esquadrão Tático</h1>
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">Simulador de Sinergia e Força de Combate</p>
        </div>
      </div>
    </div>

    <div class="flex flex-col lg:flex-row gap-8">
      
      <div class="w-full lg:w-3/4 grid grid-cols-2 md:grid-cols-5 gap-4">
        <div v-for="slot in 5" :key="slot" class="flex flex-col gap-4">
          <div class="text-center">
            <span class="text-[9px] font-black text-zinc-600 uppercase tracking-[0.3em]">Posição 0{{ slot }}</span>
          </div>
          
          <div v-if="squadCards[slot - 1]" class="relative group cursor-pointer" @click="promptRemove(squadCards[slot - 1])">
            <div class="absolute -top-3 left-1/2 -translate-x-1/2 z-50 bg-emerald-950/80 border border-emerald-900 text-emerald-400 text-[8px] font-black uppercase tracking-widest px-3 py-1 clip-esports-small whitespace-nowrap shadow-[0_0_10px_rgba(16,185,129,0.3)]">
              {{ squadCards[slot - 1].squad_role }}
            </div>
            <div class="absolute inset-0 bg-rose-600/20 backdrop-blur-sm z-40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity duration-300">
               <span class="material-symbols-rounded text-rose-500 text-4xl">person_remove</span>
            </div>
            <div class="aspect-[2/3] w-full relative z-10 transform-gpu transition-transform duration-300 group-hover:scale-95">
              <FantasyCard :card="squadCards[slot - 1]" :force-reveal="true" :is-interactive="false" />
            </div>
          </div>
          
          <div v-else @click="openSelection(slot)" class="aspect-[2/3] w-full border-2 border-dashed border-zinc-800 bg-[#0a0a0c] hover:bg-zinc-900/50 hover:border-emerald-900/50 transition-colors flex flex-col items-center justify-center cursor-pointer group clip-esports">
            <span class="material-symbols-rounded text-zinc-700 group-hover:text-emerald-500 text-3xl mb-2 transition-colors">add</span>
            <span class="text-[8px] font-black text-zinc-600 group-hover:text-emerald-600 uppercase tracking-widest">Alocar Operador</span>
          </div>
        </div>
      </div>

      <div class="w-full lg:w-1/4 bg-[#0a0a0c] border border-zinc-900 p-6 clip-esports shadow-2xl flex flex-col gap-6 relative overflow-hidden">
        <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(16,185,129,0.02)_4px,rgba(16,185,129,0.02)_8px)] pointer-events-none"></div>
        
        <div>
          <h3 class="text-xs font-black text-emerald-500 uppercase tracking-[0.3em] mb-4">Relatório de Análise</h3>
          
          <div class="flex justify-between items-center mb-2">
            <span class="text-[10px] font-mono text-zinc-500 uppercase">Poder Base (RAW)</span>
            <span class="text-sm font-black text-white">{{ basePower }}</span>
          </div>
          <div class="flex justify-between items-center mb-4">
            <span class="text-[10px] font-mono text-zinc-500 uppercase">Multiplicador Sinergia</span>
            <span class="text-sm font-black" :class="synergyMultiplier >= 1 ? 'text-emerald-400' : 'text-rose-400'">{{ (synergyMultiplier * 100).toFixed(0) }}%</span>
          </div>
          
          <div class="pt-4 border-t border-zinc-800">
            <span class="text-[9px] font-black text-zinc-600 uppercase tracking-[0.2em] block mb-1">Força de Combate Efetiva</span>
            <span class="text-4xl font-mono font-black text-emerald-500 drop-shadow-[0_0_15px_rgba(16,185,129,0.4)]">{{ totalCombatPower }}</span>
          </div>
        </div>

        <div class="flex-1 bg-[#050505] border border-zinc-900 p-4 mt-4">
          <h4 class="text-[9px] font-black text-zinc-500 uppercase tracking-widest mb-3">Logs de Sinergia Ativos</h4>
          <ul class="flex flex-col gap-2">
            <li v-if="synergies.perfectComp" class="text-[10px] font-mono text-emerald-400 flex items-center gap-2">
              <span class="material-symbols-rounded text-xs">check_circle</span> Perfect Comp (+25%)
            </li>
            <li v-if="synergies.legendaryLeader" class="text-[10px] font-mono text-amber-400 flex items-center gap-2">
              <span class="material-symbols-rounded text-xs">stars</span> Liderança Elite (+10%)
            </li>
            <li v-if="synergies.overlappingRoles" class="text-[10px] font-mono text-rose-500 flex items-center gap-2">
              <span class="material-symbols-rounded text-xs">warning</span> Conflito Tático (-15%)
            </li>
            <li v-if="!synergies.perfectComp && !synergies.legendaryLeader && !synergies.overlappingRoles" class="text-[10px] font-mono text-zinc-600 italic">
              A aguardar implantação de operadores...
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div v-if="showModal" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 backdrop-blur-sm">
      <div class="bg-[#0a0a0c] border border-zinc-800 w-full max-w-4xl p-8 clip-esports shadow-2xl flex flex-col max-h-[90vh]">
        <div class="flex justify-between items-center mb-6 border-b border-zinc-900 pb-4">
          <h2 class="text-xl font-black text-white uppercase tracking-widest italic">Alocar Operador - Slot 0{{ selectedSlot }}</h2>
          <button @click="showModal = false" class="text-zinc-500 hover:text-rose-500 transition-colors">
            <span class="material-symbols-rounded">close</span>
          </button>
        </div>

        <div class="flex gap-4 mb-6">
          <button v-for="r in availableRoles" :key="r" @click="tempRole = r" class="flex-1 py-3 border text-[10px] font-black uppercase tracking-widest transition-all clip-esports-small" :class="tempRole === r ? 'bg-emerald-950/40 text-emerald-500 border-emerald-900/50' : 'bg-[#050505] text-zinc-500 border-zinc-800 hover:border-zinc-600'">
            {{ r }}
          </button>
        </div>

        <div class="overflow-y-auto flex-1 pr-2 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
          <div v-for="card in availableCards" :key="card.id" @click="executeDeploy(card)" class="cursor-pointer group relative">
            <div class="absolute inset-0 border-2 border-transparent group-hover:border-emerald-500 z-50 transition-colors clip-esports pointer-events-none"></div>
            <div class="aspect-[2/3] w-full transform-gpu transition-transform duration-200 group-hover:scale-95">
              <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" />
            </div>
          </div>
          <div v-if="availableCards.length === 0" class="col-span-full py-12 text-center">
            <span class="text-xs font-mono text-zinc-600 uppercase">Nenhum operador disponível no arsenal.</span>
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

const showModal = ref(false)
const selectedSlot = ref(null)
const tempRole = ref('Assault')
const availableRoles = ['Sniper', 'Assault', 'Support', 'IGL', 'Lurker']
const isProcessing = ref(false)

const powerMap = { "COMMON": 10, "RARE": 25, "EPIC": 60, "LEGENDARY": 120, "MYTHIC": 250 }

const squadCards = computed(() => {
  const arr = [null, null, null, null, null]
  store.cards.forEach(c => {
    if (c.squad_position >= 1 && c.squad_position <= 5) {
      arr[c.squad_position - 1] = c
    }
  })
  return arr
})

const availableCards = computed(() => {
  return store.cards.filter(c => {
    const inSquad = c.squad_position !== null
    const inContract = c.contract_end_date && new Date(c.contract_end_date) > new Date()
    return !inSquad && !inContract
  })
})

const basePower = computed(() => {
  let power = 0
  squadCards.value.forEach(c => {
    if (c) power += (powerMap[c.rarity] || 0)
  })
  return power
})

const synergies = computed(() => {
  const active = squadCards.value.filter(c => c !== null)
  const roles = active.map(c => c.squad_role)
  const uniqueRoles = new Set(roles)
  
  const roleCounts = {}
  roles.forEach(r => { roleCounts[r] = (roleCounts[r] || 0) + 1 })
  
  const igl = active.find(c => c.squad_role === 'IGL')

  return {
    perfectComp: active.length === 5 && uniqueRoles.size === 5,
    overlappingRoles: Object.values(roleCounts).some(count => count >= 3),
    legendaryLeader: igl && (igl.rarity === 'LEGENDARY' || igl.rarity === 'MYTHIC')
  }
})

const synergyMultiplier = computed(() => {
  let multi = 1.0
  if (synergies.value.perfectComp) multi += 0.25
  if (synergies.value.overlappingRoles) multi -= 0.15
  if (synergies.value.legendaryLeader) multi += 0.10
  return multi
})

const totalCombatPower = computed(() => {
  return Math.floor(basePower.value * synergyMultiplier.value)
})

const openSelection = (slot) => {
  selectedSlot.value = slot
  tempRole.value = 'Assault'
  showModal.value = true
}

const executeDeploy = async (card) => {
  if (isProcessing.value) return
  isProcessing.value = true
  
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    
    const res = await fetch(`${baseUrl}/api/squad/deploy/${card.id}`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify({ position: selectedSlot.value, role: tempRole.value })
    })
    
    if (res.ok) {
      toastStore.showToast('Deployment Confirmado', 'Operador alocado com sucesso.', 'success')
      showModal.value = false
      await store.fetchCards()
    } else {
      toastStore.showToast('Erro Tático', 'Falha ao posicionar operador.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Comunicações offline.', 'error')
  } finally {
    isProcessing.value = false
  }
}

const promptRemove = async (card) => {
  if (isProcessing.value) return
  isProcessing.value = true
  
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    
    const res = await fetch(`${baseUrl}/api/squad/remove/${card.id}`, {
      method: 'POST',
      headers: store.getHeaders()
    })
    
    if (res.ok) {
      toastStore.showToast('Extração Confirmada', 'Operador retirado do esquadrão.', 'success')
      await store.fetchCards()
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Falha na extração.', 'error')
  } finally {
    isProcessing.value = false
  }
}

onMounted(() => {
  store.fetchCards()
})
</script>