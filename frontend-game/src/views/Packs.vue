<template>
  <div class="h-full flex flex-col pb-10">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-4 border-b border-white/10 gap-4">
      <div>
        <h1 class="text-4xl heading-extrabold text-white tracking-tight">Loja de Pacotes</h1>
        <p class="text-sm font-medium text-slate-400 mt-1">Adquira novos jogadores para o seu elenco.</p>
      </div>
      <div class="flex items-center gap-4 bg-slate-900/80 px-6 py-3 rounded-full border border-white/10 shadow-xl">
        <span class="material-symbols-rounded text-amber-400">monetization_on</span>
        <span class="text-xl font-black text-white">{{ playerBalance }}</span>
      </div>
    </div>

    <div v-if="!revealedCards.length && !isOpening" class="flex flex-col items-center justify-center flex-1 mt-10 animate-fade-in">
      <div class="relative w-[220px] h-[320px] bg-gradient-to-br from-slate-700 to-slate-900 rounded-2xl border border-slate-600 shadow-[0_0_50px_rgba(0,0,0,0.5)] flex items-center justify-center mb-10 transform hover:scale-105 transition-transform duration-500">
        <div class="absolute inset-0 bg-white opacity-5 mix-blend-overlay rounded-2xl"></div>
        <span class="text-5xl font-black text-white/20 uppercase rotate-[-45deg] tracking-widest select-none">Standard</span>
      </div>

      <div class="flex flex-wrap justify-center gap-3 mb-8">
        <button 
          v-for="qty in [1, 3, 5, 7, 10]" 
          :key="qty" 
          @click="amount = qty" 
          class="px-6 py-3 rounded-xl font-bold text-sm transition-all border" 
          :class="amount === qty ? 'bg-[var(--md-sys-color-primary)] text-white border-[var(--md-sys-color-primary)] shadow-[0_0_20px_var(--md-sys-color-primary)]' : 'bg-slate-800 text-slate-400 border-white/10 hover:bg-slate-700 hover:text-white'"
        >
          {{ qty }}x Pacote{{ qty > 1 ? 's' : '' }}
        </button>
      </div>

      <button 
        @click="openPacks" 
        :disabled="isOpening" 
        class="px-10 py-4 bg-white text-black rounded-full font-black uppercase tracking-widest hover:scale-105 hover:bg-amber-400 transition-all flex items-center gap-3 shadow-[0_0_30px_rgba(255,255,255,0.2)]"
      >
        <span class="material-symbols-rounded">lock_open</span>
        Abrir por {{ amount * 2500 }} Coins
      </button>
    </div>

    <div v-if="isOpening" class="flex flex-col items-center justify-center flex-1 h-[60vh] animate-fade-in">
       <span class="material-symbols-rounded text-6xl text-[var(--md-sys-color-primary)] animate-spin mb-4">sync</span>
       <h2 class="text-2xl font-black text-white animate-pulse tracking-widest uppercase">Descompactando...</h2>
    </div>

    <div v-if="revealedCards.length > 0 && !isOpening" class="animate-fade-in-up">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-black text-white">Cartas Obtidas</h2>
        <button @click="resetStore" class="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg font-bold text-sm border border-white/10 transition-colors">
          Abrir Mais
        </button>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <div 
          v-for="(card, index) in revealedCards" 
          :key="card.id" 
          class="w-[190px] h-[270px] mx-auto animate-zoom-in" 
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <FantasyCard :card="card" class="w-full h-full" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useToastStore } from '../stores/toast'
import { useFantasyStore } from '../stores/fantasy'
import FantasyCard from '../components/FantasyCard.vue'
import { buildApiUrl } from '../utils/api'

const toastStore = useToastStore()
const fantasyStore = useFantasyStore()

const amount = ref(1)
const isOpening = ref(false)
const revealedCards = ref([])
const playerBalance = ref(0)

const updateBalance = async () => {
  await fantasyStore.fetchProfile()
  playerBalance.value = fantasyStore.balance || 0
}

const openPacks = async () => {
  if (isOpening.value) return
  isOpening.value = true
  revealedCards.value = []

  try {
    const res = await fetch(buildApiUrl(`/api/packs/open/STANDARD?amount=${amount.value}`), {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('jwt_token')}` }
    })

    if (res.ok) {
      const cards = await res.json()
      setTimeout(() => {
        revealedCards.value = cards
        isOpening.value = false
        updateBalance()
        toastStore.showToast('Sucesso', `${amount.value} pacote(s) aberto(s)!`, 'success')
      }, 1800)
    } else {
      const error = await res.json()
      toastStore.showToast('Recusado', error.detail || 'Erro ao abrir pacote.', 'error')
      isOpening.value = false
    }
  } catch (e) {
    toastStore.showToast('Erro', 'Falha na conexão com o servidor.', 'error')
    isOpening.value = false
  }
}

const resetStore = () => {
  revealedCards.value = []
  amount.value = 1
}

onMounted(() => {
  updateBalance()
})
</script>

<style scoped>
@keyframes zoom-in {
  0% { opacity: 0; transform: scale(0.8); }
  100% { opacity: 1; transform: scale(1); }
}
.animate-zoom-in {
  animation: zoom-in 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
}
</style>
