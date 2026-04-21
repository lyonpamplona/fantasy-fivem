<template>
  <div class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 md:p-8 backdrop-blur-md">
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
       <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] blur-[120px] rounded-full opacity-10" :class="theme.bgClass"></div>
    </div>

    <div class="bg-[#18181b] border border-zinc-700 w-full max-w-6xl flex flex-col md:flex-row relative clip-modal shadow-2xl z-10 overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-1" :class="theme.bgClass"></div>
      <button @click="$emit('close')" class="absolute top-4 right-4 md:top-6 md:right-6 z-50 w-10 h-10 md:w-12 md:h-12 bg-zinc-900 border border-zinc-700 flex items-center justify-center text-zinc-400 hover:text-white hover:bg-rose-500 transition-all clip-esports-small shadow-sm">
        <span class="material-symbols-rounded text-lg md:text-xl">close</span>
      </button>

      <div class="w-full md:w-2/5 p-6 md:p-10 bg-zinc-900/50 flex items-center justify-center border-b md:border-b-0 md:border-r border-zinc-800 relative">
        <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.02)_4px,rgba(255,255,255,0.02)_8px)] pointer-events-none"></div>
        <div class="w-full max-w-[240px] md:max-w-[320px] aspect-[2/3] relative z-10 my-4 md:mt-12 md:mb-6">
          <FantasyCard :card="card" :force-reveal="true" :is-interactive="false" />
        </div>
      </div>

      <div class="w-full md:w-3/5 p-6 md:p-14 flex flex-col relative bg-[#18181b] overflow-y-auto max-h-[60vh] md:max-h-[80vh] custom-scrollbar">
        <div class="mb-6 md:mb-8 relative">
          <h1 class="text-3xl md:text-6xl font-black text-zinc-100 tracking-tighter uppercase italic mb-3 md:mb-4 truncate">{{ card.player_nickname }}</h1>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="px-3 md:px-4 py-1 md:py-1.5 bg-zinc-900 border text-[8px] md:text-[10px] font-black uppercase tracking-[0.3em]" :class="[theme.borderClass, theme.textColor]">{{ card.rarity }} CLASS</span>
            <span class="px-3 md:px-4 py-1 md:py-1.5 bg-zinc-950 text-[8px] md:text-[10px] font-mono text-zinc-400 border border-zinc-800 uppercase tracking-widest shadow-inner truncate">SN: {{ card.serial_number }}</span>
            <span v-if="card.is_forged" class="px-3 md:px-4 py-1 md:py-1.5 bg-amber-950/20 text-[8px] md:text-[10px] font-black text-amber-400 border border-amber-800/30 uppercase tracking-[0.2em] flex items-center gap-1">
              <span class="material-symbols-rounded text-[10px] md:text-[12px]">local_fire_department</span> Forged
            </span>
          </div>
        </div>

        <div class="flex flex-wrap gap-2 p-1 bg-zinc-900 clip-esports-small w-fit mb-6 border border-zinc-800">
           <button @click="activePanel = 'STATS'" class="px-4 md:px-6 py-2 text-[8px] md:text-[9px] font-black uppercase tracking-[0.3em] transition-colors clip-esports-small" :class="activePanel === 'STATS' ? 'bg-[#18181b] text-white border border-zinc-700 shadow-sm' : 'text-zinc-400 hover:text-white'">Estatísticas</button>
           <button @click="activePanel = 'MARKET'" class="px-4 md:px-6 py-2 text-[8px] md:text-[9px] font-black uppercase tracking-[0.3em] transition-colors clip-esports-small" :class="activePanel === 'MARKET' ? 'bg-amber-950/30 text-amber-400 border border-amber-800/50 shadow-sm' : 'text-zinc-400 hover:text-white'">Mercado</button>
           <button @click="activePanel = 'OPERATIONS'" class="px-4 md:px-6 py-2 text-[8px] md:text-[9px] font-black uppercase tracking-[0.3em] transition-colors clip-esports-small" :class="activePanel === 'OPERATIONS' ? 'bg-indigo-950/30 text-indigo-400 border border-indigo-800/50 shadow-sm' : 'text-zinc-400 hover:text-white'">Staking</button>
        </div>

        <div v-if="activePanel === 'STATS'" class="flex flex-col gap-6">
          <div class="grid grid-cols-3 gap-2">
            <div class="bg-zinc-900 p-3 md:p-4 border-l-2 md:border-l-4 flex flex-col justify-center shadow-sm" :class="theme.borderClass">
              <span class="text-[7px] md:text-[8px] font-black text-zinc-500 uppercase tracking-widest block mb-1">Confirmed_Kills</span>
              <span class="text-lg md:text-2xl font-mono font-black text-zinc-100 leading-none">{{ card.kills }}</span>
            </div>
            <div class="bg-zinc-900 p-3 md:p-4 border-l-2 md:border-l-4 flex flex-col justify-center shadow-sm" :class="theme.borderClass">
              <span class="text-[7px] md:text-[8px] font-black text-zinc-500 uppercase tracking-widest block mb-1">Headshots</span>
              <span class="text-lg md:text-2xl font-mono font-black text-zinc-100 leading-none">{{ card.headshots }}</span>
            </div>
            <div class="bg-zinc-900 p-3 md:p-4 border-l-2 md:border-l-4 flex flex-col justify-center shadow-sm" :class="theme.borderClass">
              <span class="text-[7px] md:text-[8px] font-black text-zinc-500 uppercase tracking-widest block mb-1">Float_Value</span>
              <span class="text-base md:text-xl font-mono font-black leading-none" :class="floatColor">{{ card.float_value.toFixed(4) }}</span>
            </div>
          </div>

          <div class="bg-zinc-900 border border-zinc-800 p-4 md:p-6 clip-esports-small shadow-sm">
            <h3 class="text-[9px] md:text-[10px] font-black text-zinc-400 uppercase tracking-widest mb-4">Análise de Performance Visual</h3>
            <div class="flex flex-col gap-4">
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-[7px] md:text-[8px] font-mono text-zinc-400">Poder de Fogo (Kills)</span>
                  <span class="text-[7px] md:text-[8px] font-mono text-emerald-400">{{ Math.min(100, (card.kills / 100) * 100).toFixed(0) }}%</span>
                </div>
                <div class="w-full bg-zinc-950 h-1.5 overflow-hidden rounded-full">
                  <div class="bg-emerald-500 h-full transition-all" :style="{ width: Math.min(100, (card.kills / 100) * 100) + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-[7px] md:text-[8px] font-mono text-zinc-400">Precisão Letal (HS)</span>
                  <span class="text-[7px] md:text-[8px] font-mono text-amber-400">{{ Math.min(100, (card.headshots / 50) * 100).toFixed(0) }}%</span>
                </div>
                <div class="w-full bg-zinc-950 h-1.5 overflow-hidden rounded-full">
                  <div class="bg-amber-500 h-full transition-all" :style="{ width: Math.min(100, (card.headshots / 50) * 100) + '%' }"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-[7px] md:text-[8px] font-mono text-zinc-400">Integridade (Inverso do Float)</span>
                  <span class="text-[7px] md:text-[8px] font-mono" :class="floatColor">{{ ((1 - card.float_value) * 100).toFixed(0) }}%</span>
                </div>
                <div class="w-full bg-zinc-950 h-1.5 overflow-hidden rounded-full">
                  <div class="h-full transition-all" :class="floatColor.replace('text-', 'bg-')" :style="{ width: ((1 - card.float_value) * 100) + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="activePanel === 'MARKET'" class="bg-zinc-900 border border-amber-900/40 p-4 md:p-6 clip-esports-small flex flex-col gap-4 shadow-sm">
          <div class="flex items-center gap-3 mb-2">
            <span class="material-symbols-rounded text-amber-500 text-xl md:text-2xl">storefront</span>
            <h3 class="text-base md:text-lg font-black text-amber-500 uppercase tracking-widest">Listagem de Mercado</h3>
          </div>
          <p class="text-[9px] md:text-[10px] font-mono text-zinc-400 mb-2 md:mb-4">Insira o valor pretendido para vender este operador na rede P2P.</p>
          <div class="flex flex-col sm:flex-row gap-3 md:gap-4">
            <div class="relative flex-1">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500 font-mono">C$</span>
              <input v-model="sellPrice" type="number" min="1" class="w-full bg-zinc-950 border border-zinc-700 text-zinc-100 font-mono text-base md:text-lg py-2.5 md:py-3 pl-12 pr-4 focus:outline-none focus:border-amber-500 transition-colors clip-esports-small" placeholder="0">
            </div>
            <button @click="listOnMarket" :disabled="isProcessing || !sellPrice || sellPrice <= 0" class="w-full sm:w-auto px-8 py-3 bg-amber-600 hover:bg-amber-500 text-zinc-950 font-black uppercase tracking-widest text-[9px] md:text-[10px] transition-colors clip-esports-small disabled:opacity-30 shadow-[0_0_15px_rgba(217,119,6,0.2)]">
              Vender
            </button>
          </div>
        </div>

        <div v-if="activePanel === 'OPERATIONS'" class="bg-zinc-900 border border-indigo-900/40 p-4 md:p-6 clip-esports-small flex flex-col gap-4 md:gap-6 shadow-sm">
           <div class="flex items-start gap-4">
             <div class="w-10 h-10 md:w-12 md:h-12 bg-indigo-950/20 border border-indigo-800/50 flex items-center justify-center shrink-0 shadow-[0_0_15px_rgba(79,70,229,0.1)]">
                <span class="material-symbols-rounded text-indigo-400 text-xl md:text-2xl">assignment</span>
             </div>
             <div>
               <h3 class="text-base md:text-lg font-black text-indigo-400 uppercase tracking-widest mb-1">Staking Tático</h3>
               <p class="text-[9px] md:text-[10px] font-mono text-zinc-400 leading-relaxed">Assine um contrato para enviar este operador para missões off-grid. O ativo ficará indisponível durante a operação, mas gerará C$ passivamente.</p>
             </div>
           </div>
           <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 md:gap-4">
             <button @click="signContract(3)" :disabled="isProcessing" class="flex flex-col items-center p-3 md:p-4 bg-zinc-950 border border-zinc-800 hover:border-indigo-500 transition-all clip-esports-small group disabled:opacity-30">
                <span class="text-[9px] md:text-[10px] font-black text-zinc-500 group-hover:text-zinc-300 uppercase tracking-widest mb-1 md:mb-2">Reconhecimento</span>
                <span class="text-lg md:text-xl font-mono font-black text-indigo-400">3 Dias</span>
             </button>
             <button @click="signContract(7)" :disabled="isProcessing" class="flex flex-col items-center p-3 md:p-4 bg-zinc-950 border border-zinc-800 hover:border-indigo-500 transition-all clip-esports-small group disabled:opacity-30">
                <span class="text-[9px] md:text-[10px] font-black text-zinc-500 group-hover:text-zinc-300 uppercase tracking-widest mb-1 md:mb-2">Infiltração</span>
                <span class="text-lg md:text-xl font-mono font-black text-indigo-400">7 Dias</span>
             </button>
             <button @click="signContract(14)" :disabled="isProcessing" class="flex flex-col items-center p-3 md:p-4 bg-zinc-950 border border-zinc-800 hover:border-indigo-500 transition-all clip-esports-small group disabled:opacity-30">
                <span class="text-[9px] md:text-[10px] font-black text-zinc-500 group-hover:text-zinc-300 uppercase tracking-widest mb-1 md:mb-2">Black Ops</span>
                <span class="text-lg md:text-xl font-mono font-black text-indigo-400">14 Dias</span>
             </button>
           </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import FantasyCard from './FantasyCard.vue'
import { useFantasyStore } from '../stores/fantasy'
import { useToastStore } from '../stores/toast'

const props = defineProps({ card: Object })
const emit = defineEmits(['close', 'contract-signed'])
const store = useFantasyStore()
const toastStore = useToastStore()

const activePanel = ref('STATS')
const isProcessing = ref(false)
const sellPrice = ref('')

const theme = computed(() => {
  const themes = {
    COMMON: { borderClass: 'border-zinc-500', textColor: 'text-zinc-400', bgClass: 'bg-zinc-600' },
    RARE: { borderClass: 'border-blue-600', textColor: 'text-blue-400', bgClass: 'bg-blue-600' },
    EPIC: { borderClass: 'border-purple-600', textColor: 'text-purple-400', bgClass: 'bg-purple-600' },
    LEGENDARY: { borderClass: 'border-emerald-500', textColor: 'text-emerald-400', bgClass: 'bg-emerald-500' },
    MYTHIC: { borderClass: 'border-amber-500', textColor: 'text-amber-400', bgClass: 'bg-amber-500' }
  }
  return themes[props.card.rarity] || themes.COMMON
})

const floatColor = computed(() => {
  if (props.card.float_value < 0.1) return 'text-emerald-400'
  if (props.card.float_value < 0.5) return 'text-blue-400'
  if (props.card.float_value < 0.8) return 'text-yellow-400'
  return 'text-rose-500'
})

const listOnMarket = async () => {
  if (isProcessing.value || !sellPrice.value) return
  isProcessing.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/market/p2p/sell/${props.card.id}`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify({ price: parseInt(sellPrice.value), is_auction: false })
    })
    
    if (res.ok) {
      toastStore.showToast('Mercado P2P', 'Operador listado com sucesso.', 'success')
      emit('close')
      await store.fetchCards()
    } else {
      const errData = await res.json().catch(() => ({}))
      toastStore.showToast('Erro', errData.detail || 'Falha ao listar.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor offline.', 'error')
  } finally {
    isProcessing.value = false
  }
}

const signContract = async (days) => {
  if (isProcessing.value) return
  isProcessing.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    const res = await fetch(`${baseUrl}/api/cards/${props.card.id}/contract`, {
      method: 'POST',
      headers: store.getHeaders(),
      body: JSON.stringify({ duration_days: days })
    })
    if (res.ok) {
      toastStore.showToast('Operação Autorizada', `Contrato assinado para ${days} dias.`, 'success')
      emit('contract-signed')
    } else {
      const errData = await res.json().catch(() => ({}))
      toastStore.showToast('Erro', errData.detail || 'Ativo já em uso.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro Crítico', 'Servidor offline.', 'error')
  } finally {
    isProcessing.value = false
  }
}

const handleKeydown = (e) => {
  if (e.key === 'Escape' || e.key === 'Esc') {
    emit('close')
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #52525b; }

.clip-modal { clip-path: polygon(30px 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%, 0 30px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }
</style>