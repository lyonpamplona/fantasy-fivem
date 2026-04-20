<template>
  <div class="h-full flex flex-col pb-10 bg-[#050505] relative">
    
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-4 md:mb-8 pb-4 md:pb-6 border-b border-zinc-900 gap-4 md:gap-6 shrink-0">
      <div class="flex items-center gap-3 md:gap-4">
        <div class="w-10 h-10 md:w-12 md:h-12 bg-[#0a0a0c] border border-zinc-800 flex shrink-0 items-center justify-center clip-esports shadow-[0_0_15px_rgba(0,0,0,1)] transition-colors" :class="isForgeMode ? 'border-amber-600 shadow-[0_0_20px_rgba(217,119,6,0.3)]' : ''">
          <span class="material-symbols-rounded text-xl md:text-2xl transition-colors" :class="isForgeMode ? 'text-amber-500' : 'text-emerald-500'">{{ isForgeMode ? 'local_fire_department' : 'style' }}</span>
        </div>
        <div>
          <h1 class="text-2xl md:text-4xl font-black text-white tracking-tighter uppercase italic leading-none drop-shadow-md">Arsenal Tático</h1>
          <p class="text-[8px] md:text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">{{ isForgeMode ? 'Protocolo de Fusão' : 'Gestão de Ativos' }}</p>
        </div>
      </div>

      <div class="flex w-full md:w-auto shrink-0">
        <button @click="toggleForgeMode" class="w-full md:w-auto px-4 py-3 md:px-6 md:py-3 border text-[9px] md:text-[10px] font-black uppercase tracking-[0.2em] transition-all clip-esports-small flex items-center justify-center gap-2" :class="isForgeMode ? 'bg-amber-950/40 text-amber-500 border-amber-900/50 shadow-[0_0_15px_rgba(217,119,6,0.2)]' : 'bg-[#0a0a0c] text-zinc-500 border-zinc-800 hover:text-amber-500 hover:border-amber-900/50'">
          <span class="material-symbols-rounded text-sm">whatshot</span>
          {{ isForgeMode ? 'Cancelar Fusão' : 'Ativar Forja' }}
        </button>
      </div>
    </div>

    <div v-if="isForgeMode" class="mb-8 w-full bg-amber-950/10 border border-amber-900/30 clip-esports relative overflow-hidden shrink-0 flex flex-col">
      <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(217,119,6,0.05)_4px,rgba(217,119,6,0.05)_8px)] pointer-events-none"></div>
      
      <div class="relative z-10 flex flex-col lg:flex-row items-center justify-between p-4 sm:p-6 gap-6 w-full border-b border-amber-900/30">
        <div class="flex flex-col sm:flex-row items-center gap-4 w-full lg:w-auto">
          <div class="flex gap-2 sm:gap-3">
            <div v-for="i in 5" :key="i" class="w-10 h-10 sm:w-12 sm:h-12 border border-amber-900/50 flex items-center justify-center bg-black/50 transition-colors" :class="selectedForForge.length >= i ? 'bg-amber-500/20 border-amber-500' : ''">
               <div v-if="selectedForForge.length >= i" class="w-3 h-3 sm:w-4 sm:h-4 bg-amber-500 rounded-full animate-pulse shadow-[0_0_10px_rgba(217,119,6,0.8)]"></div>
            </div>
          </div>
          <span class="text-xs font-mono font-black tracking-widest text-amber-500 mt-2 sm:mt-0">{{ selectedForForge.length }} / 5</span>
        </div>
        
        <div class="flex flex-col w-full lg:w-1/3">
          <div class="flex justify-between items-center mb-2">
            <span class="text-[9px] font-black uppercase tracking-widest text-amber-500">Injeção de C$</span>
            <span class="text-[10px] font-mono text-white">{{ forgeBoostCoins.toLocaleString() }} C$</span>
          </div>
          <input type="range" v-model.number="forgeBoostCoins" min="0" max="50000" step="1000" class="w-full accent-amber-500 h-1 bg-zinc-900 rounded-lg appearance-none cursor-pointer">
        </div>

        <button @click="executeForge" :disabled="selectedForForge.length !== 5 || isProcessing" class="w-full lg:w-auto px-8 py-4 bg-amber-600 hover:bg-amber-500 text-black text-[11px] font-black uppercase tracking-[0.3em] transition-all clip-esports-small disabled:opacity-20 disabled:hover:bg-amber-600 shadow-[0_0_20px_rgba(217,119,6,0.3)] shrink-0">
          {{ isProcessing ? 'Processando...' : 'Fundir' }}
        </button>
      </div>

      <div class="relative z-10 bg-[#050505]/80 p-4 flex flex-col sm:flex-row justify-between items-center gap-4 w-full">
        <div class="text-[9px] font-black uppercase tracking-widest text-amber-500/70 flex items-center gap-2 w-full sm:w-auto justify-center">
          <span class="material-symbols-rounded text-sm">radar</span> Probabilidade
        </div>
        <div class="flex flex-wrap justify-center sm:justify-end gap-3 sm:gap-6 w-full">
          <div class="flex flex-col items-center"><span class="text-[8px] text-zinc-500 uppercase tracking-widest">Comum</span><span class="text-[10px] font-mono font-black text-zinc-300">{{ forgeProbabilities.COMMON }}%</span></div>
          <div class="flex flex-col items-center"><span class="text-[8px] text-blue-500 uppercase tracking-widest">Raro</span><span class="text-[10px] font-mono font-black text-blue-400">{{ forgeProbabilities.RARE }}%</span></div>
          <div class="flex flex-col items-center"><span class="text-[8px] text-purple-500 uppercase tracking-widest">Épico</span><span class="text-[10px] font-mono font-black text-purple-400">{{ forgeProbabilities.EPIC }}%</span></div>
          <div class="flex flex-col items-center"><span class="text-[8px] text-emerald-500 uppercase tracking-widest">Lendário</span><span class="text-[10px] font-mono font-black text-emerald-400 drop-shadow-[0_0_5px_rgba(16,185,129,0.5)]">{{ forgeProbabilities.LEGENDARY }}%</span></div>
          <div class="flex flex-col items-center"><span class="text-[8px] text-amber-500 uppercase tracking-widest">Mítico</span><span class="text-[10px] font-mono font-black text-amber-400 drop-shadow-[0_0_8px_rgba(217,119,6,0.8)]">{{ forgeProbabilities.MYTHIC }}%</span></div>
        </div>
      </div>
    </div>
    
    <div v-if="store.packs && store.packs.length > 0 && !isForgeMode" class="mb-8 p-4 sm:p-6 bg-zinc-950 border border-zinc-800 clip-esports relative shadow-[0_0_30px_rgba(0,0,0,0.5)] w-full shrink-0">
      <div class="flex items-center gap-3 mb-6 border-b border-zinc-900 pb-4">
        <span class="material-symbols-rounded text-emerald-500">inventory_2</span>
        <h2 class="text-sm font-black text-white uppercase tracking-[0.3em]">Suprimentos Fechados</h2>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="pack in store.packs" :key="pack.id" class="flex flex-col items-center w-full">
          <div class="relative w-full aspect-square flex items-center justify-center group transition-all clip-esports-small mb-2" :class="getPackStyle(pack.pack_type).bg">
             <div class="absolute -top-2 -right-2 w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-black z-10 shadow-lg text-white" :class="getPackStyle(pack.pack_type).badge">
               {{ pack.amount }}
             </div>
             <span class="material-symbols-rounded text-5xl transition-colors" :class="getPackStyle(pack.pack_type).iconColor">
               {{ getPackStyle(pack.pack_type).icon }}
             </span>
          </div>
          <button @click="openPack(pack.pack_type)" :disabled="isProcessing" class="w-full py-3 bg-[#050505] border text-[9px] font-black uppercase tracking-widest transition-colors clip-esports-small disabled:opacity-50" :class="getPackStyle(pack.pack_type).button">
            {{ getPackStyle(pack.pack_type).btnText }}
          </button>
        </div>
      </div>
    </div>
    
    <div v-if="!store.cards.length" class="flex-1 flex flex-col items-center justify-center opacity-30 px-4 text-center mt-10">
      <span class="material-symbols-rounded text-6xl mb-4 text-zinc-600">inventory_2</span>
      <h2 class="text-xs font-black text-zinc-400 uppercase tracking-[0.4em]">Arsenal Vazio</h2>
    </div>

    <div v-else class="flex flex-col flex-1 w-full min-h-0">
      <div class="flex gap-2 mb-6 overflow-x-auto pb-2 scrollbar-hide border-b border-zinc-900/50 w-full shrink-0">
        <button v-for="tab in filterTabs" :key="tab.id" @click="activeFilter = tab.id" class="shrink-0 px-6 py-3 text-[10px] font-black uppercase tracking-[0.2em] transition-all relative whitespace-nowrap" :class="activeFilter === tab.id ? `text-${tab.color}-400` : 'text-zinc-600 hover:text-zinc-400'">
          {{ tab.label }} ({{ rarityCounts[tab.id] || 0 }})
          <div v-if="activeFilter === tab.id" class="absolute bottom-0 left-0 w-full h-0.5" :class="`bg-${tab.color}-500 shadow-[0_0_10px_currentColor]`"></div>
        </button>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4 sm:gap-6 px-1 sm:px-2 pb-12 w-full overflow-y-auto">
        <div v-for="card in filteredCards" :key="card.id" class="w-full mx-auto relative group shrink-0" @click="handleCardClick(card)">
          
          <div v-if="isForgeMode && selectedForForge.includes(card.id)" class="absolute -inset-2 border-2 border-amber-500 z-50 pointer-events-none clip-esports animate-pulse shadow-[inset_0_0_20px_rgba(217,119,6,0.5)]"></div>

          <div v-if="isContractActive(card)" class="absolute -top-3 left-1/2 -translate-x-1/2 z-50 bg-indigo-600 text-white text-[8px] font-black uppercase tracking-widest px-3 py-1 clip-esports-small shadow-[0_0_15px_rgba(79,70,229,0.5)] whitespace-nowrap">
            Operação
          </div>

          <div class="aspect-[2/3] w-full transform-gpu transition-all duration-300 relative z-10" :class="{'scale-95 opacity-50': isForgeMode && !selectedForForge.includes(card.id) && selectedForForge.length > 0, 'cursor-pointer lg:group-hover:-translate-y-2': !isContractActive(card)}">
            <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" />
          </div>
        </div>
      </div>
    </div>

    <CardDetailsModal v-if="selectedCard" :card="selectedCard" @close="selectedCard = null" @contract-signed="handleContractSigned" />

    <div v-if="isRevealing" class="fixed inset-0 z-[200] bg-[#050505]/95 backdrop-blur-xl transition-all duration-500 overflow-y-auto">
      <div class="min-h-screen w-full flex flex-col items-center justify-center py-20 px-4 sm:px-8 relative">
        <div v-if="revealType === 'CLASSIFIED'" class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(225,29,72,0.1)_0%,transparent_60%)] pointer-events-none"></div>
        <div v-else-if="revealType === 'FORGE'" class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(217,119,6,0.1)_0%,transparent_60%)] pointer-events-none"></div>
        <div v-else class="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(16,185,129,0.1)_0%,transparent_60%)] pointer-events-none"></div>
        
        <div v-if="!showDecryptionSuccess" class="relative flex flex-col items-center animate-pulse text-center w-full my-auto">
          <div class="w-32 h-32 border-2 flex items-center justify-center rotate-45 mb-12 shrink-0" :class="revealType === 'CLASSIFIED' ? 'border-rose-500/50 animate-[ping_1s_infinite]' : (revealType === 'FORGE' ? 'border-amber-500/50' : 'border-emerald-500/50')">
            <div class="w-24 h-24 border flex items-center justify-center -rotate-45 shrink-0" :class="revealType === 'CLASSIFIED' ? 'border-rose-400/30' : (revealType === 'FORGE' ? 'border-amber-400/30' : 'border-emerald-400/30')">
              <span class="material-symbols-rounded text-6xl" :class="revealType === 'CLASSIFIED' ? 'text-rose-500' : (revealType === 'FORGE' ? 'text-amber-500' : 'text-emerald-500')">
                {{ revealType === 'CLASSIFIED' ? 'terminal' : (revealType === 'FORGE' ? 'local_fire_department' : 'lock_open') }}
              </span>
            </div>
          </div>
          <h2 class="text-2xl md:text-3xl font-black text-white uppercase tracking-[0.4em] mb-2">Processando</h2>
          <div class="w-64 h-1 bg-zinc-900 mt-8 overflow-hidden shrink-0">
            <div class="h-full w-1/2 animate-[slide_1s_ease-in-out_infinite]" :class="revealType === 'CLASSIFIED' ? 'bg-rose-600' : (revealType === 'FORGE' ? 'bg-amber-500' : 'bg-emerald-500')"></div>
          </div>
        </div>

        <div v-else class="relative flex flex-col items-center transform-gpu animate-[zoomIn_0.5s_ease-out_forwards] w-full max-w-6xl mx-auto my-auto">
          <h2 class="text-2xl md:text-3xl font-black text-white uppercase tracking-[0.3em] drop-shadow-md mb-12 text-center">Concluído</h2>
          <div class="flex flex-wrap justify-center gap-4 md:gap-6 w-full px-4">
            <div v-for="(newCard, index) in revealedCards" :key="index" class="w-32 sm:w-40 md:w-48 aspect-[2/3] shrink-0 animate-[zoomIn_0.5s_ease-out_forwards]" :style="`animation-delay: ${index * 0.1}s`">
              <FantasyCard :card="newCard" :force-reveal="true" :is-interactive="false" />
            </div>
          </div>
          <button @click="closeReveal" class="mt-16 shrink-0 px-12 py-4 text-black text-xs font-black uppercase tracking-widest clip-esports-small w-full sm:w-auto" :class="revealType === 'CLASSIFIED' ? 'bg-rose-600 hover:bg-rose-500' : (revealType === 'FORGE' ? 'bg-amber-600 hover:bg-amber-500' : 'bg-emerald-600 hover:bg-emerald-500')">
            Continuar
          </button>
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
import CardDetailsModal from '../components/CardDetailsModal.vue'

const store = useFantasyStore()
const toastStore = useToastStore()

const selectedCard = ref(null)
const isForgeMode = ref(false)
const selectedForForge = ref([])
const forgeBoostCoins = ref(0)
const isProcessing = ref(false)

const isRevealing = ref(false)
const revealType = ref(null) 
const showDecryptionSuccess = ref(false)
const revealedCards = ref([])

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
  store.cards.forEach(c => { counts[c.rarity] = (counts[c.rarity] || 0) + 1 })
  return counts
})

const filteredCards = computed(() => {
  if (activeFilter.value === 'ALL') return store.cards
  return store.cards.filter(c => c.rarity === activeFilter.value)
})

const forgeProbabilities = computed(() => {
  const weightMap = { "COMMON": 1, "RARE": 3, "EPIC": 10, "LEGENDARY": 30, "MYTHIC": 100 }
  let baseWeight = 0
  selectedForForge.value.forEach(id => {
    const card = store.cards.find(c => c.id === id)
    if (card) baseWeight += (weightMap[card.rarity] || 1)
  })
  const boostWeight = Math.floor(forgeBoostCoins.value / 1000) * 5
  const totalWeight = baseWeight + boostWeight

  const mythic = Math.min(0.15, 0.005 + (totalWeight * 0.00015))
  const legendary = Math.min(0.30, 0.02 + (totalWeight * 0.0006))
  const epic = Math.min(0.50, 0.10 + (totalWeight * 0.0015))
  const rare = 0.35
  const common = Math.max(0, 1 - (mythic + legendary + epic + rare))

  return {
    MYTHIC: (mythic * 100).toFixed(1),
    LEGENDARY: (legendary * 100).toFixed(1),
    EPIC: (epic * 100).toFixed(1),
    RARE: (rare * 100).toFixed(1),
    COMMON: (common * 100).toFixed(1)
  }
})

const getPackStyle = (type) => {
  if (type === 'CLASSIFIED') return { bg: 'bg-[#0a0000] border-rose-900', badge: 'bg-rose-600 border-rose-400', icon: 'bug_report', iconColor: 'text-rose-900 group-hover:text-rose-500 animate-pulse', button: 'border-rose-900 text-rose-500 hover:bg-rose-950/50 hover:text-white', btnText: 'DECRIPTAR' }
  if (type === '1') return { bg: 'bg-zinc-950 border-zinc-800 hover:border-emerald-500', badge: 'bg-zinc-600 border-zinc-400', icon: 'box', iconColor: 'text-zinc-600 group-hover:text-emerald-400', button: 'border-zinc-800 text-zinc-400 hover:bg-emerald-950/50 hover:text-white', btnText: 'Abrir' }
  if (type === '3') return { bg: 'bg-blue-950/20 border-blue-900 hover:border-emerald-500', badge: 'bg-blue-600 border-blue-400', icon: 'inventory_2', iconColor: 'text-blue-900 group-hover:text-emerald-400', button: 'border-blue-900 text-blue-500 hover:bg-emerald-950/50 hover:text-white', btnText: 'Abrir Raro' }
  if (type === '5') return { bg: 'bg-purple-950/20 border-purple-900 hover:border-emerald-500', badge: 'bg-purple-600 border-purple-400', icon: 'all_inbox', iconColor: 'text-purple-900 group-hover:text-emerald-400', button: 'border-purple-900 text-purple-500 hover:bg-emerald-950/50 hover:text-white', btnText: 'Abrir Épico' }
  if (type === '7') return { bg: 'bg-emerald-950/20 border-emerald-900 hover:border-emerald-500', badge: 'bg-emerald-600 border-emerald-400', icon: 'deployed_code', iconColor: 'text-emerald-900 group-hover:text-emerald-400', button: 'border-emerald-900 text-emerald-500 hover:bg-emerald-950/50 hover:text-white', btnText: 'Abrir Lendário' }
  if (type === '10') return { bg: 'bg-amber-950/20 border-amber-900 hover:border-emerald-500', badge: 'bg-amber-600 border-amber-400', icon: 'treasure_chest', iconColor: 'text-amber-900 group-hover:text-emerald-400', button: 'border-amber-900 text-amber-500 hover:bg-emerald-950/50 hover:text-white', btnText: 'Abrir Mítico' }
  return { bg: 'bg-zinc-900 border-zinc-800 hover:border-emerald-500', badge: 'bg-emerald-600 border-emerald-400', icon: 'box', iconColor: 'text-emerald-400 group-hover:text-emerald-300', button: 'border-zinc-800 text-emerald-400 hover:bg-emerald-950/50 hover:text-white', btnText: 'Abrir' }
}

const isContractActive = (card) => {
  if (!card.contract_end_date) return false
  return new Date(card.contract_end_date) > new Date()
}

const toggleForgeMode = () => {
  isForgeMode.value = !isForgeMode.value
  selectedForForge.value = []
  forgeBoostCoins.value = 0
  selectedCard.value = null
}

const handleCardClick = (card) => {
  if (isContractActive(card)) return
  if (isForgeMode.value) {
    if (selectedForForge.value.includes(card.id)) {
      selectedForForge.value = selectedForForge.value.filter(id => id !== card.id)
    } else {
      if (selectedForForge.value.length < 5) selectedForForge.value.push(card.id)
    }
  } else {
    selectedCard.value = card
  }
}

const executeForge = async () => {
  if (selectedForForge.value.length !== 5 || isProcessing.value) return
  isProcessing.value = true
  isRevealing.value = true
  revealType.value = 'FORGE'
  showDecryptionSuccess.value = false
  revealedCards.value = []
  
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/cards/forge`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify({ card_ids: selectedForForge.value, boost_coins: forgeBoostCoins.value })
    })
    
    if (res.ok) {
      const data = await res.json()
      setTimeout(async () => {
        revealedCards.value = data.new_card ? [data.new_card] : []
        showDecryptionSuccess.value = true
        selectedForForge.value = []
        forgeBoostCoins.value = 0
        isForgeMode.value = false
        await store.fetchCards()
        if (store.fetchProfile) await store.fetchProfile()
      }, 1500)
    } else {
      isRevealing.value = false
      isProcessing.value = false
      toastStore.showToast('Erro', 'Fundos insuficientes ou falha na forja.', 'error')
    }
  } catch (error) {
    isRevealing.value = false
    isProcessing.value = false
    toastStore.showToast('Erro Crítico', 'Servidor offline.', 'error')
  }
}

const openPack = async (packType) => {
  if (isProcessing.value) return
  isProcessing.value = true
  isRevealing.value = true
  revealType.value = packType === 'CLASSIFIED' ? 'CLASSIFIED' : 'PACK'
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
      }, 1500)
    } else {
      isRevealing.value = false
      isProcessing.value = false
      toastStore.showToast('Erro', 'Falha ao extrair módulo.', 'error')
    }
  } catch (error) {
    isRevealing.value = false
    isProcessing.value = false
    toastStore.showToast('Erro Crítico', 'Servidor offline.', 'error')
  }
}

const closeReveal = () => {
  isRevealing.value = false
  revealType.value = null
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
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }
</style>