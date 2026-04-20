<template>
  <div class="h-full flex flex-col pb-10 bg-[#050505]">
    <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between mb-10 pb-6 border-b border-zinc-900 gap-6">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center clip-esports shadow-[0_0_15px_rgba(0,0,0,1)]">
          <span class="material-symbols-rounded text-white text-2xl">style</span>
        </div>
        <div>
          <h1 class="text-4xl font-black text-white tracking-tighter uppercase italic leading-none drop-shadow-md">Arsenal</h1>
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">Data & Assets Storage</p>
        </div>
      </div>
      
      <div class="flex flex-wrap items-center gap-4">
        <div class="bg-[#0a0a0c] border border-zinc-800 p-1 flex gap-1 clip-esports-small">
          <button v-for="f in ['ALL', 'COMMON', 'RARE', 'EPIC', 'LEGENDARY']" :key="f" @click="setFilter(f)" class="px-5 py-2 text-[9px] font-black uppercase tracking-[0.2em] transition-all duration-300 clip-esports-small" :class="activeFilter === f ? 'bg-zinc-800 text-white' : 'text-zinc-600 hover:text-white'">
            {{ f === 'ALL' ? 'Todos' : f }}
          </button>
        </div>
        
        <button @click="toggleForgeMode" class="px-6 py-3 text-[10px] font-black uppercase tracking-[0.2em] flex items-center gap-2 transition-all duration-300 border clip-esports-small" :class="isForgeMode ? 'bg-rose-950/50 border-rose-900 text-rose-500 hover:bg-rose-600 hover:text-black' : 'bg-[#0a0a0c] border-zinc-800 text-zinc-500 hover:bg-white hover:text-black'">
          <span class="material-symbols-rounded text-sm">{{ isForgeMode ? 'close' : 'bolt' }}</span>
          {{ isForgeMode ? 'Abortar' : 'Protocolo Forja' }}
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto pr-2 custom-scrollbar transform-gpu">
      <div v-if="store.packs.length > 0" class="mb-12">
        <h2 class="text-[10px] font-black text-zinc-500 uppercase tracking-[0.3em] mb-6 flex items-center gap-3">
          <span class="w-8 h-[1px] bg-zinc-800"></span> Cargas Criptografadas
        </h2>
        <div class="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-4">
           <div v-for="pack in store.packs" :key="pack.pack_type" class="bg-[#0a0a0c] border border-zinc-800 p-6 flex flex-col items-center justify-center relative group cursor-pointer hover:bg-zinc-900 hover:-translate-y-2 transition-all duration-300 transform-gpu will-change-transform clip-esports" @click="openPack(pack.pack_type)">
              <div class="absolute top-0 right-0 m-2 w-6 h-6 bg-[#050505] border border-zinc-800 flex items-center justify-center clip-esports-small">
                <span class="text-[9px] font-mono font-black text-white">{{ pack.amount }}</span>
              </div>
              <span class="material-symbols-rounded text-4xl mb-3 text-zinc-600 group-hover:text-white transition-colors">inventory_2</span>
              <h3 class="text-[9px] font-black text-zinc-400 uppercase tracking-widest">Type {{ pack.pack_type }}</h3>
           </div>
        </div>
      </div>

      <div v-if="paginatedCards.length === 0" class="flex flex-col items-center justify-center h-[40vh] opacity-30">
        <div class="w-20 h-20 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center mb-6 rotate-45">
          <span class="material-symbols-rounded text-5xl -rotate-45 text-zinc-600">analytics</span>
        </div>
        <h2 class="text-sm font-black text-zinc-500 uppercase tracking-[0.4em]">Database Vazia</h2>
      </div>
      
      <div v-else>
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-5">
          <div v-for="card in paginatedCards" :key="card.id" class="w-full aspect-[2/3] relative transition-all duration-300 transform-gpu will-change-transform" :class="{'scale-95 opacity-50': isSelected(card.id)}">
            <div v-if="isForgeMode" class="absolute -top-2 -right-2 z-30 w-8 h-8 border border-zinc-700 bg-[#050505] flex items-center justify-center transition-colors clip-esports-small" :class="{'bg-emerald-600 border-emerald-500': isSelected(card.id)}">
              <span v-if="isSelected(card.id)" class="material-symbols-rounded text-black text-sm font-black">check</span>
            </div>
            <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" @cardClick="handleCardClick" />
          </div>
        </div>
        
        <div class="flex justify-between items-center mt-14 mb-4 px-6 py-4 bg-[#0a0a0c] border border-zinc-800 clip-esports-small">
          <span class="text-[10px] font-mono font-black text-zinc-500 uppercase tracking-widest">Índice {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, displayedCards.length) }} de {{ displayedCards.length }}</span>
          <div class="flex gap-2">
            <button @click="currentPage--" :disabled="currentPage === 1" class="w-10 h-10 bg-[#050505] border border-zinc-800 flex items-center justify-center hover:bg-white hover:text-black disabled:opacity-30 disabled:hover:bg-[#050505] disabled:hover:text-white transition-colors clip-esports-small">
              <span class="material-symbols-rounded text-lg">chevron_left</span>
            </button>
            <button @click="currentPage++" :disabled="currentPage === totalPages" class="w-10 h-10 bg-[#050505] border border-zinc-800 flex items-center justify-center hover:bg-white hover:text-black disabled:opacity-30 disabled:hover:bg-[#050505] disabled:hover:text-white transition-colors clip-esports-small">
              <span class="material-symbols-rounded text-lg">chevron_right</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isForgeMode" class="fixed bottom-8 left-1/2 -translate-x-1/2 w-full max-w-3xl bg-[#050505] border-t-2 border-zinc-800 p-4 shadow-[0_0_50px_rgba(0,0,0,0.9)] z-50 flex items-center justify-between clip-esports">
      <div class="flex items-center gap-6 pl-4">
        <div class="w-12 h-12 bg-rose-950/50 flex items-center justify-center border border-rose-900/50 clip-esports-small">
          <span class="material-symbols-rounded text-rose-500 text-2xl" :class="{'animate-spin': isBurning}">bolt</span>
        </div>
        <div class="flex flex-col">
          <span class="text-[9px] font-black text-rose-500 uppercase tracking-[0.3em] mb-1">Sobrecarga de Ativos</span>
          <div class="flex items-baseline gap-2">
            <span class="text-3xl font-mono font-black text-white leading-none">{{ selectedCards.length }}</span>
            <span class="text-xs font-black text-zinc-600 uppercase">/ 10 Máx</span>
          </div>
        </div>
        <div class="hidden md:flex flex-col ml-4 pl-8 border-l border-zinc-800">
          <span class="text-[9px] font-black text-zinc-500 uppercase tracking-[0.3em] mb-1">Taxa de Estabilidade</span>
          <span class="text-2xl font-mono font-black leading-none" :class="burnChance >= 50 ? 'text-emerald-500' : 'text-rose-500'">{{ burnChance }}%</span>
        </div>
      </div>
      <button @click="handleBurn" :disabled="selectedCards.length < 5 || selectedCards.length > 10 || isBurning" class="px-10 py-5 bg-white text-black font-black text-[10px] uppercase tracking-[0.3em] hover:bg-rose-600 hover:text-white transition-all duration-300 disabled:opacity-20 disabled:cursor-not-allowed clip-esports-small">
        {{ isBurning ? 'Iniciando...' : 'Forjar Ativos' }}
      </button>
    </div>

    <div v-if="revealedCards.length > 0" class="fixed inset-0 z-[200] bg-black/95 backdrop-blur-md flex flex-col items-center justify-center p-6 transform-gpu">
      <div class="mb-14 text-center">
        <div class="w-16 h-16 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center mx-auto mb-6 clip-esports shadow-[0_0_50px_rgba(255,255,255,0.1)]">
          <span class="material-symbols-rounded text-white text-3xl">lock_open</span>
        </div>
        <h2 class="text-5xl font-black text-white tracking-tighter uppercase italic mb-3">Protocolo Descriptografado</h2>
        <p class="text-[10px] font-black text-zinc-500 uppercase tracking-[0.3em]">Clique nos ativos para revelar o conteúdo militar.</p>
      </div>
      <div class="flex flex-wrap justify-center gap-6 w-full max-w-6xl">
        <div v-for="(card, index) in revealedCards" :key="index" class="w-[160px] md:w-[200px] aspect-[2/3] transform-gpu will-change-transform animate-gacha-drop" :style="{ animationDelay: `${index * 150}ms` }">
          <FantasyCard :card="card" :force-reveal="card.isRevealed" :is-interactive="true" @cardClick="card.isRevealed = true" />
        </div>
      </div>
      <div class="mt-16 h-16">
        <transition name="fade">
          <button v-if="allCardsRevealed" @click="closeGacha" class="px-12 py-5 bg-emerald-600 text-black font-black text-[11px] uppercase tracking-[0.3em] hover:bg-emerald-500 transition-colors clip-esports-small shadow-[0_0_30px_rgba(16,185,129,0.3)]">
            Sincronizar Arsenal
          </button>
        </transition>
      </div>
    </div>

    <CardDetailsModal v-if="selectedModalCard" :card="selectedModalCard" @close="selectedModalCard = null" />
    <CardDetailsModal v-if="rewardCard" :card="rewardCard" @close="rewardCard = null" />
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

const activeFilter = ref('ALL')
const isForgeMode = ref(false)
const selectedCards = ref([])
const isBurning = ref(false)
const currentPage = ref(1)
const itemsPerPage = 12

const selectedModalCard = ref(null)
const rewardCard = ref(null)
const revealedCards = ref([])

const filteredCards = computed(() => {
  if (activeFilter.value === 'ALL') return store.cards
  return store.cards.filter(c => c.rarity === activeFilter.value)
})

const forgeEligibleCards = computed(() => {
  return filteredCards.value.filter(c => c.squad_position === null && !c.is_listed)
})

const displayedCards = computed(() => {
  return isForgeMode.value ? forgeEligibleCards.value : filteredCards.value
})

const totalPages = computed(() => Math.ceil(displayedCards.value.length / itemsPerPage) || 1)

const paginatedCards = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return displayedCards.value.slice(start, start + itemsPerPage)
})

const isSelected = (id) => selectedCards.value.includes(id)

const burnChance = computed(() => {
  const l = selectedCards.value.length;
  if (l < 5) return 0;
  const chances = { 5: 20, 6: 36, 7: 52, 8: 68, 9: 84, 10: 100 };
  return chances[l] || 0;
})

const setFilter = (f) => {
  activeFilter.value = f
  currentPage.value = 1
}

const toggleForgeMode = () => {
  isForgeMode.value = !isForgeMode.value
  selectedCards.value = []
  currentPage.value = 1
}

const handleCardClick = (card) => {
  if (isForgeMode.value) {
    const index = selectedCards.value.indexOf(card.id)
    if (index > -1) {
      selectedCards.value.splice(index, 1)
    } else {
      if (selectedCards.value.length < 10) selectedCards.value.push(card.id)
    }
  } else {
    selectedModalCard.value = card
  }
}

const handleBurn = async () => {
  if (selectedCards.value.length < 5 || selectedCards.value.length > 10 || isBurning.value) return
  isBurning.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    
    const payload = [...selectedCards.value] 
    
    const res = await fetch(`${baseUrl}/api/cards/burn`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify(payload)
    })
    
    if (res.ok) {
      const data = await res.json()
      if (data.status === 'success') {
        toastStore.showToast('Sobrecarga Estável', 'Novo ativo de elite forjado.', 'success')
        rewardCard.value = data.card
      } else {
        toastStore.showToast('Falha Crítica', 'Instabilidade no núcleo. Ativos destruídos.', 'error')
      }
      selectedCards.value = []
      isForgeMode.value = false
      await store.fetchCards()
    } else {
      const errData = await res.json().catch(() => ({}))
      toastStore.showToast('Erro na Forja', errData.detail || 'Verifique se os ativos não estão em uso.', 'error')
      await store.fetchCards()
      selectedCards.value = []
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor inacessível.', 'error')
  } finally { 
    isBurning.value = false 
  }
}

const openPack = async (packType) => {
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/packs/open/${packType}`, {
      method: 'POST',
      headers: store.getHeaders()
    })
    
    if (res.ok) {
      const data = await res.json()
      await store.fetchCards()
      await store.fetchPacks()
      revealedCards.value = data.cards.map(c => ({ ...c, isRevealed: false }))
    } else {
      const errData = await res.json().catch(() => ({}))
      toastStore.showToast('Protocolo Negado', errData.detail || 'Falha ao descriptografar a carga.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor inacessível.', 'error')
  }
}

const closeGacha = () => {
  revealedCards.value = []
}

const allCardsRevealed = computed(() => {
  return revealedCards.value.length > 0 && revealedCards.value.every(c => c.isRevealed)
})

onMounted(async () => { 
  if(store.fetchProfile) {
    store.fetchProfile().catch(() => {})
  }
  await store.fetchCards()
  await store.fetchPacks()
})
</script>

<style scoped>
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }

.animate-gacha-drop {
  animation: dropIn 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275) backwards;
}

@keyframes dropIn {
  0% { transform: translateY(-100px) scale(0.8); opacity: 0; }
  100% { transform: translateY(0) scale(1); opacity: 1; }
}
</style>