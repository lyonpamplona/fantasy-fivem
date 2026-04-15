<template>
  <div class="h-full flex flex-col pb-10">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-4 border-b border-white/10 gap-4">
      <div>
        <h1 class="text-4xl font-black text-white tracking-tighter uppercase">Meu Deck</h1>
        <p class="text-sm font-medium text-slate-400 mt-1">Gerencie suas cartas e forje novas.</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <button v-for="f in ['ALL', 'COMMON', 'RARE', 'EPIC', 'LEGENDARY']" :key="f" @click="activeFilter = f" class="px-4 py-2 rounded-xl font-bold text-xs uppercase tracking-widest transition-all border" :class="activeFilter === f ? 'bg-[var(--md-sys-color-primary)] text-white border-[var(--md-sys-color-primary)] shadow-[0_0_15px_var(--md-sys-color-primary)]' : 'bg-slate-900 text-slate-400 border-white/10 hover:bg-slate-800 hover:text-white'">
          {{ f === 'ALL' ? 'Todas' : f }}
        </button>
      </div>
    </div>

    <div class="flex-1 overflow-y-auto custom-scrollbar pr-2">
      <div v-if="filteredCards.length === 0" class="flex flex-col items-center justify-center h-[50vh] opacity-50">
        <span class="material-symbols-rounded text-6xl text-white mb-4">style</span>
        <h2 class="text-xl font-black text-white uppercase tracking-widest">Nenhuma carta encontrada</h2>
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <div v-for="card in filteredCards" :key="card.id" class="relative group cursor-pointer" @click="toggleSelection(card)">
          <div :class="{'ring-2 ring-[var(--md-sys-color-primary)] scale-95 opacity-80': isSelected(card.id)}" class="transition-all duration-200 w-full aspect-[3/4]">
            <FantasyCard :card="card" />
          </div>
          <button @click.stop="openModal(card)" class="absolute top-2 right-2 w-8 h-8 bg-black/60 backdrop-blur border border-white/10 rounded-lg flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white/20">
            <span class="material-symbols-rounded text-sm">visibility</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="selectedCards.length > 0" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-slate-900/90 backdrop-blur-xl border border-white/10 p-4 rounded-2xl shadow-2xl flex items-center gap-6 z-40 animate-zoom-in">
      <div class="flex flex-col">
        <span class="text-[10px] font-black text-slate-400 uppercase tracking-widest">Cartas Selecionadas</span>
        <span class="text-2xl font-black text-white leading-none">{{ selectedCards.length }} <span class="text-sm text-slate-500">/ 10</span></span>
      </div>
      <button @click="handleBurn" :disabled="selectedCards.length !== 10 || isBurning" class="px-8 py-3 bg-[var(--md-sys-color-primary)] text-white rounded-xl font-black uppercase tracking-widest flex items-center gap-2 hover:scale-105 transition-all disabled:opacity-50 disabled:hover:scale-100 disabled:cursor-not-allowed shadow-[0_0_20px_var(--md-sys-color-primary)]">
        <span class="material-symbols-rounded" :class="{'animate-spin': isBurning}">{{ isBurning ? 'sync' : 'local_fire_department' }}</span>
        {{ isBurning ? 'Forjando...' : 'Forjar Contrato' }}
      </button>
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
const selectedCards = ref([])
const isBurning = ref(false)
const selectedModalCard = ref(null)
const rewardCard = ref(null)

const filteredCards = computed(() => {
  if (activeFilter.value === 'ALL') return store.cards
  return store.cards.filter(c => c.rarity === activeFilter.value)
})

const isSelected = (id) => selectedCards.value.includes(id)

const toggleSelection = (card) => {
  if (card.rarity !== 'COMMON') {
    toastStore.showToast('Forja Inválida', 'Apenas cartas COMUNS podem ser forjadas.', 'warning')
    return
  }
  const index = selectedCards.value.indexOf(card.id)
  if (index > -1) {
    selectedCards.value.splice(index, 1)
  } else {
    if (selectedCards.value.length < 10) selectedCards.value.push(card.id)
    else toastStore.showToast('Limite Atingido', 'Você já selecionou 10 cartas.', 'warning')
  }
}

const openModal = (card) => {
  selectedModalCard.value = card
}

const handleBurn = async () => {
  if (selectedCards.value.length !== 10) return
  isBurning.value = true
  try {
    const newCard = await store.burnCards(selectedCards.value)
    if (newCard) {
      toastStore.showToast('Forja Concluída!', `Você obteve ${newCard.player_nickname} (${newCard.rarity})`, 'success')
      selectedCards.value = []
      rewardCard.value = newCard
    } else {
      toastStore.showToast('Falha na Forja', 'Verifique se você possui os requisitos.', 'error')
    }
  } catch (error) {
  } finally {
    isBurning.value = false
  }
}

onMounted(() => {
  store.fetchCards()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
@keyframes zoom-in { 0% { opacity: 0; transform: translate(-50%, 20px); } 100% { opacity: 1; transform: translate(-50%, 0); } }
.animate-zoom-in { animation: zoom-in 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards; }
</style>