<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center bg-black/98 p-4 md:p-8 backdrop-blur-xl">
    
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
       <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] blur-[120px] rounded-full opacity-10" :class="theme.bgClass"></div>
    </div>

    <div class="bg-[#050505] border border-zinc-800 w-full max-w-6xl flex flex-col md:flex-row relative clip-modal shadow-[0_0_100px_rgba(0,0,0,0.9)] z-10">
      
      <div class="absolute top-0 left-0 w-full h-1" :class="theme.bgClass"></div>

      <button @click="$emit('close')" class="absolute top-6 right-6 z-50 w-12 h-12 bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-500 hover:text-white hover:bg-rose-600 transition-all clip-esports-small">
        <span class="material-symbols-rounded text-xl">close</span>
      </button>

      <div class="w-full md:w-2/5 p-10 bg-[#08080a] flex items-center justify-center border-r border-zinc-900 relative overflow-visible">
        <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.01)_4px,rgba(255,255,255,0.01)_8px)] pointer-events-none"></div>
        <div class="absolute inset-y-10 left-4 w-px bg-gradient-to-b from-transparent via-zinc-800 to-transparent"></div>
        
        <div class="w-full max-w-[320px] h-full max-h-[480px] aspect-[2/3] relative z-10 mt-12 mb-6">
          <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" />
        </div>
      </div>

      <div class="w-full md:w-3/5 p-8 md:p-14 flex flex-col relative bg-[#050505]">
        <div class="mb-8 relative">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-1.5 h-1.5 rotate-45" :class="theme.bgClass"></div>
            <span class="text-[11px] font-black uppercase tracking-[0.5em] text-zinc-500">Combat_Record_System</span>
          </div>
          <h1 class="text-6xl font-black text-white tracking-tighter uppercase italic mb-4 drop-shadow-2xl">{{ card.player_nickname }}</h1>
          <div class="flex items-center gap-2">
            <span class="px-4 py-1.5 bg-zinc-900 border text-[10px] font-black uppercase tracking-[0.3em]" :class="[theme.borderClass, theme.textColor]">{{ card.rarity }} CLASS</span>
            <span class="px-4 py-1.5 bg-[#0a0a0c] text-[10px] font-mono text-zinc-600 border border-zinc-900 uppercase tracking-widest shadow-inner">SN: {{ card.serial_number }}</span>
          </div>
        </div>

        <div class="grid grid-cols-3 gap-1 mb-8 bg-zinc-900 border border-zinc-900 shadow-2xl">
          <div class="bg-[#0a0a0c] p-4 flex flex-col justify-between border-l-4" :class="theme.borderClass">
            <span class="text-[8px] font-black text-zinc-600 uppercase tracking-widest mb-1">Confirmed_Kills</span>
            <span class="text-3xl font-mono font-black text-white italic">{{ card.kills }}</span>
          </div>
          <div class="bg-[#0a0a0c] p-4 flex flex-col justify-between border-l-4" :class="theme.borderClass">
            <span class="text-[8px] font-black text-zinc-600 uppercase tracking-widest mb-1">Lethal_Precision</span>
            <span class="text-3xl font-mono font-black text-white italic">{{ card.headshots }}</span>
          </div>
          <div class="bg-[#0a0a0c] p-4 flex flex-col justify-between border-l-4" :class="theme.borderClass">
            <span class="text-[8px] font-black text-zinc-600 uppercase tracking-widest mb-1">Hardware_Integrity</span>
            <span class="text-2xl font-mono font-black italic drop-shadow-md" :class="floatColor">{{ card.float_value.toFixed(4) }}</span>
          </div>
        </div>

        <div class="mb-8 w-full bg-[#0a0a0c] border border-zinc-900 p-5 clip-esports-small relative overflow-hidden flex flex-col justify-center min-h-[140px]">
          <div class="absolute inset-0 bg-[repeating-linear-gradient(90deg,transparent,transparent_20px,rgba(255,255,255,0.02)_20px,rgba(255,255,255,0.02)_21px)] pointer-events-none"></div>
          <div class="flex justify-between items-center mb-4 relative z-10">
            <span class="text-[9px] font-black text-zinc-500 uppercase tracking-widest">Market_Volatility (7D)</span>
            <span v-if="isFetchingHistory" class="material-symbols-rounded text-zinc-600 animate-spin text-sm">sync</span>
            <span v-else-if="historyTrend !== 0" class="text-[10px] font-black flex items-center gap-1" :class="historyTrend > 0 ? 'text-emerald-500' : 'text-rose-500'">
              <span class="material-symbols-rounded text-[12px]">{{ historyTrend > 0 ? 'trending_up' : 'trending_down' }}</span>
              {{ Math.abs(historyTrend).toFixed(1) }}%
            </span>
          </div>
          
          <div class="relative w-full h-16 z-10 flex items-end">
             <svg v-if="sparklinePoints" viewBox="0 0 100 30" class="w-full h-full overflow-visible" preserveAspectRatio="none">
               <polyline fill="none" :stroke="theme.hexColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" :points="sparklinePoints" class="drop-shadow-[0_2px_5px_currentColor]"/>
               <circle v-for="(point, index) in rawPoints" :key="index" :cx="point.x" :cy="point.y" r="1.5" :fill="theme.hexColor" />
             </svg>
             <div v-else class="w-full h-full flex items-center justify-center">
               <span class="text-[9px] font-mono text-zinc-600">A processar dados de telemetria...</span>
             </div>
          </div>
        </div>

        <div class="mt-auto pt-6 border-t border-zinc-900/50 flex flex-col gap-4">
          <div v-if="card.is_listed" class="flex flex-col gap-3">
            <div class="bg-emerald-950/20 border border-emerald-900/40 p-4 text-center clip-esports-small">
              <span class="text-[10px] font-black text-emerald-500 uppercase tracking-[0.4em] animate-pulse">Asset_In_Network_Trade</span>
            </div>
            <button @click="cancelListing" :disabled="isProcessing" class="w-full py-4 bg-zinc-950 border border-zinc-800 hover:bg-rose-600/20 hover:border-rose-600/50 text-zinc-500 hover:text-rose-500 text-[9px] font-black uppercase tracking-[0.4em] transition-all clip-esports-small disabled:opacity-30">
              Revoke_Authorization
            </button>
          </div>
          
          <div v-else-if="card.squad_position !== null" class="bg-zinc-900/30 border border-zinc-800 p-5 text-center clip-esports-small border-l-4 border-l-blue-600">
            <span class="text-[10px] font-black text-zinc-500 uppercase tracking-[0.4em]">Active_Operational_Duty</span>
          </div>
          
          <div v-else class="flex flex-col gap-3">
            <div class="flex gap-2 p-1 bg-zinc-900 clip-esports-small w-fit">
              <button @click="tradeMode = 'FIXED'" class="px-5 py-2 text-[8px] font-black uppercase tracking-[0.3em] transition-colors clip-esports-small" :class="tradeMode === 'FIXED' ? 'bg-[#050505] text-white border border-zinc-700' : 'text-zinc-500 hover:text-white'">Venda Direta</button>
              <button @click="tradeMode = 'AUCTION'" class="px-5 py-2 text-[8px] font-black uppercase tracking-[0.3em] transition-colors clip-esports-small" :class="tradeMode === 'AUCTION' ? 'bg-amber-950/40 text-amber-500 border border-amber-900/50' : 'text-zinc-500 hover:text-white'">Leilão Público</button>
            </div>

            <div class="flex flex-col xl:flex-row gap-3">
              <div class="flex-1 relative h-14 group">
                <span class="absolute left-5 top-1/2 -translate-y-1/2 text-zinc-700 font-mono font-black text-lg group-focus-within:text-emerald-500 transition-colors">C$</span>
                <input v-model="sellPrice" type="number" :placeholder="tradeMode === 'FIXED' ? 'SET_FIXED_PRICE' : 'STARTING_BID'" class="w-full h-full bg-[#08080a] border border-zinc-800 pl-14 pr-4 text-white font-mono text-xl focus:outline-none focus:border-emerald-600 transition-all clip-esports-small placeholder:text-zinc-800">
              </div>
              <button @click="sellCard" :disabled="isProcessing || !sellPrice || sellPrice <= 0" class="xl:w-1/2 h-14 text-black text-[10px] font-black uppercase tracking-[0.4em] transition-all clip-esports-small disabled:opacity-20 disabled:grayscale active:scale-95" :class="tradeMode === 'FIXED' ? 'bg-emerald-600 hover:bg-emerald-500 shadow-[0_0_20px_rgba(16,185,129,0.2)]' : 'bg-amber-500 hover:bg-amber-400 shadow-[0_0_20px_rgba(245,158,11,0.2)]'">
                {{ tradeMode === 'FIXED' ? 'Execute_Order' : 'Start_Auction' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import FantasyCard from './FantasyCard.vue'
import { useFantasyStore } from '../stores/fantasy'
import { useToastStore } from '../stores/toast'

const props = defineProps({
  card: Object
})

const emit = defineEmits(['close'])
const store = useFantasyStore()
const toastStore = useToastStore()

const sellPrice = ref(null)
const isProcessing = ref(false)
const tradeMode = ref('FIXED') 

const isFetchingHistory = ref(false)
const marketHistory = ref([])

const theme = computed(() => {
  const themes = {
    COMMON: { borderClass: 'border-zinc-500', textColor: 'text-zinc-400', bgClass: 'bg-zinc-500', hexColor: '#71717a' },
    RARE: { borderClass: 'border-blue-600', textColor: 'text-blue-400', bgClass: 'bg-blue-600', hexColor: '#2563eb' },
    EPIC: { borderClass: 'border-purple-600', textColor: 'text-purple-400', bgClass: 'bg-purple-600', hexColor: '#9333ea' },
    LEGENDARY: { borderClass: 'border-emerald-500', textColor: 'text-emerald-400', bgClass: 'bg-emerald-500', hexColor: '#10b981' }
  }
  return themes[props.card.rarity] || themes.COMMON
})

const floatColor = computed(() => {
  if (props.card.float_value < 0.1) return 'text-emerald-400'
  if (props.card.float_value < 0.5) return 'text-blue-400'
  if (props.card.float_value < 0.8) return 'text-yellow-500'
  return 'text-rose-600'
})

const historyTrend = computed(() => {
  if (marketHistory.value.length < 2) return 0
  const first = marketHistory.value[0].price
  const last = marketHistory.value[marketHistory.value.length - 1].price
  return ((last - first) / first) * 100
})

const rawPoints = computed(() => {
  if (marketHistory.value.length === 0) return []
  const prices = marketHistory.value.map(h => h.price)
  const minPrice = Math.min(...prices) * 0.95
  const maxPrice = Math.max(...prices) * 1.05
  const range = maxPrice - minPrice || 1
  
  return marketHistory.value.map((h, i) => {
    const x = (i / (marketHistory.value.length - 1)) * 100
    const y = 30 - (((h.price - minPrice) / range) * 30)
    return { x: x.toFixed(2), y: y.toFixed(2) }
  })
})

const sparklinePoints = computed(() => {
  if (rawPoints.value.length === 0) return null
  return rawPoints.value.map(p => `${p.x},${p.y}`).join(' ')
})

const fetchHistory = async () => {
  isFetchingHistory.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p/history/${props.card.id}`, { headers: store.getHeaders() })
    if (res.ok) {
      marketHistory.value = await res.json()
    }
  } catch (error) {
  } finally {
    isFetchingHistory.value = false
  }
}

const sellCard = async () => {
  if (!sellPrice.value || sellPrice.value <= 0) return
  isProcessing.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p/sell/${props.card.id}`, {
      method: 'POST',
      headers: { ...store.getHeaders(), 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        price: sellPrice.value,
        is_auction: tradeMode.value === 'AUCTION'
      })
    })
    if (res.ok) {
      toastStore.showToast(tradeMode.value === 'FIXED' ? 'Ordem Executada' : 'Leilão Iniciado', 'Operador listado na rede.', 'success')
      await store.fetchCards()
      emit('close')
    } else {
      toastStore.showToast('Erro de Sistema', 'Falha ao autenticar ordem.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro de Rede', 'Servidor inacessível.', 'error')
  } finally { isProcessing.value = false }
}

const cancelListing = async () => {
  if (!props.card.listing_id) return
  isProcessing.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p/cancel/${props.card.listing_id}`, {
      method: 'DELETE',
      headers: store.getHeaders()
    })
    if (res.ok) {
      toastStore.showToast('Contrato Revogado', 'Operador retornou ao Arsenal Local.', 'warning')
      await store.fetchCards()
      emit('close')
    }
  } catch (error) {} finally { isProcessing.value = false }
}

onMounted(() => {
  fetchHistory()
})
</script>

<style scoped>
.clip-modal { clip-path: polygon(40px 0, 100% 0, 100% calc(100% - 40px), calc(100% - 40px) 100%, 0 100%, 0 40px); }
.clip-esports-small { clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }
</style>