<template>
  <div class="h-full flex flex-col pb-10 bg-[#050505] relative">
    
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-6 border-b border-zinc-900 gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center clip-esports shadow-[0_0_15px_rgba(0,0,0,1)] transition-colors" :class="isForgeMode ? 'border-amber-600 shadow-[0_0_20px_rgba(217,119,6,0.3)]' : ''">
          <span class="material-symbols-rounded text-2xl transition-colors" :class="isForgeMode ? 'text-amber-500' : 'text-emerald-500'">{{ isForgeMode ? 'local_fire_department' : 'style' }}</span>
        </div>
        <div>
          <h1 class="text-4xl font-black text-white tracking-tighter uppercase italic leading-none drop-shadow-md">Arsenal Tático</h1>
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">{{ isForgeMode ? 'Protocolo de Fusão Ativo' : 'Gestão de Ativos Pessoais' }}</p>
        </div>
      </div>

      <div class="flex gap-4">
        <button @click="toggleForgeMode" class="px-6 py-3 border text-[10px] font-black uppercase tracking-[0.2em] transition-all clip-esports-small flex items-center gap-2" :class="isForgeMode ? 'bg-amber-950/40 text-amber-500 border-amber-900/50 shadow-[0_0_15px_rgba(217,119,6,0.2)]' : 'bg-[#0a0a0c] text-zinc-500 border-zinc-800 hover:text-amber-500 hover:border-amber-900/50'">
          <span class="material-symbols-rounded text-sm">whatshot</span>
          {{ isForgeMode ? 'Cancelar Fusão' : 'Ativar Forja' }}
        </button>
      </div>
    </div>

    <div v-if="isForgeMode" class="mb-8 p-6 bg-amber-950/10 border border-amber-900/30 clip-esports relative overflow-hidden">
      <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(217,119,6,0.05)_4px,rgba(217,119,6,0.05)_8px)] pointer-events-none"></div>
      <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
        <div class="flex items-center gap-4">
          <div class="flex gap-2">
            <div v-for="i in 5" :key="i" class="w-8 h-8 border border-amber-900/50 flex items-center justify-center bg-black/50" :class="selectedForForge.length >= i ? 'bg-amber-500/20 border-amber-500' : ''">
               <div v-if="selectedForForge.length >= i" class="w-3 h-3 bg-amber-500 rounded-full animate-pulse"></div>
            </div>
          </div>
          <span class="text-xs font-mono text-amber-500">{{ selectedForForge.length }} / 5 Ativos Selecionados</span>
        </div>
        
        <button @click="executeForge" :disabled="selectedForForge.length !== 5 || isProcessing" class="px-8 py-4 bg-amber-600 text-black text-[11px] font-black uppercase tracking-[0.3em] transition-all clip-esports-small disabled:opacity-20 shadow-[0_0_20px_rgba(217,119,6,0.3)]">
          {{ isProcessing ? 'Fundindo...' : 'Executar Protocolo de Fusão' }}
        </button>
      </div>
    </div>
    
    <div v-if="store.packs && store.packs.length > 0 && !isForgeMode" class="mb-10 p-6 bg-zinc-950 border border-zinc-800 clip-esports relative shadow-[0_0_30px_rgba(0,0,0,0.5)]">
      <div class="flex items-center gap-3 mb-6 border-b border-zinc-900 pb-4">
        <span class="material-symbols-rounded text-emerald-500">inventory_2</span>
        <h2 class="text-sm font-black text-white uppercase tracking-[0.3em]">Suprimentos Fechados</h2>
      </div>

      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="pack in store.packs" :key="pack.id" class="flex flex-col items-center">
          <div class="relative w-full aspect-square bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center group hover:border-emerald-500 hover:shadow-[0_0_20px_rgba(16,185,129,0.2)] transition-all clip-esports-small mb-2">
             <div class="absolute -top-2 -right-2 w-6 h-6 bg-emerald-600 rounded-full flex items-center justify-center text-[10px] font-black border border-emerald-400 z-10">
               {{ pack.amount }}
             </div>
             <span class="material-symbols-rounded text-5xl text-zinc-600 group-hover:text-emerald-400 transition-colors" :class="{'animate-pulse text-emerald-500': openingPackType === pack.pack_type}">box</span>
          </div>
          <button @click="openPack(pack.pack_type)" :disabled="isProcessing" class="w-full py-2 bg-[#050505] border border-zinc-800 text-[9px] font-black text-zinc-400 hover:text-white uppercase tracking-widest hover:bg-emerald-950/50 transition-colors clip-esports-small disabled:opacity-50">
            Abrir Modulo
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="!store.cards.length" class="flex-1 flex flex-col items-center justify-center opacity-30">
      <span class="material-symbols-rounded text-6xl mb-4 text-zinc-600">inventory_2</span>
      <h2 class="text-xs font-black text-zinc-400 uppercase tracking-[0.4em]">Arsenal Vazio</h2>
    </div>

    <div v-else class="flex flex-col flex-1">
      <div class="flex gap-2 mb-6 overflow-x-auto pb-2 scrollbar-hide border-b border-zinc-900/50">
        <button v-for="tab in filterTabs" :key="tab.id" @click="activeFilter = tab.id" class="px-6 py-3 text-[10px] font-black uppercase tracking-[0.2em] transition-all relative whitespace-nowrap" :class="activeFilter === tab.id ? `text-${tab.color}-400` : 'text-zinc-600 hover:text-zinc-400'">
          {{ tab.label }} ({{ rarityCounts[tab.id] || 0 }})
          <div v-if="activeFilter === tab.id" class="absolute bottom-0 left-0 w-full h-0.5" :class="`bg-${tab.color}-500 shadow-[0_0_10px_currentColor]`"></div>
        </button>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6 px-2 pb-12">
        <div v-for="card in filteredCards" :key="card.id" class="w-full mx-auto relative group" @click="handleCardClick(card)">
          
          <div v-if="isForgeMode && selectedForForge.includes(card.id)" class="absolute -inset-2 border-2 border-amber-500 z-50 pointer-events-none clip-esports animate-pulse shadow-[inset_0_0_20px_rgba(217,119,6,0.5)]"></div>

          <div v-if="isContractActive(card)" class="absolute -top-3 left-1/2 -translate-x-1/2 z-50 bg-indigo-600 text-white text-[8px] font-black uppercase tracking-widest px-3 py-1 clip-esports-small shadow-[0_0_15px_rgba(79,70,229,0.5)] whitespace-nowrap">
            Operação em Curso
          </div>

          <div class="aspect-[2/3] w-full transform-gpu transition-all duration-300 relative z-10" :class="{'scale-95 opacity-50': isForgeMode && !selectedForForge.includes(card.id) && selectedForForge.length > 0, 'cursor-pointer group-hover:-translate-y-2': !isContractActive(card)}">
            <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" />
          </div>
        </div>
        
        <div v-if="filteredCards.length === 0" class="col-span-full py-12 flex flex-col items-center justify-center opacity-40">
          <span class="material-symbols-rounded text-4xl mb-2 text-zinc-600">search_off</span>
          <span class="text-[10px] font-mono uppercase tracking-widest">Nenhum operador desta classe</span>
        </div>
      </div>
    </div>

    <CardDetailsModal v-if="selectedCard" :card="selectedCard" @close="selectedCard = null" @contract-signed="handleContractSigned" />

    <div v-if="openingPackType" class="fixed inset-0 z-[200] flex flex-col items-center justify-center bg-[#050505]/95 backdrop-blur-xl transition-all duration-500">
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.1)_0%,transparent_60%)]"></div>
      
      <div v-if="!showDecryptionSuccess" class="relative flex flex-col items-center animate-pulse">
        <div class="w-32 h-32 border-2 border-emerald-500/50 flex items-center justify-center rotate-45 mb-12 shadow-[0_0_50px_rgba(16,185,129,0.2)]">
          <div class="w-24 h-24 border border-emerald-400/30 flex items-center justify-center -rotate-45">
            <span class="material-symbols-rounded text-6xl text-emerald-500">lock_open</span>
          </div>
        </div>
        <h2 class="text-2xl font-black text-white uppercase tracking-[0.4em] mb-2 drop-shadow-[0_0_10px_rgba(16,185,129,0.8)]">Decodificando Módulo</h2>
        <p class="text-xs font-mono text-emerald-500/70 tracking-widest">A extrair dados do operador...</p>
        
        <div class="w-64 h-1 bg-zinc-900 mt-8 overflow-hidden">
          <div class="h-full bg-emerald-500 w-1/2 animate-[slide_1s_ease-in-out_infinite]"></div>
        </div>
      </div>

      <div v-else class="relative flex flex-col items-center transform-gpu animate-[zoomIn_0.5s_ease-out_forwards] w-full max-w-4xl px-8">
        <h2 class="text-3xl font-black text-white uppercase tracking-[0.3em] drop-shadow-md mb-12">Operadores Extraídos</h2>
        
        <div class="flex flex-wrap justify-center gap-6">
          <div v-for="(newCard, index) in revealedCards" :key="index" class="w-48 aspect-[2/3] transform-gpu transition-all hover:scale-105 hover:-translate-y-2 animate-[zoomIn_0.5s_ease-out_forwards]" :style="`animation-delay: ${index * 0.2}s`">
            <FantasyCard :card="newCard" :force-reveal="true" :is-interactive="false" />
          </div>
        </div>

        <button @click="closePackReveal" class="mt-16 px-12 py-4 bg-emerald-600 hover:bg-emerald-500 text-black text-xs font-black uppercase tracking-widest transition-colors clip-esports-small shadow-[0_0_20px_rgba(16,185,129,0.3)]">
          Continuar
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useFantasyStore } from '../stores/fantasy'
import { useToastStore } from '../stores/toast'
import FantasyCard from '../components/FantasyCard.vue'
import CardDetailsModal from '../components/CardDetailsModal.vue'

const store = useFantasyStore()
const toastStore = useToastStore()

const selectedCard = ref(null)
const isForgeMode = ref(false)
const selectedForForge = ref([])
const isProcessing = ref(false)

const openingPackType = ref(null)
const showDecryptionSuccess = ref(false)

const activeFilter = ref('ALL')
const filterTabs = [
  { id: 'ALL', label: 'Todos', color: 'emerald' },
  { id: 'COMMON', label: 'Comum', color: 'zinc' },
  { id: 'RARE', label: 'Raro', color: 'blue' },
  { id: 'EPIC', label: 'Épico', color: 'purple' },
  { id: 'LEGENDARY', label: 'Lendário', color: 'emerald' },
  { id: 'MYTHIC', label: 'Mítico', color: 'amber' }
]

const rarityCounts = computed(() => {
  const counts = { ALL: store.cards.length }
  store.cards.forEach(c => {
    counts[c.rarity] = (counts[c.rarity] || 0) + 1
  })
  return counts
})

const filteredCards = computed(() => {
  if (activeFilter.value === 'ALL') return store.cards
  return store.cards.filter(c => c.rarity === activeFilter.value)
})

const isContractActive = (card) => {
  if (!card.contract_end_date) return false
  return new Date(card.contract_end_date) > new Date()
}

const toggleForgeMode = () => {
  isForgeMode.value = !isForgeMode.value
  selectedForForge.value = []
  selectedCard.value = null
}

const handleCardClick = (card) => {
  if (isContractActive(card)) {
    toastStore.showToast('Acesso Negado', 'Ativo encontra-se em operação e não pode ser alterado.', 'warning')
    return
  }

  if (isForgeMode.value) {
    if (selectedForForge.value.includes(card.id)) {
      selectedForForge.value = selectedForForge.value.filter(id => id !== card.id)
    } else {
      if (selectedForForge.value.length >= 5) {
        toastStore.showToast('Capacidade Máxima', 'A Forja suporta apenas 5 ativos por ciclo.', 'warning')
        return
      }
      selectedForForge.value.push(card.id)
    }
  } else {
    selectedCard.value = card
  }
}

const executeForge = async () => {
  if (selectedForForge.value.length !== 5 || isProcessing.value) return
  isProcessing.value = true
  
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    
    const res = await fetch(`${baseUrl}/api/cards/forge`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify({ card_ids: selectedForForge.value })
    })
    
    if (res.ok) {
      toastStore.showToast('Forja Concluída', 'Ativos fundidos com sucesso. Novo operador gerado.', 'success')
      selectedForForge.value = []
      isForgeMode.value = false
      await store.fetchCards()
      if (store.fetchProfile) await store.fetchProfile()
    } else {
      const errData = await res.json().catch(() => ({}))
      toastStore.showToast('Falha no Protocolo', errData.detail || 'Fundos insuficientes ou incompatibilidade de ativos.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor de fusão offline.', 'error')
  } finally {
    isProcessing.value = false
  }
}

const revealedCards = ref([])

const openPack = async (packType) => {
  if (isProcessing.value) return
  isProcessing.value = true
  openingPackType.value = packType
  showDecryptionSuccess.value = false
  revealedCards.value = []
  
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    
    const res = await fetch(`${baseUrl}/api/packs/open/${packType}`, {
      method: 'POST',
      headers: store.getHeaders()
    })
    
    if (res.ok) {
      const data = await res.json()
      
      setTimeout(async () => {
        revealedCards.value = data.cards || (data.new_card ? [data.new_card] : [])
        showDecryptionSuccess.value = true
        await store.fetchPacks()
        await store.fetchCards()
      }, 2000)
    } else {
      openingPackType.value = null
      isProcessing.value = false
      toastStore.showToast('Falha na Extração', 'Erro ao comunicar com o cofre.', 'error')
    }
  } catch (error) {
    openingPackType.value = null
    isProcessing.value = false
    toastStore.showToast('Erro Crítico', 'Servidor offline.', 'error')
  }
}

const closePackReveal = () => {
  openingPackType.value = null
  showDecryptionSuccess.value = false
  revealedCards.value = []
  isProcessing.value = false
}

const handleContractSigned = async () => {
  selectedCard.value = null
  await store.fetchCards()
  if (store.fetchProfile) await store.fetchProfile()
}

onMounted(() => {
  store.fetchCards()
  store.fetchPacks()
})
</script>

<style scoped>
@keyframes slide {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(200%); }
}
@keyframes zoomIn {
  0% { opacity: 0; transform: scale(0.8); }
  100% { opacity: 1; transform: scale(1); }
}
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>