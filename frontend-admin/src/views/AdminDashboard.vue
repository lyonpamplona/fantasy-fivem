<template>
  <div class="min-h-screen bg-[#050505] text-white p-4 flex flex-col font-sans overflow-x-hidden">
    
    <header class="w-full max-w-[1800px] mx-auto mb-8 bg-[#0a0a0c] border-b-2 border-zinc-900 px-8 py-5 flex flex-col md:flex-row items-center justify-between shadow-[0_10px_30px_rgba(0,0,0,0.8)] z-40 relative clip-esports">
      <div class="flex items-center gap-5">
        <div class="w-12 h-12 bg-[#050505] border border-rose-900 flex items-center justify-center rotate-45 shadow-[0_0_20px_rgba(244,63,94,0.15)]">
          <span class="material-symbols-rounded text-rose-500 text-2xl -rotate-45">radar</span>
        </div>
        <div class="flex flex-col">
          <h1 class="text-3xl font-black tracking-tighter text-white leading-none italic uppercase">Heurística <span class="text-rose-600">Core</span></h1>
          <span class="text-[9px] font-bold text-zinc-500 uppercase tracking-[0.3em] mt-1">Terminal de Segurança Anti-Cheat</span>
        </div>
      </div>

      <div class="flex items-center gap-3 mt-4 md:mt-0">
        <button @click="seedMocks" :disabled="isProcessing" class="px-5 py-3 bg-[#050505] border border-zinc-800 text-[9px] font-black uppercase tracking-[0.2em] text-zinc-400 hover:text-white hover:border-zinc-500 transition-colors clip-esports-small disabled:opacity-30">
          Gerar Anomalias
        </button>
        <button @click="clearMocks" :disabled="isProcessing" class="px-5 py-3 bg-[#050505] border border-zinc-800 text-[9px] font-black uppercase tracking-[0.2em] text-zinc-400 hover:text-rose-500 hover:border-rose-800 transition-colors clip-esports-small disabled:opacity-30">
          Expurgar
        </button>
        <button @click="fetchSuspects" :disabled="isProcessing" class="w-12 h-12 bg-emerald-600 hover:bg-emerald-500 text-black flex items-center justify-center transition-colors clip-esports-small disabled:opacity-30 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
          <span class="material-symbols-rounded text-lg" :class="{'animate-spin': isProcessing}">refresh</span>
        </button>
        <div class="w-[1px] h-8 bg-zinc-800 mx-2"></div>
        <button @click="handleLogout" class="px-5 py-3 bg-zinc-950 border border-zinc-800 text-[9px] font-black uppercase tracking-[0.2em] text-zinc-500 hover:text-rose-500 hover:bg-[#0a0a0c] transition-colors flex items-center gap-2 clip-esports-small">
          <span class="material-symbols-rounded text-sm">logout</span> Sair
        </button>
      </div>
    </header>

    <main class="w-full max-w-[1800px] mx-auto flex-1 flex flex-col">
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
        <div class="bg-[#0a0a0c] border-l-4 border-zinc-700 p-5 flex items-center justify-between clip-esports-small shadow-[0_5px_20px_rgba(0,0,0,0.5)]">
          <div class="flex flex-col">
            <span class="text-[9px] font-black text-zinc-500 uppercase tracking-[0.2em]">Total Monitorado</span>
            <span class="text-4xl font-mono font-black text-white mt-1">{{ suspects.length }}</span>
          </div>
          <span class="material-symbols-rounded text-5xl text-zinc-800">monitoring</span>
        </div>
        <div class="bg-[#0a0a0c] border-l-4 border-rose-600 p-5 flex items-center justify-between clip-esports-small shadow-[0_5px_20px_rgba(0,0,0,0.5)]">
          <div class="flex flex-col">
            <span class="text-[9px] font-black text-rose-500/70 uppercase tracking-[0.2em]">Ameaças Críticas</span>
            <span class="text-4xl font-mono font-black text-rose-500 mt-1 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)]">{{ criticalCount }}</span>
          </div>
          <span class="material-symbols-rounded text-5xl text-rose-950">warning</span>
        </div>
        <div class="bg-[#0a0a0c] border-l-4 border-emerald-600 p-5 flex items-center justify-between clip-esports-small shadow-[0_5px_20px_rgba(0,0,0,0.5)]">
          <div class="flex flex-col">
            <span class="text-[9px] font-black text-emerald-600/70 uppercase tracking-[0.2em]">Média Global</span>
            <span class="text-4xl font-mono font-black text-emerald-500 mt-1">{{ averageScore.toFixed(1) }}</span>
          </div>
          <span class="material-symbols-rounded text-5xl text-emerald-950">analytics</span>
        </div>
      </div>

      <div v-if="suspects.length === 0" class="flex flex-col items-center justify-center flex-1 opacity-30 py-20">
        <span class="material-symbols-rounded text-7xl mb-4 text-zinc-600">policy</span>
        <h2 class="text-sm font-black text-zinc-500 uppercase tracking-[0.4em]">Perímetro Seguro</h2>
      </div>

      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-5 pb-10">
        <div v-for="player in suspects" :key="player.id" class="bg-[#0a0a0c] border border-zinc-900 p-5 flex flex-col relative group hover:bg-[#0c0c0e] transition-colors clip-esports shadow-lg">
          
          <div class="absolute top-0 right-0 w-full h-1" :class="getScoreBg(player.suspicion_score)"></div>

          <div class="relative z-10 flex items-center gap-3 mb-5">
            <div class="w-10 h-10 bg-[#050505] border border-zinc-800 flex items-center justify-center clip-esports-small">
              <span class="material-symbols-rounded text-zinc-600 text-lg">person</span>
            </div>
            <div class="flex flex-col overflow-hidden">
              <span class="text-xs font-black text-white uppercase tracking-widest truncate italic">{{ player.nickname || 'Unknown' }}</span>
              <span class="text-[8px] font-mono text-zinc-500 truncate">ID: {{ player.fivem_id }}</span>
            </div>
          </div>

          <div class="relative z-10 flex flex-col items-center justify-center bg-[#050505] py-4 border border-zinc-800 mb-5 clip-esports-small">
            <span class="text-[7px] font-black text-zinc-500 uppercase tracking-[0.3em] mb-1">Suspicion Score</span>
            <span class="text-4xl font-mono font-black leading-none drop-shadow-md" :class="getScoreColor(player.suspicion_score)">
              {{ player.suspicion_score.toFixed(1) }}
            </span>
          </div>

          <div class="relative z-10 grid grid-cols-2 gap-2 mb-5">
            <div class="bg-[#050505] p-2 flex flex-col items-center border border-zinc-900 clip-esports-small">
              <span class="text-[7px] font-bold text-zinc-600 uppercase tracking-widest mb-1">Status</span>
              <span class="text-[9px] font-black uppercase tracking-widest" :class="player.is_quarantined ? 'text-rose-600' : 'text-emerald-500'">
                {{ player.is_quarantined ? 'Bloqueado' : 'Livre' }}
              </span>
            </div>
            <div class="bg-[#050505] p-2 flex flex-col items-center border border-zinc-900 clip-esports-small">
              <span class="text-[7px] font-bold text-zinc-600 uppercase tracking-widest mb-1">VIP</span>
              <span class="text-[9px] font-black uppercase tracking-widest text-zinc-400">
                {{ player.is_vip ? 'Sim' : 'Não' }}
              </span>
            </div>
          </div>

          <div class="relative z-10 mt-auto grid grid-cols-2 gap-2">
            <button @click="openInjectModal(player)" class="py-2.5 bg-zinc-900 text-emerald-500 text-[8px] font-black uppercase tracking-[0.2em] hover:bg-emerald-600 hover:text-black transition-colors clip-esports-small">
              Injetar C$
            </button>
            <button @click="viewDossier(player.id)" class="py-2.5 bg-zinc-900 text-zinc-300 text-[8px] font-black uppercase tracking-[0.2em] hover:bg-white hover:text-black transition-colors clip-esports-small">
              Dossiê
            </button>
            <button @click="toggleQuarantine(player)" class="col-span-2 py-2.5 text-[9px] font-black uppercase tracking-[0.2em] transition-colors clip-esports-small" :class="player.is_quarantined ? 'bg-zinc-800 text-zinc-400 hover:bg-zinc-700' : 'bg-rose-950/50 text-rose-500 hover:bg-rose-600 hover:text-black border border-rose-900/50'">
              {{ player.is_quarantined ? 'Desbloquear Alvo' : 'Protocolo Bloqueio' }}
            </button>
          </div>
        </div>
      </div>
    </main>

    <div v-if="selectedPlayer" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/90 p-4 backdrop-blur-sm">
      <div class="bg-[#0a0a0c] border border-zinc-800 w-full max-w-sm p-8 relative clip-modal shadow-[0_0_50px_rgba(0,0,0,0.9)]">
        <button @click="selectedPlayer = null" class="absolute top-4 right-4 w-8 h-8 bg-[#050505] border border-zinc-800 flex items-center justify-center text-zinc-500 hover:text-white hover:bg-rose-600 transition-colors clip-esports-small">
          <span class="material-symbols-rounded text-sm">close</span>
        </button>
        <div class="mb-8">
          <h2 class="text-2xl font-black text-white tracking-tighter uppercase italic">Injeção de Capital</h2>
          <p class="text-[9px] font-mono text-zinc-500 uppercase tracking-[0.2em] mt-1">Alvo: {{ selectedPlayer.nickname }}</p>
        </div>
        <div class="relative h-14 mb-8">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-600 font-mono font-black text-lg">C$</span>
          <input v-model="injectAmount" type="number" class="w-full h-full bg-[#050505] border border-zinc-800 pl-12 pr-4 text-white font-mono text-lg focus:outline-none focus:border-emerald-600 clip-esports-small">
        </div>
        <button @click="confirmInjection" :disabled="isProcessing || !injectAmount" class="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-black font-black text-[10px] uppercase tracking-[0.3em] disabled:opacity-30 clip-esports-small transition-colors">
          Confirmar Envio
        </button>
      </div>
    </div>

    <div v-if="showDossier && selectedDossier" class="fixed inset-0 z-[200] flex items-center justify-center bg-black/95 p-4 md:p-8 backdrop-blur-sm">
      <div class="bg-[#050505] border border-zinc-800 w-full max-w-6xl flex flex-col md:flex-row relative clip-modal shadow-[0_0_100px_rgba(0,0,0,0.9)] overflow-hidden">
        
        <button @click="closeDossier" class="absolute top-6 right-6 z-50 w-12 h-12 bg-[#0a0a0c] border border-zinc-800 flex items-center justify-center text-zinc-500 hover:text-white hover:bg-rose-600 transition-colors clip-esports-small">
          <span class="material-symbols-rounded">close</span>
        </button>

        <div class="w-full md:w-2/5 p-10 bg-[#0a0a0c] border-r border-zinc-900 flex flex-col items-center relative">
          <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.01)_4px,rgba(255,255,255,0.01)_8px)] pointer-events-none"></div>
          <h3 class="text-[10px] font-black text-zinc-500 uppercase tracking-[0.3em] mb-8 relative z-10">Análise Balística</h3>
          
          <div class="relative w-[200px] h-[350px] flex flex-col items-center justify-start gap-1 z-10">
            <div class="w-16 h-16 border-2 bg-[#050505] flex items-center justify-center rotate-45" :class="getHitColor(selectedDossier.stats?.headshots || 0, 30)">
              <span class="text-xs font-mono font-black -rotate-45">{{ selectedDossier.stats?.headshots || 0 }}%</span>
            </div>
            
            <div class="flex gap-1 mt-4">
              <div class="w-6 h-32 border-2 bg-[#050505] clip-esports-small" :class="getHitColor(selectedDossier.stats?.arms || 0, 20)"></div>
              <div class="w-24 h-40 border-2 bg-[#050505] flex items-center justify-center clip-esports-small" :class="getHitColor(selectedDossier.stats?.torso || 0, 40)">
                <span class="text-xs font-mono font-black">{{ selectedDossier.stats?.torso || 0 }}%</span>
              </div>
              <div class="w-6 h-32 border-2 bg-[#050505] clip-esports-small" :class="getHitColor(selectedDossier.stats?.arms || 0, 20)"></div>
            </div>
            
            <div class="flex gap-2">
              <div class="w-10 h-36 border-2 bg-[#050505] clip-esports-small" :class="getHitColor(selectedDossier.stats?.legs || 0, 15)"></div>
              <div class="w-10 h-36 border-2 bg-[#050505] clip-esports-small" :class="getHitColor(selectedDossier.stats?.legs || 0, 15)"></div>
            </div>
          </div>
        </div>

        <div class="w-full md:w-3/5 p-10 flex flex-col z-10 bg-[#050505]">
          <div class="mb-10">
            <span class="px-4 py-1.5 bg-[#0a0a0c] border border-zinc-800 text-[9px] font-black uppercase tracking-[0.3em] text-zinc-400 clip-esports-small">Dossiê Confidencial</span>
            <h1 class="text-5xl font-black text-white tracking-tighter uppercase italic mt-4 mb-1">{{ selectedDossier.player?.nickname || 'Unknown' }}</h1>
            <p class="text-xs font-mono text-zinc-500">ID_REGISTRO: {{ selectedDossier.player?.fivem_id }}</p>
          </div>

          <div class="grid grid-cols-2 gap-4 mb-8">
            <div class="bg-[#0a0a0c] border border-zinc-900 p-5 flex flex-col justify-between clip-esports-small">
              <span class="text-[9px] font-bold text-zinc-500 uppercase tracking-[0.2em] mb-2">K/D Ratio Global</span>
              <span class="text-4xl font-mono font-black text-white">{{ (selectedDossier.stats?.kd || 0).toFixed(2) }}</span>
            </div>
            <div class="bg-[#0a0a0c] border border-zinc-900 p-5 flex flex-col justify-between clip-esports-small">
              <span class="text-[9px] font-bold text-zinc-500 uppercase tracking-[0.2em] mb-2">Precisão (Accuracy)</span>
              <span class="text-4xl font-mono font-black text-white">{{ selectedDossier.stats?.accuracy || 0 }}%</span>
            </div>
            <div class="bg-[#050505] p-6 border border-zinc-800 flex flex-col justify-between col-span-2 clip-esports relative overflow-hidden">
              <div class="absolute top-0 left-0 w-1 h-full" :class="selectedDossier.player?.suspicion_score >= 80 ? 'bg-rose-600' : 'bg-emerald-600'"></div>
              <div class="flex justify-between items-center mb-2 pl-2">
                <span class="text-[9px] font-bold text-zinc-400 uppercase tracking-[0.2em]">Nível de Ameaça Detectado</span>
                <span class="material-symbols-rounded" :class="selectedDossier.player?.suspicion_score >= 80 ? 'text-rose-500 animate-pulse' : 'text-emerald-500'">policy</span>
              </div>
              <div class="flex items-end gap-3 pl-2">
                <span class="text-5xl font-mono font-black leading-none tracking-tighter" :class="selectedDossier.player?.suspicion_score >= 80 ? 'text-rose-600 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)]' : 'text-emerald-500'">{{ selectedDossier.player?.suspicion_score.toFixed(1) || 0 }}</span>
                <span class="text-sm font-black text-zinc-600 uppercase pb-1">/ 100</span>
              </div>
            </div>
          </div>
          
          <div class="mt-auto pt-6 border-t border-zinc-900 flex justify-end">
             <button @click="closeDossier" class="px-10 py-4 bg-zinc-900 text-zinc-400 text-[10px] font-black uppercase tracking-[0.2em] hover:bg-white hover:text-black transition-colors clip-esports-small">
               Encerrar Relatório
             </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const suspects = ref([])
const isProcessing = ref(false)
const selectedPlayer = ref(null)
const injectAmount = ref(null)

const showDossier = ref(false)
const selectedDossier = ref(null)

const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001'
const baseUrl = rawUrl.replace(/\/$/, '')

const fetchSuspects = async () => {
  isProcessing.value = true
  try {
    const res = await fetch(`${baseUrl}/api/admin/suspects`)
    if (res.ok) suspects.value = await res.json()
  } catch (error) {
    toastStore.showToast('Erro de Conexão', 'Falha ao comunicar com a central.', 'error')
  } finally {
    isProcessing.value = false
  }
}

const seedMocks = async () => {
  isProcessing.value = true
  try {
    const res = await fetch(`${baseUrl}/api/admin/seed_mocks`, { method: 'POST' })
    if (res.ok) {
      toastStore.showToast('Simulação', 'Anomalias injetadas na rede.', 'warning')
      await fetchSuspects()
    }
  } finally {
    isProcessing.value = false
  }
}

const clearMocks = async () => {
  isProcessing.value = true
  try {
    const res = await fetch(`${baseUrl}/api/admin/clear_mocks`, { method: 'DELETE' })
    if (res.ok) {
      toastStore.showToast('Expurgo Concluído', 'Registros apagados.', 'success')
      await fetchSuspects()
    }
  } finally {
    isProcessing.value = false
  }
}

const openInjectModal = (player) => {
  selectedPlayer.value = player
  injectAmount.value = null
}

const confirmInjection = async () => {
  if (!selectedPlayer.value || !injectAmount.value) return
  isProcessing.value = true
  try {
    const res = await fetch(`${baseUrl}/api/admin/inject_coins`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_fivem_id: selectedPlayer.value.fivem_id, amount: Number(injectAmount.value) })
    })
    if (res.ok) {
      toastStore.showToast('Transferência Executada', `C$ ${injectAmount.value} injetados.`, 'success')
      selectedPlayer.value = null
      await fetchSuspects()
    }
  } finally {
    isProcessing.value = false
  }
}

const toggleQuarantine = async (player) => {
  toastStore.showToast('Protocolo de Segurança', `Comando enviado para ${player.nickname}.`, 'warning')
  player.is_quarantined = !player.is_quarantined
}

const viewDossier = async (playerId) => {
  isProcessing.value = true
  try {
    const res = await fetch(`${baseUrl}/api/admin/player/${playerId}/dossier`)
    if (res.ok) {
      selectedDossier.value = await res.json()
      showDossier.value = true
    } else {
      toastStore.showToast('Acesso Negado', 'Dossiê não encontrado.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Erro de Rede', 'Falha ao obter dossiê.', 'error')
  } finally {
    isProcessing.value = false
  }
}

const closeDossier = () => {
  showDossier.value = false
  selectedDossier.value = null
}

const handleLogout = () => {
  localStorage.removeItem('admin_token')
  window.location.href = '/login'
}

const criticalCount = computed(() => suspects.value.filter(s => s.suspicion_score >= 80).length)
const averageScore = computed(() => {
  if (suspects.value.length === 0) return 0
  const total = suspects.value.reduce((acc, curr) => acc + curr.suspicion_score, 0)
  return total / suspects.value.length
})

const getScoreColor = (score) => {
  if (score >= 80) return 'text-rose-600 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)]'
  if (score >= 50) return 'text-yellow-500'
  return 'text-emerald-500'
}

const getScoreBg = (score) => {
  if (score >= 80) return 'bg-rose-600 shadow-[0_0_15px_rgba(225,29,72,0.5)]'
  if (score >= 50) return 'bg-yellow-500 shadow-[0_0_15px_rgba(234,179,8,0.5)]'
  return 'bg-emerald-600'
}

const getScoreGradient = (score) => {
  if (score >= 80) return 'from-rose-600'
  if (score >= 50) return 'from-yellow-500'
  return 'from-emerald-600'
}

const getHitColor = (val, threshold) => {
  if (val > threshold) return 'border-rose-600 text-rose-500 shadow-[0_0_15px_rgba(225,29,72,0.3)]'
  if (val > threshold / 2) return 'border-yellow-600 text-yellow-500'
  return 'border-zinc-800 text-zinc-600'
}

onMounted(() => {
  fetchSuspects()
})
</script>

<style scoped>
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #27272a; }
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }
.clip-modal { clip-path: polygon(30px 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%, 0 30px); }
</style>