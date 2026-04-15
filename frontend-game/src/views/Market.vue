<template>
  <div class="h-full flex flex-col pb-10">
    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-4 border-b border-white/10 gap-4">
      <div>
        <h1 class="text-4xl heading-extrabold text-white tracking-tight flex items-center gap-3">
          Mercado de Transferências
        </h1>
        <p class="text-sm font-medium text-slate-400 mt-1">Negocie cartas diretamente com outros jogadores.</p>
      </div>
      <div class="flex items-center gap-4 bg-slate-900/80 px-6 py-3 rounded-full border border-white/10 shadow-xl">
        <span class="material-symbols-rounded text-amber-400">monetization_on</span>
        <span class="text-xl font-black text-white">{{ playerBalance }}</span>
      </div>
    </div>

    <div v-if="loading" class="flex items-center justify-center flex-1 h-[60vh]">
       <span class="material-symbols-rounded text-6xl text-[var(--md-sys-color-primary)] animate-spin">sync</span>
    </div>

    <div v-else-if="listings.length === 0" class="flex flex-col items-center justify-center flex-1 h-[60vh] opacity-50">
       <span class="material-symbols-rounded text-6xl text-white mb-4">storefront</span>
       <h2 class="text-xl font-black text-white uppercase tracking-widest">Mercado Vazio</h2>
    </div>

    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 custom-scrollbar overflow-y-auto pr-4">
      <div v-for="listing in listings" :key="listing.id" class="flex flex-col bg-slate-900/50 p-4 rounded-[20px] border border-white/10">
        <div class="w-full h-[240px] mb-4">
          <FantasyCard :card="listing.card" />
        </div>
        <div class="flex items-center justify-between mt-auto pt-4 border-t border-white/10">
          <div class="flex flex-col">
            <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Preço</span>
            <span class="text-lg font-black text-amber-400">{{ listing.price }}</span>
          </div>
          <button @click="buyCard(listing.id)" class="w-10 h-10 bg-emerald-500/20 hover:bg-emerald-500 text-emerald-400 hover:text-white rounded-xl flex items-center justify-center transition-colors border border-emerald-500/30">
            <span class="material-symbols-rounded text-sm">shopping_cart</span>
          </button>
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

const listings = ref([])
const loading = ref(true)
const playerBalance = ref(0)

const fetchListings = async () => {
  loading.value = true
  try {
    const res = await fetch(buildApiUrl('/api/market/'), {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('jwt_token')}` }
    })
    if (res.ok) listings.value = await res.json()
  } catch (e) {
  } finally {
    loading.value = false
  }
}

const updateBalance = async () => {
  await fantasyStore.fetchProfile()
  playerBalance.value = fantasyStore.balance || 0
}

const buyCard = async (listingId) => {
  try {
    const res = await fetch(buildApiUrl(`/api/market/buy/${listingId}`), {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${localStorage.getItem('jwt_token')}` }
    })
    if (res.ok) {
      toastStore.showToast('Transferência Concluída', 'Carta adicionada ao seu Deck!', 'success')
      await fetchListings()
      await updateBalance()
    } else {
      const err = await res.json()
      toastStore.showToast('Mercado', err.detail || 'Falha na compra.', 'error')
    }
  } catch (e) {
    toastStore.showToast('Erro', 'Conexão falhou.', 'error')
  }
}

onMounted(() => {
  fetchListings()
  updateBalance()
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
</style>
