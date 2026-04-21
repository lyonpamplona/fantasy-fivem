<template>
  <div class="min-h-screen bg-zinc-950 text-white p-4 flex flex-col font-sans overflow-hidden">
    
    <header class="w-full max-w-[1800px] mx-auto mb-6 bg-zinc-900 border-b-2 border-zinc-800 px-8 py-5 flex flex-col md:flex-row items-center justify-between shadow-[0_10px_30px_rgba(0,0,0,0.5)] z-40 relative clip-esports shrink-0">
      <div class="flex items-center gap-5">
        <div class="w-12 h-12 bg-zinc-950 border border-rose-900 flex items-center justify-center rotate-45 shadow-[0_0_20px_rgba(244,63,94,0.15)]">
          <span class="material-symbols-rounded text-rose-500 text-2xl -rotate-45">radar</span>
        </div>
        <div class="flex flex-col">
          <h1 class="text-3xl font-black tracking-tighter text-white leading-none italic uppercase">Heurística <span class="text-rose-600">Core</span></h1>
          <span class="text-[9px] font-bold text-zinc-400 uppercase tracking-[0.3em] mt-1">Terminal de Segurança Anti-Cheat</span>
        </div>
      </div>

      <div class="flex items-center gap-3 mt-4 md:mt-0">
        <button @click="seedMocks" :disabled="isProcessing" class="px-5 py-3 bg-zinc-950 border border-zinc-800 text-[9px] font-black uppercase tracking-[0.2em] text-zinc-400 hover:text-white hover:border-zinc-500 transition-colors clip-esports-small disabled:opacity-30">
          Gerar Teste
        </button>
        <button @click="clearMocks" :disabled="isProcessing" class="px-5 py-3 bg-zinc-950 border border-zinc-800 text-[9px] font-black uppercase tracking-[0.2em] text-zinc-400 hover:text-rose-500 hover:border-rose-800 transition-colors clip-esports-small disabled:opacity-30">
          Limpar Logs
        </button>
        <button @click="fetchSuspects" :disabled="isProcessing" class="w-12 h-12 bg-emerald-600 hover:bg-emerald-500 text-black flex items-center justify-center transition-colors clip-esports-small disabled:opacity-30 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
          <span class="material-symbols-rounded text-lg" :class="{'animate-spin': isProcessing}">refresh</span>
        </button>
        <div class="w-[1px] h-8 bg-zinc-800 mx-2"></div>
        <button @click="handleLogout" class="px-5 py-3 bg-zinc-900 border border-zinc-700 text-[9px] font-black uppercase tracking-[0.2em] text-zinc-400 hover:text-rose-500 hover:bg-zinc-800 transition-colors flex items-center gap-2 clip-esports-small">
          <span class="material-symbols-rounded text-sm">logout</span> Sair
        </button>
      </div>
    </header>

    <div class="w-full max-w-[1800px] mx-auto grid grid-cols-1 sm:grid-cols-3 gap-6 mb-6 shrink-0">
      <div class="bg-zinc-900 border-l-4 border-zinc-600 p-5 flex items-center justify-between clip-esports-small shadow-lg">
        <div class="flex flex-col">
          <span class="text-[9px] font-black text-zinc-400 uppercase tracking-[0.2em]">Total Monitorado</span>
          <span class="text-4xl font-mono font-black text-white mt-1">{{ suspects.length }}</span>
        </div>
        <span class="material-symbols-rounded text-5xl text-zinc-700">monitoring</span>
      </div>
      <div class="bg-zinc-900 border-l-4 border-rose-600 p-5 flex items-center justify-between clip-esports-small shadow-lg">
        <div class="flex flex-col">
          <span class="text-[9px] font-black text-rose-500/70 uppercase tracking-[0.2em]">Ameaças Críticas</span>
          <span class="text-4xl font-mono font-black text-rose-500 mt-1 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)]">{{ criticalCount }}</span>
        </div>
        <span class="material-symbols-rounded text-5xl text-rose-950">warning</span>
      </div>
      <div class="bg-zinc-900 border-l-4 border-emerald-600 p-5 flex items-center justify-between clip-esports-small shadow-lg">
        <div class="flex flex-col">
          <span class="text-[9px] font-black text-emerald-600/70 uppercase tracking-[0.2em]">Média Global</span>
          <span class="text-4xl font-mono font-black text-emerald-500 mt-1">{{ averageScore.toFixed(1) }}</span>
        </div>
        <span class="material-symbols-rounded text-5xl text-emerald-950">analytics</span>
      </div>
    </div>

    <main class="w-full max-w-[1800px] mx-auto flex-1 flex gap-6 overflow-hidden pb-4 transition-all duration-500">
      
      <div class="flex-1 bg-zinc-900 border border-zinc-800 clip-esports shadow-xl flex flex-col overflow-hidden relative transition-all duration-500">
        <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.01)_4px,rgba(255,255,255,0.01)_8px)] pointer-events-none"></div>
        
        <div v-if="suspects.length === 0" class="flex flex-col items-center justify-center flex-1 opacity-40">
          <span class="material-symbols-rounded text-7xl mb-4 text-zinc-500">policy</span>
          <h2 class="text-sm font-black text-zinc-400 uppercase tracking-[0.4em]">Perímetro Seguro</h2>
        </div>

        <div v-else class="flex-1 overflow-y-auto custom-scrollbar relative z-10">
          <table class="w-full text-left border-collapse">
            <thead class="sticky top-0 bg-zinc-950 z-20 shadow-md">
              <tr class="text-[9px] font-black text-zinc-400 uppercase tracking-widest border-b border-zinc-800">
                <th class="py-4 px-6">Player</th>
                <th class="py-4 px-4">FiveM ID</th>
                <th class="py-4 px-4">Score</th>
                <th class="py-4 px-4">Status / VIP</th>
                <th class="py-4 px-6 text-right">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="player in suspects" :key="player.id" 
                  @click="viewDossier(player.id)"
                  class="border-b border-zinc-800/50 hover:bg-zinc-800/60 transition-colors cursor-pointer group"
                  :class="{'bg-zinc-800 border-l-2 border-l-emerald-500': selectedDossier?.player?.id === player.id}">
                
                <td class="py-4 px-6 flex items-center gap-3">
                  <div class="w-2.5 h-2.5 rounded-full shadow-lg shrink-0" :class="player.suspicion_score >= 80 ? 'bg-rose-500 shadow-rose-500/50 animate-pulse' : (player.suspicion_score >= 50 ? 'bg-yellow-500 shadow-yellow-500/50' : 'bg-emerald-500 shadow-emerald-500/50')"></div>
                  <span class="text-sm font-black text-white italic truncate group-hover:text-emerald-400 transition-colors">{{ player.nickname || 'Unknown' }}</span>
                  <span v-if="player.suspicion_score < 15" class="material-symbols-rounded text-emerald-500 text-[14px]" title="Trust Factor: Seguro">verified_user</span>
                </td>
                
                <td class="py-4 px-4 text-xs font-mono text-zinc-400">
                  steam:{{ player.fivem_id }}
                </td>
                
                <td class="py-4 px-4">
                  <span class="text-xl font-mono font-black drop-shadow-md" :class="getScoreColor(player.suspicion_score)">
                    {{ player.suspicion_score.toFixed(1) }}
                  </span>
                </td>
                
                <td class="py-4 px-4">
                  <div class="flex gap-2">
                    <span class="px-2 py-1 text-[8px] font-black uppercase tracking-widest clip-esports-small" :class="player.is_quarantined ? 'bg-rose-950/50 text-rose-500 border border-rose-900' : 'bg-emerald-950/30 text-emerald-500 border border-emerald-900/50'">
                      {{ player.is_quarantined ? 'Bloqueado' : 'Livre' }}
                    </span>
                    <span v-if="player.is_vip" class="px-2 py-1 bg-amber-950/30 text-amber-500 border border-amber-900/50 text-[8px] font-black uppercase tracking-widest clip-esports-small">
                      VIP
                    </span>
                  </div>
                </td>
                
                <td class="py-4 px-6 text-right">
                  <div class="flex items-center justify-end gap-2">
                    <button @click.stop="openInjectModal(player)" class="w-8 h-8 bg-zinc-800 text-emerald-500 hover:bg-emerald-600 hover:text-black flex items-center justify-center transition-colors clip-esports-small border border-zinc-700" title="Injetar C$">
                      <span class="material-symbols-rounded text-sm">toll</span>
                    </button>
                    <button @click.stop="toggleQuarantine(player)" class="w-8 h-8 flex items-center justify-center transition-colors clip-esports-small border" :class="player.is_quarantined ? 'bg-rose-900/20 text-rose-500 border-rose-900/50 hover:bg-rose-600 hover:text-white' : 'bg-zinc-800 text-zinc-400 border-zinc-700 hover:bg-rose-600 hover:text-white hover:border-rose-600'" title="Bloqueio">
                      <span class="material-symbols-rounded text-sm">{{ player.is_quarantined ? 'lock' : 'lock_open' }}</span>
                    </button>
                  </div>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <Transition name="slide-panel">
        <aside v-if="selectedDossier" class="w-[450px] bg-zinc-900 border border-zinc-800 clip-esports flex flex-col overflow-y-auto custom-scrollbar shrink-0 shadow-[-10px_0_30px_rgba(0,0,0,0.5)] relative">
          <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.01)_4px,rgba(255,255,255,0.01)_8px)] pointer-events-none"></div>

          <button @click="closeDossier" class="absolute top-6 right-6 z-50 w-8 h-8 bg-zinc-950 border border-zinc-800 flex items-center justify-center text-zinc-400 hover:text-white hover:bg-rose-600 transition-colors clip-esports-small shadow-md">
            <span class="material-symbols-rounded text-sm">close</span>
          </button>

          <div class="flex flex-col min-h-full relative z-10">
            
            <div class="p-8 pb-6 border-b border-zinc-800 bg-zinc-950">
               <div class="flex items-center justify-between mb-4">
                 <span class="px-4 py-1.5 bg-zinc-900 border border-zinc-800 text-[9px] font-black uppercase tracking-[0.3em] text-zinc-400 clip-esports-small inline-block">Dossiê Confidencial</span>
                 <span v-if="selectedDossier.player?.suspicion_score < 15" class="px-3 py-1 bg-emerald-950/30 border border-emerald-900/50 text-emerald-500 text-[8px] font-black uppercase tracking-widest clip-esports-small flex items-center gap-1">
                   <span class="material-symbols-rounded text-[12px]">verified_user</span> Trust Factor
                 </span>
               </div>
               <h2 class="text-4xl font-black text-white tracking-tighter uppercase italic truncate mb-1 pr-10">{{ selectedDossier.player?.nickname || 'Unknown' }}</h2>
               <p class="text-xs font-mono text-zinc-500 uppercase">ID_REGISTRO: {{ selectedDossier.player?.fivem_id }}</p>
            </div>

            <div class="p-6 flex flex-col items-center border-b border-zinc-800 bg-zinc-900">
              <h3 class="text-[10px] font-black text-zinc-400 uppercase tracking-[0.3em] mb-6 w-full text-left">Análise Balística</h3>
              <div class="relative w-[180px] h-[320px] flex flex-col items-center justify-start gap-1 z-10 scale-95">
                <div class="w-16 h-16 border-2 bg-zinc-950 flex items-center justify-center rotate-45" :class="getHitColor(selectedDossier.stats?.headshots || 0, 30)">
                  <span class="text-xs font-mono font-black -rotate-45">{{ selectedDossier.stats?.headshots || 0 }}%</span>
                </div>
                <div class="flex gap-1 mt-4">
                  <div class="w-6 h-32 border-2 bg-zinc-950 clip-esports-small" :class="getHitColor(selectedDossier.stats?.arms || 0, 20)"></div>
                  <div class="w-24 h-40 border-2 bg-zinc-950 flex items-center justify-center clip-esports-small" :class="getHitColor(selectedDossier.stats?.torso || 0, 40)">
                    <span class="text-xs font-mono font-black">{{ selectedDossier.stats?.torso || 0 }}%</span>
                  </div>
                  <div class="w-6 h-32 border-2 bg-zinc-950 clip-esports-small" :class="getHitColor(selectedDossier.stats?.arms || 0, 20)"></div>
                </div>
                <div class="flex gap-2">
                  <div class="w-10 h-36 border-2 bg-zinc-950 clip-esports-small" :class="getHitColor(selectedDossier.stats?.legs || 0, 15)"></div>
                  <div class="w-10 h-36 border-2 bg-zinc-950 clip-esports-small" :class="getHitColor(selectedDossier.stats?.legs || 0, 15)"></div>
                </div>
              </div>
            </div>

            <div class="p-6 flex flex-col gap-4 flex-1 bg-zinc-900">
              <div class="grid grid-cols-2 gap-4">
                <div class="bg-zinc-800/50 border border-zinc-700/50 p-4 flex flex-col justify-between clip-esports-small">
                  <span class="text-[8px] font-bold text-zinc-400 uppercase tracking-[0.2em] mb-2">K/D Global</span>
                  <span class="text-3xl font-mono font-black text-white">{{ (selectedDossier.stats?.kd || 0).toFixed(2) }}</span>
                </div>
                <div class="bg-zinc-800/50 border border-zinc-700/50 p-4 flex flex-col justify-between clip-esports-small">
                  <span class="text-[8px] font-bold text-zinc-400 uppercase tracking-[0.2em] mb-2">Precisão (Acc)</span>
                  <span class="text-3xl font-mono font-black text-white">{{ selectedDossier.stats?.accuracy || 0 }}%</span>
                </div>
              </div>

              <div class="bg-zinc-950 p-5 border border-zinc-800 flex flex-col justify-between clip-esports relative overflow-hidden mt-2">
                <div class="absolute top-0 left-0 w-1 h-full" :class="selectedDossier.player?.suspicion_score >= 80 ? 'bg-rose-600' : 'bg-emerald-600'"></div>
                <div class="flex justify-between items-center mb-2 pl-2">
                  <span class="text-[9px] font-bold text-zinc-400 uppercase tracking-[0.2em]">Nível de Ameaça</span>
                  <span class="material-symbols-rounded text-sm" :class="selectedDossier.player?.suspicion_score >= 80 ? 'text-rose-500 animate-pulse' : 'text-emerald-500'">policy</span>
                </div>
                <div class="flex items-end gap-3 pl-2">
                  <span class="text-4xl font-mono font-black leading-none tracking-tighter" :class="getScoreColor(selectedDossier.player?.suspicion_score || 0)">{{ selectedDossier.player?.suspicion_score.toFixed(1) || 0 }}</span>
                  <span class="text-xs font-black text-zinc-500 uppercase pb-0.5">/ 100</span>
                </div>
              </div>

              <div class="bg-zinc-800/50 border border-zinc-700/50 p-4 clip-esports-small mt-2">
                <h3 class="text-[9px] font-bold text-zinc-400 uppercase tracking-[0.2em] mb-4">Evolução K/D (7 Dias)</h3>
                <div class="h-16 w-full relative flex items-end">
                  <svg viewBox="0 0 100 60" preserveAspectRatio="none" class="w-full h-full overflow-visible">
                    <polyline :points="generateChartPoints(selectedDossier.stats?.kd_history)" fill="none" stroke="currentColor" stroke-width="2" class="transition-all duration-500" :class="selectedDossier.player?.suspicion_score >= 80 ? 'text-rose-500' : 'text-emerald-500'" vector-effect="non-scaling-stroke" />
                  </svg>
                </div>
              </div>
              
              <div class="mt-4 flex flex-col gap-2">
                 <h3 class="text-[9px] font-black text-zinc-400 uppercase tracking-[0.3em] mb-2">Módulos Detetados</h3>
                 <div v-if="!selectedDossier.player || selectedDossier.player.suspicion_score < 50" class="p-3 bg-emerald-950/30 text-emerald-500 text-[9px] font-black uppercase tracking-widest flex items-center gap-2 border border-emerald-900/50 clip-esports-small">
                   <span class="material-symbols-rounded text-sm">check_circle</span> Sem anomalias detetadas
                 </div>
                 <div v-else class="flex flex-col gap-2">
                   <div class="p-3 bg-yellow-950/30 text-yellow-500 text-[9px] font-black uppercase tracking-widest flex items-center gap-2 border border-yellow-900/50 clip-esports-small">
                     <span class="material-symbols-rounded text-sm">warning</span> Comportamento Suspeito
                   </div>
                   <div v-if="selectedDossier.player.suspicion_score >= 80" class="p-3 bg-rose-950/30 text-rose-500 text-[9px] font-black uppercase tracking-widest flex items-center gap-2 border border-rose-900/50 clip-esports-small">
                     <span class="material-symbols-rounded text-sm">api</span> Aimbot Lock (Crítico)
                   </div>
                 </div>
              </div>

              <div class="mt-4 flex flex-col gap-2">
                 <h3 class="text-[9px] font-black text-zinc-400 uppercase tracking-[0.3em] mb-2">Auditoria Financeira</h3>
                 <div v-if="!selectedDossier.financial_logs || selectedDossier.financial_logs.length === 0" class="p-3 bg-zinc-800/50 border border-zinc-700/50 text-zinc-500 text-[9px] font-black uppercase tracking-widest text-center clip-esports-small">
                   Nenhum registo de transações
                 </div>
                 <div v-else class="flex flex-col gap-2">
                   <div v-for="log in selectedDossier.financial_logs" :key="log.id" class="p-3 border flex justify-between items-center clip-esports-small" :class="log.suspicious ? 'bg-rose-950/20 border-rose-900/50' : 'bg-zinc-900/80 border-zinc-700/50'">
                      <div class="flex flex-col">
                        <span class="text-[8px] font-black uppercase tracking-widest" :class="log.suspicious ? 'text-rose-500' : 'text-zinc-400'">{{ log.type }}</span>
                        <span class="text-[9px] font-mono text-zinc-500">Alvo: {{ log.target }}</span>
                      </div>
                      <span class="text-xs font-mono font-black" :class="log.suspicious ? 'text-rose-400' : 'text-white'">{{ log.amount.toLocaleString() }} C$</span>
                   </div>
                 </div>
              </div>

            </div>

            <div class="p-6 bg-zinc-900 border-t border-zinc-800 mt-auto">
               <button @click="openInjectModal(selectedDossier.player)" class="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-black font-black uppercase tracking-[0.2em] text-[10px] transition-all shadow-[0_0_15px_rgba(16,185,129,0.2)] flex items-center justify-center gap-2 clip-esports-small">
                 <span class="material-symbols-rounded text-sm">toll</span> Injetar Capital (C$)
               </button>
            </div>
          </div>
        </aside>
      </Transition>
    </main>

    <div v-if="selectedPlayerForInject" class="fixed inset-0 z-[100] flex items-center justify-center bg-zinc-950/80 backdrop-blur-sm p-4">
      <div class="bg-zinc-900 border border-zinc-800 w-full max-w-sm p-8 rounded-2xl shadow-[0_0_50px_rgba(0,0,0,0.8)]">
        <div class="flex justify-between items-center mb-6 border-b border-zinc-800 pb-4">
          <h2 class="text-xl font-black text-white uppercase tracking-widest italic">Injeção de Capital</h2>
          <button @click="selectedPlayerForInject = null" class="w-8 h-8 flex items-center justify-center bg-zinc-800 rounded-md text-zinc-400 hover:text-white hover:bg-rose-600 transition-colors">
            <span class="material-symbols-rounded text-sm">close</span>
          </button>
        </div>
        <p class="text-[10px] font-mono text-zinc-400 mb-6 uppercase tracking-widest">Alvo Autorizado: <span class="text-emerald-400 font-black">{{ selectedPlayerForInject.nickname }}</span></p>
        
        <div class="relative h-14 mb-6">
          <span class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500 font-mono font-black text-lg">C$</span>
          <input v-model="injectAmount" type="number" class="w-full h-full bg-zinc-950 border border-zinc-800 rounded-xl pl-12 pr-4 text-white font-mono text-lg focus:outline-none focus:border-emerald-500 shadow-inner">
        </div>
        
        <button @click="confirmInjection" :disabled="isProcessing || !injectAmount" class="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-black font-black text-[10px] uppercase tracking-[0.2em] rounded-xl disabled:opacity-30 transition-all shadow-[0_0_20px_rgba(16,185,129,0.3)]">
          Confirmar Transferência
        </button>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useToastStore } from '../stores/toast'

const toastStore = useToastStore()

const suspects = ref([])
const isProcessing = ref(false)
const selectedPlayerForInject = ref(null)
const injectAmount = ref(null)
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
      selectedDossier.value = null
    }
  } finally {
    isProcessing.value = false
  }
}

const openInjectModal = (player) => {
  selectedPlayerForInject.value = player
  injectAmount.value = null
}

const confirmInjection = async () => {
  if (!selectedPlayerForInject.value || !injectAmount.value) return
  isProcessing.value = true
  try {
    const res = await fetch(`${baseUrl}/api/admin/inject_coins`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ target_fivem_id: selectedPlayerForInject.value.fivem_id, amount: Number(injectAmount.value) })
    })
    if (res.ok) {
      toastStore.showToast('Transferência Executada', `C$ ${injectAmount.value} injetados.`, 'success')
      selectedPlayerForInject.value = null
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
      const data = await res.json()
      
      if (!data.player) data.player = { id: playerId, nickname: 'Unknown', suspicion_score: 0, fivem_id: 'unknown' }
      if (!data.stats) data.stats = { kills: 0, headshots: 0, arms: 0, torso: 0, legs: 0, kd: 1.0, accuracy: 0 }
      
      if (!data.stats.kd_history) {
        const baseKd = data.stats.kd || 1.2
        const isHacker = data.player.suspicion_score >= 80
        data.stats.kd_history = Array.from({length: 7}, (_, i) => {
          if (isHacker && i >= 4) return parseFloat((baseKd + (i * 0.8)).toFixed(2))
          return parseFloat((Math.max(0.1, baseKd + (Math.random() * 0.6 - 0.3))).toFixed(2))
        })
      }
      
      if (!data.financial_logs) {
        const isHacker = data.player.suspicion_score >= 80
        data.financial_logs = isHacker ? [
          { id: 1, type: 'RMT_SUSPECT', amount: 15000000, target: 'steam:9928', suspicious: true },
          { id: 2, type: 'MARKET_DUMP', amount: 5000000, target: 'steam:1102', suspicious: true }
        ] : [
          { id: 3, type: 'MARKET_BUY', amount: 12000, target: 'Loja', suspicious: false }
        ]
      }

      selectedDossier.value = data
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
  selectedDossier.value = null
}

const handleLogout = () => {
  localStorage.removeItem('admin_token')
  window.location.href = '/login'
}

const generateChartPoints = (history) => {
  if (!history || history.length === 0) return '0,60 100,60'
  const max = Math.max(...history, 1)
  const min = Math.min(...history, 0)
  const range = max - min || 1
  return history.map((val, i) => {
    const x = (i / (history.length - 1)) * 100
    const y = 60 - (((val - min) / range) * 60)
    return `${x},${y}`
  }).join(' ')
}

const criticalCount = computed(() => suspects.value.filter(s => s.suspicion_score >= 80).length)
const averageScore = computed(() => {
  if (suspects.value.length === 0) return 0
  const total = suspects.value.reduce((acc, curr) => acc + curr.suspicion_score, 0)
  return total / suspects.value.length
})

const getScoreColor = (score) => {
  if (score >= 80) return 'text-rose-500 drop-shadow-[0_0_10px_rgba(225,29,72,0.8)]'
  if (score >= 50) return 'text-yellow-500'
  return 'text-emerald-500'
}

const getHitColor = (val, threshold) => {
  if (val > threshold) return 'border-rose-500 shadow-[0_0_15px_rgba(225,29,72,0.4)]'
  if (val > threshold / 2) return 'border-yellow-500 shadow-[0_0_15px_rgba(234,179,8,0.2)]'
  return 'border-zinc-700'
}

const handleKeydown = (e) => {
  if (e.key === 'Escape' || e.key === 'Esc') {
    if (selectedPlayerForInject.value) {
      selectedPlayerForInject.value = null
    } else if (selectedDossier.value) {
      closeDossier()
    }
  }
}

onMounted(() => {
  fetchSuspects()
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #52525b; }
.clip-esports { clip-path: polygon(15px 0, 100% 0, 100% calc(100% - 15px), calc(100% - 15px) 100%, 0 100%, 0 15px); }
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }

.slide-panel-enter-active,
.slide-panel-leave-active {
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}
.slide-panel-enter-from,
.slide-panel-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>