<template>
  <div class="h-full flex flex-col pb-10 bg-[#050505] relative overflow-hidden">
    
    <div class="w-full bg-[#0a0a0c] border-b border-zinc-900 py-1.5 px-4 mb-8 overflow-hidden relative flex items-center shadow-inner">
      <div class="absolute left-0 top-0 bottom-0 w-16 bg-gradient-to-r from-[#0a0a0c] to-transparent z-10"></div>
      <div class="flex gap-8 whitespace-nowrap animate-ticker">
        <span class="text-[9px] font-mono uppercase tracking-widest" :class="isDarkWebActive ? 'text-rose-500' : 'text-emerald-500'">
          <span class="text-zinc-600">SYS_LOG:</span> TACTICAL PACK EM ALTA DE 5.2%
        </span>
        <span class="text-[9px] font-mono uppercase tracking-widest" :class="isDarkWebActive ? 'text-rose-500 animate-pulse' : 'text-emerald-500'">
          <span class="text-zinc-600">SYS_LOG:</span> {{ isDarkWebActive ? 'ANOMALIA CRÍTICA DETETADA. NODE SECRETO ATIVO.' : 'VOLATILIDADE DETETADA NO SETOR 4' }}
        </span>
        <span class="text-[9px] font-mono uppercase tracking-widest" :class="isDarkWebActive ? 'text-rose-500' : 'text-emerald-500'">
          <span class="text-zinc-600">SYS_LOG:</span> REDZONE PACK ATINGIU O MÍNIMO HISTÓRICO
        </span>
        <span class="text-[9px] font-mono uppercase tracking-widest" :class="isDarkWebActive ? 'text-rose-500' : 'text-emerald-500'">
          <span class="text-zinc-600">SYS_LOG:</span> ALVO_004 NEGOCIADO POR 12,000 C$
        </span>
      </div>
      <div class="absolute right-0 top-0 bottom-0 w-16 bg-gradient-to-l from-[#0a0a0c] to-transparent z-10"></div>
    </div>

    <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-6 border-b border-zinc-900 gap-6 relative z-10">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center clip-esports shadow-[0_0_15px_rgba(0,0,0,1)] transition-colors duration-500" :class="activeTab === 'DARKWEB' ? 'border-rose-900 shadow-[0_0_20px_rgba(225,29,72,0.4)]' : ''">
          <span class="material-symbols-rounded text-2xl transition-colors duration-500" :class="activeTab === 'DARKWEB' ? 'text-rose-500' : 'text-emerald-500'">{{ activeTab === 'DARKWEB' ? 'warning' : 'storefront' }}</span>
        </div>
        <div>
          <h1 class="text-4xl font-black text-white tracking-tighter uppercase italic leading-none drop-shadow-md transition-colors duration-500" :class="activeTab === 'DARKWEB' ? 'text-rose-500' : ''">{{ activeTab === 'DARKWEB' ? 'Protocolo Oculto' : 'Rede de Suprimentos' }}</h1>
          <p class="text-[10px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">{{ activeTab === 'DARKWEB' ? 'Acesso Não Autorizado' : 'Cripto-Mercado & Trade Network' }}</p>
        </div>
      </div>
      
      <div class="bg-[#0a0a0c] border-l-2 px-5 py-3 flex items-center gap-2 clip-esports-small transition-colors duration-500" :class="activeTab === 'DARKWEB' ? 'border-rose-500 shadow-[0_0_15px_rgba(225,29,72,0.2)]' : 'border-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.1)]'">
        <span class="material-symbols-rounded text-xl transition-colors duration-500" :class="activeTab === 'DARKWEB' ? 'text-rose-500 drop-shadow-[0_0_8px_rgba(225,29,72,0.8)]' : 'text-emerald-500 drop-shadow-[0_0_8px_rgba(16,185,129,0.8)]'">toll</span>
        <span class="text-2xl font-black text-white font-mono tracking-tighter">{{ userBalance.toLocaleString() }}</span>
      </div>
    </div>

    <div class="flex gap-2 mb-8 bg-[#0a0a0c] p-2 border border-zinc-900 clip-esports-small w-fit relative z-10">
      <button @click="activeTab = 'STORE'" class="px-8 py-3 text-[9px] font-black uppercase tracking-[0.2em] transition-all clip-esports-small flex items-center gap-2" :class="activeTab === 'STORE' ? 'bg-[#050505] text-white border border-zinc-700 shadow-lg' : 'bg-transparent text-zinc-600 hover:text-white'">
        <span class="material-symbols-rounded text-xs" :class="{'animate-spin': isFetchingStore}">sync</span>
        Bolsa Oficial
      </button>
      <button @click="fetchP2PListings" class="px-8 py-3 text-[9px] font-black uppercase tracking-[0.2em] transition-all flex items-center gap-2 clip-esports-small" :class="activeTab === 'P2P' ? 'bg-[#050505] text-emerald-400 border border-emerald-900/50 shadow-[0_0_15px_rgba(16,185,129,0.1)]' : 'bg-transparent text-zinc-600 hover:text-white'">
        <span class="material-symbols-rounded text-xs" :class="{'animate-spin': isFetchingP2P}">sync</span>
        Mercado P2P
      </button>
      <button v-if="isDarkWebActive" @click="activeTab = 'DARKWEB'" class="px-8 py-3 text-[9px] font-black uppercase tracking-[0.2em] transition-all flex items-center gap-2 clip-esports-small animate-pulse" :class="activeTab === 'DARKWEB' ? 'bg-rose-950/40 text-rose-500 border border-rose-900/50 shadow-[0_0_15px_rgba(225,29,72,0.2)]' : 'bg-rose-950/10 text-rose-800 hover:text-rose-500 border border-transparent hover:border-rose-900/30'">
        <span class="material-symbols-rounded text-xs">gpp_bad</span>
        Node Dark Web
      </button>
    </div>

    <div v-if="activeTab === 'STORE'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 px-2 pt-6 relative z-10">
      <div v-for="pack in mergedStorePacks" :key="pack.pack_type" class="relative group flex flex-col items-center perspective-1000">
        <div class="absolute -bottom-4 w-3/4 h-8 rounded-[100%] blur-xl transition-all duration-500 group-hover:blur-2xl group-hover:scale-110" :class="pack.glowClass"></div>
        <div class="absolute -bottom-1 w-1/2 h-1 rounded-[100%] transition-all duration-500 opacity-50 group-hover:opacity-100" :class="pack.coreGlowClass"></div>

        <div class="w-full bg-[#0a0a0c] border-2 flex flex-col items-center p-6 relative z-10 clip-esports transition-transform duration-500 group-hover:-translate-y-3 shadow-[inset_0_0_20px_rgba(0,0,0,0.8)]" :class="pack.borderClass">
          <div class="absolute inset-0 opacity-20 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.05)_4px,rgba(255,255,255,0.05)_8px)] pointer-events-none"></div>
          
          <div class="w-16 h-16 bg-[#050505] border border-zinc-800 flex items-center justify-center mb-5 rotate-45 group-hover:rotate-90 transition-transform duration-700 shadow-[0_0_15px_rgba(0,0,0,1)]">
            <span class="material-symbols-rounded text-4xl -rotate-45 group-hover:-rotate-90 transition-transform duration-700 drop-shadow-[0_0_10px_currentColor]" :class="pack.iconColor">inventory_2</span>
          </div>
          
          <h3 class="text-xl font-black text-white uppercase tracking-tighter italic mb-1 drop-shadow-md">{{ pack.title }}</h3>
          <p class="text-[8px] font-bold text-zinc-500 uppercase tracking-[0.2em] mb-4">Capacidade: {{ pack.pack_type }} Alvos</p>
          
          <div class="flex flex-col items-center mb-6 w-full bg-[#050505] py-2 border border-zinc-900 clip-esports-small relative overflow-hidden">
             <div class="absolute left-0 top-0 bottom-0 w-1" :class="pack.fluctuation >= 0 ? 'bg-rose-500' : 'bg-emerald-500'"></div>
             <span class="text-[8px] font-bold text-zinc-500 uppercase tracking-[0.2em] mb-1">Cotação Atual</span>
             <div class="flex items-center gap-2">
               <span class="text-xl font-mono font-black" :class="pack.fluctuation >= 0 ? 'text-rose-500' : 'text-emerald-500'">{{ pack.current_price.toLocaleString() }} C$</span>
               <span class="text-[9px] font-black flex items-center" :class="pack.fluctuation >= 0 ? 'text-rose-500' : 'text-emerald-500'">
                 <span class="material-symbols-rounded text-[10px]">{{ pack.fluctuation >= 0 ? 'trending_up' : 'trending_down' }}</span>
                 {{ Math.abs(pack.fluctuation).toFixed(1) }}%
               </span>
             </div>
          </div>
          
          <button @click="buyPack(pack.pack_type, pack.current_price)" :disabled="isBuying" class="w-full py-3 bg-[#050505] border text-[9px] font-black uppercase tracking-[0.2em] transition-all hover:bg-white hover:text-black hover:border-white clip-esports-small disabled:opacity-30 disabled:cursor-not-allowed" :class="pack.btnClass">
            Executar Ordem
          </button>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'P2P'" class="relative z-10 flex-1 overflow-y-auto pr-2 scrollbar-hide">
      <div v-if="p2pListings.length === 0" class="flex flex-col items-center justify-center h-full opacity-30 min-h-[40vh]">
        <span class="material-symbols-rounded text-6xl mb-4 text-zinc-600 drop-shadow-lg">storefront</span>
        <h2 class="text-xs font-black text-zinc-400 uppercase tracking-[0.4em]">Nenhum Contrato Ativo</h2>
      </div>
      
      <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-7 gap-4">
        <div v-for="listing in p2pListings" :key="listing.id" class="w-full mx-auto flex flex-col group relative">
          
          <template v-if="listing.card">
            <div class="aspect-[2/3] w-full mb-2 transform-gpu transition-transform duration-300 group-hover:-translate-y-2 relative z-10">
              <FantasyCard :card="listing.card" :force-reveal="true" :is-interactive="false" />
            </div>
            
            <button v-if="myCardIds.includes(listing.card.id) || listing.seller_id === store.profile?.id || listing.seller_id === store.user?.id" disabled class="w-full py-3 bg-[#050505] border-t border-zinc-800 text-zinc-600 text-[8px] font-black uppercase tracking-[0.3em] cursor-not-allowed clip-esports-small z-20">
              Ordem Própria
            </button>
            
            <div v-else-if="listing.is_auction" class="flex flex-col gap-1 w-full z-20">
              <input v-model="bidInputs[listing.id]" type="number" placeholder="Seu Lance C$" class="w-full py-2 bg-[#050505] border border-zinc-800 text-center text-white font-mono text-xs focus:outline-none focus:border-amber-500 clip-esports-small">
              <button @click="placeBid(listing.id)" :disabled="isBuying || !bidInputs[listing.id]" class="w-full py-2.5 bg-amber-600 text-black text-[9px] font-black uppercase tracking-[0.3em] hover:bg-amber-500 transition-colors clip-esports-small disabled:opacity-30">
                Licitar
              </button>
            </div>

            <button v-else @click="buyP2PCard(listing.id)" :disabled="isBuying" class="w-full py-3 bg-[#050505] border-t-2 border-emerald-600 text-emerald-500 text-[9px] font-black uppercase tracking-[0.3em] hover:bg-emerald-600 hover:text-black transition-colors flex items-center justify-center gap-1.5 clip-esports-small z-20 disabled:opacity-30 shadow-[0_-5px_15px_rgba(16,185,129,0.15)] hover:shadow-[0_0_20px_rgba(16,185,129,0.5)]">
              <span class="material-symbols-rounded text-[11px]">shopping_cart</span> {{ listing.price.toLocaleString() }}
            </button>
          </template>
        </div>
      </div>
    </div>

    <div v-if="activeTab === 'DARKWEB'" class="flex-1 flex items-center justify-center relative z-10 p-4">
      <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(225,29,72,0.1)_0%,transparent_70%)] pointer-events-none animate-pulse"></div>
      
      <div class="w-full max-w-lg bg-[#0a0a0c]/90 backdrop-blur-xl border border-rose-900/50 p-8 clip-esports relative shadow-[0_0_50px_rgba(225,29,72,0.1)]">
        <div class="absolute inset-0 bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(225,29,72,0.05)_2px,rgba(225,29,72,0.05)_4px)] pointer-events-none"></div>
        
        <div class="flex flex-col items-center text-center relative z-10">
          <div class="w-24 h-24 bg-rose-950/30 border border-rose-900 flex items-center justify-center mb-6 rotate-45 shadow-[0_0_30px_rgba(225,29,72,0.3)]">
            <span class="material-symbols-rounded text-6xl text-rose-500 -rotate-45">skull</span>
          </div>
          
          <h2 class="text-3xl font-black text-rose-500 uppercase tracking-tighter italic mb-2 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)]">Classified Crate</h2>
          <p class="text-[10px] font-mono text-zinc-400 uppercase tracking-widest mb-8">Conteúdo estritamente Lendário garantido. Rastreio bloqueado.</p>
          
          <div class="w-full bg-[#050505] border border-rose-900/50 p-4 mb-8 clip-esports-small flex justify-between items-center">
             <span class="text-[9px] font-black text-rose-500 uppercase tracking-[0.2em]">Custo da Transação</span>
             <span class="text-2xl font-mono font-black text-rose-500 drop-shadow-[0_0_8px_rgba(225,29,72,0.5)]">{{ darkWebPrice.toLocaleString() }} C$</span>
          </div>

          <button @click="buyDarkWebPack" :disabled="isBuying" class="w-full py-5 bg-rose-600 hover:bg-rose-500 text-black text-[12px] font-black uppercase tracking-[0.3em] transition-all clip-esports-small shadow-[0_0_20px_rgba(225,29,72,0.4)] disabled:opacity-30 disabled:grayscale">
            {{ isBuying ? 'Processando Rota...' : 'Adquirir Ativo Ilegal' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useFantasyStore } from '../stores/fantasy'
import { useToastStore } from '../stores/toast'
import FantasyCard from '../components/FantasyCard.vue'

const store = useFantasyStore()
const toastStore = useToastStore()

const activeTab = ref('STORE')
const isBuying = ref(false)
const isFetchingP2P = ref(false)
const isFetchingStore = ref(false)
const p2pListings = ref([])
const apiStorePacks = ref([])
const bidInputs = reactive({})

const isDarkWebActive = ref(false)
const darkWebPrice = ref(50000)
let pollInterval = null

const userBalance = computed(() => store.profile?.wallet_balance ?? store.user?.wallet_balance ?? 0)
const myCardIds = computed(() => store.cards ? store.cards.map(c => c.id) : [])

const visualPacksMeta = [
  { pack_type: "1", title: "Single", base_price: 1000, borderClass: "border-zinc-700", glowClass: "bg-zinc-600/20", coreGlowClass: "bg-zinc-400", iconColor: "text-zinc-500", btnClass: "border-zinc-700 text-zinc-400" },
  { pack_type: "3", title: "Tactical", base_price: 2800, borderClass: "border-blue-800", glowClass: "bg-blue-600/20", coreGlowClass: "bg-blue-400", iconColor: "text-blue-500", btnClass: "border-blue-800 text-blue-400" },
  { pack_type: "5", title: "Squad", base_price: 4500, borderClass: "border-purple-800", glowClass: "bg-purple-600/20", coreGlowClass: "bg-purple-400", iconColor: "text-purple-500", btnClass: "border-purple-800 text-purple-400" },
  { pack_type: "7", title: "Assault", base_price: 6000, borderClass: "border-orange-800", glowClass: "bg-orange-600/20", coreGlowClass: "bg-orange-400", iconColor: "text-orange-500", btnClass: "border-orange-800 text-orange-400" },
  { pack_type: "10", title: "Redzone", base_price: 8000, borderClass: "border-rose-800", glowClass: "bg-rose-600/20", coreGlowClass: "bg-rose-400", iconColor: "text-rose-500", btnClass: "border-rose-800 text-rose-400" }
]

const mergedStorePacks = computed(() => {
  if (!apiStorePacks.value || apiStorePacks.value.length === 0) {
    return visualPacksMeta.map(meta => ({ ...meta, current_price: meta.base_price, fluctuation: 0 }))
  }
  return visualPacksMeta.map(meta => {
    const apiData = apiStorePacks.value.find(p => p.pack_type === meta.pack_type)
    return apiData ? { ...meta, ...apiData } : { ...meta, current_price: meta.base_price, fluctuation: 0 }
  })
})

const fetchStoreData = async () => {
  if (isFetchingStore.value) return
  isFetchingStore.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/store`, { headers: store.getHeaders() })
    if (res.ok) apiStorePacks.value = await res.json()
  } catch (error) {
  } finally { isFetchingStore.value = false }
}

const checkDarkWebStatus = async () => {
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/darkweb/status`, { headers: store.getHeaders() })
    if (res.ok) {
      const data = await res.json()
      isDarkWebActive.value = data.is_active
      darkWebPrice.value = data.pack_price
    }
  } catch (error) {}
}

const fetchP2PListings = async () => {
  activeTab.value = 'P2P'
  if (isFetchingP2P.value) return
  isFetchingP2P.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p`, { headers: store.getHeaders() })
    if (res.ok) {
      const rawData = await res.json()
      p2pListings.value = rawData.filter(item => item.card != null)
    }
  } catch (error) {
    toastStore.showToast('Erro', 'Falha ao aceder à rede P2P.', 'error')
  } finally { isFetchingP2P.value = false }
}

const buyPack = async (packType, price) => {
  if (isBuying.value) return
  isBuying.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/buy/${packType}`, { 
      method: 'POST', 
      headers: { ...store.getHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ expected_price: price })
    })
    
    if (res.ok) {
      toastStore.showToast('Ordem Executada', `Suprimentos adquiridos.`, 'success')
      if (store.profile) store.profile.wallet_balance -= price
      await store.fetchPacks()
    } else {
      toastStore.showToast('Transação Negada', 'Fundos insuficientes ou preço alterado.', 'error')
    }
    await fetchStoreData() 
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor de transações offline.', 'error')
  } finally { isBuying.value = false }
}

const buyDarkWebPack = async () => {
  if (isBuying.value) return
  isBuying.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/darkweb/buy`, { method: 'POST', headers: store.getHeaders() })
    
    if (res.ok) {
      toastStore.showToast('Aquisição Ilegal', `Carga Classificada entregue.`, 'success')
      if (store.profile) store.profile.wallet_balance -= darkWebPrice.value
      await store.fetchPacks()
      activeTab.value = 'STORE'
    } else {
      toastStore.showToast('Transação Bloqueada', 'Fundos insuficientes.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Conexão perdida.', 'error')
  } finally { isBuying.value = false }
}

const buyP2PCard = async (listingId) => {
  if (isBuying.value) return
  isBuying.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p/buy/${listingId}`, { method: 'POST', headers: store.getHeaders() })
    if (res.ok) {
      toastStore.showToast('Transferência P2P', 'Ativo adquirido e transferido para o Arsenal.', 'success')
      await fetchP2PListings()
      await store.fetchCards()
      const data = await res.json()
      if (store.profile && data.new_balance) store.profile.wallet_balance = data.new_balance
    } else {
      toastStore.showToast('Ordem Rejeitada', 'Ação não permitida ou fundos insuficientes.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor offline.', 'error')
  } finally { isBuying.value = false }
}

const placeBid = async (listingId) => {
  if (isBuying.value || !bidInputs[listingId]) return
  isBuying.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p/bid/${listingId}`, { 
      method: 'POST', 
      headers: { ...store.getHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ bid_amount: bidInputs[listingId] })
    })
    
    if (res.ok) {
      toastStore.showToast('Licitação Aceite', 'Lideras o leilão por este ativo.', 'success')
      bidInputs[listingId] = ''
      await fetchP2PListings()
      const data = await res.json()
      if (store.profile && data.new_balance) store.profile.wallet_balance = data.new_balance
    } else {
      toastStore.showToast('Licitação Recusada', 'O valor deve ser superior.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor de leilões offline.', 'error')
  } finally { isBuying.value = false }
}

onMounted(() => {
  if(store.fetchProfile) store.fetchProfile().catch(() => {})
  store.fetchCards()
  fetchStoreData()
  checkDarkWebStatus()
  fetchP2PListings()
  
  pollInterval = setInterval(() => {
    if (activeTab.value === 'STORE') fetchStoreData()
    if (activeTab.value === 'DARKWEB') checkDarkWebStatus()
  }, 30000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.perspective-1000 { perspective: 1000px; }
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }
.clip-tab { clip-path: polygon(8px 0, calc(100% - 8px) 0, 100% 8px, 100% 100%, 0 100%, 0 8px); }

.animate-ticker {
  animation: tickerSlide 30s linear infinite;
}

@keyframes tickerSlide {
  0% { transform: translateX(100%); }
  100% { transform: translateX(-100%); }
}

.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>