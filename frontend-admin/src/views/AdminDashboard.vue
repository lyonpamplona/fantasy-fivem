<template>
  <div class="h-full p-6 md:p-10 relative">
    <div class="max-w-[1600px] mx-auto h-full flex flex-col">
      
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between mb-8 pb-6 border-b border-white/10 gap-6">
        <div>
          <div class="flex items-center gap-3 mb-1">
            <span class="material-symbols-rounded text-rose-500 text-4xl bg-rose-500/10 p-2 rounded-xl border border-rose-500/20">admin_panel_settings</span>
            <h1 class="text-4xl font-black text-white tracking-tighter uppercase">Centro de Comando</h1>
          </div>
        </div>
        
        <div class="flex flex-wrap items-center gap-3">
          <button @click="emulateData" :disabled="isWorking" class="bg-amber-500/10 text-amber-500 border border-amber-500/30 hover:bg-amber-500/20 px-5 py-2.5 rounded-xl flex items-center gap-2 transition-all font-bold text-xs uppercase tracking-widest disabled:opacity-50">
            <span class="material-symbols-rounded text-base" :class="{'animate-spin': isWorking && loadingType === 'emulate'}">bug_report</span>
            Emular Teste
          </button>

          <button @click="injectCoins" :disabled="isWorking" class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/20 px-5 py-2.5 rounded-xl flex items-center gap-2 transition-all font-bold text-xs uppercase tracking-widest disabled:opacity-50">
            <span class="material-symbols-rounded text-base" :class="{'animate-spin': isWorking && loadingType === 'coins'}">payments</span>
            Injetar Coins
          </button>

          <button @click="clearMocks" :disabled="isWorking" class="bg-rose-500/10 text-rose-400 border border-rose-500/30 hover:bg-rose-500/20 px-5 py-2.5 rounded-xl flex items-center gap-2 transition-all font-bold text-xs uppercase tracking-widest disabled:opacity-50">
            <span class="material-symbols-rounded text-base" :class="{'animate-spin': isWorking && loadingType === 'clear'}">delete_sweep</span>
            Limpar Logs
          </button>
          
          <button @click="logout" class="bg-white/5 hover:bg-rose-500/20 hover:text-rose-400 hover:border-rose-500/30 text-white border border-white/10 px-5 py-2.5 rounded-xl flex items-center gap-2 transition-all font-bold text-xs uppercase tracking-widest ml-2">
            <span class="material-symbols-rounded text-base">logout</span>
            Sair
          </button>
        </div>
      </div>

      <div class="bg-slate-900/60 rounded-[30px] border border-white/10 shadow-2xl overflow-hidden backdrop-blur-2xl flex-1 flex flex-col">
        <div class="overflow-x-auto flex-1">
          <table class="w-full text-left border-collapse min-w-[900px]">
            <thead class="bg-black/40 border-b border-white/10">
              <tr class="text-[10px] uppercase tracking-widest text-slate-500">
                <th class="p-6 font-black">Player</th>
                <th class="p-6 font-black">FiveM ID</th>
                <th class="p-6 font-black text-center">Estatísticas (K/HS)</th>
                <th class="p-6 font-black text-center">Eficiência (HS%)</th>
                <th class="p-6 font-black text-center">Alerta Heurístico</th>
                <th class="p-6 font-black text-center">Ações</th>
              </tr>
            </thead>
            
            <tbody class="text-sm text-slate-300">
              <tr v-if="loading && suspects.length === 0">
                <td colspan="6" class="p-16 text-center text-slate-500 font-bold uppercase tracking-widest animate-pulse">Coletando telemetria do servidor...</td>
              </tr>
              <tr v-else-if="suspects.length === 0">
                <td colspan="6" class="p-16 text-center text-slate-500 flex flex-col items-center justify-center">
                   <span class="material-symbols-rounded text-4xl mb-3 opacity-50">verified_user</span>
                   <span class="font-bold uppercase tracking-widest">Nenhuma anomalia detectada.</span>
                </td>
              </tr>
              <tr v-else v-for="player in suspects" :key="player.id" class="border-b border-white/5 hover:bg-white/5 transition-colors cursor-pointer" @click="openDossier(player)">
                <td class="p-6 font-black text-white flex items-center gap-3">
                  <div class="w-2.5 h-2.5 rounded-full" :class="player.suspicion_score > 70 ? 'bg-rose-500 shadow-[0_0_10px_#f43f5e] animate-pulse' : (player.suspicion_score > 30 ? 'bg-amber-400' : 'bg-emerald-500')"></div>
                  {{ player.nickname }}
                  <span v-if="player.is_quarantined" class="bg-rose-500/10 text-rose-400 text-[9px] px-2 py-1 rounded uppercase tracking-widest ml-2 border border-rose-500/20">Isolado</span>
                </td>
                <td class="p-6 font-mono text-xs text-slate-500">{{ player.fivem_id }}</td>
                <td class="p-6 text-center font-bold">
                  <span class="text-white">{{ player.kills }}</span> <span class="text-slate-600 mx-1">/</span> <span class="text-emerald-400">{{ player.headshots }}</span>
                </td>
                <td class="p-6">
                  <div class="flex items-center justify-center gap-3">
                    <div class="w-24 bg-black/60 rounded-full h-1.5 overflow-hidden border border-white/5">
                      <div class="h-full transition-all duration-500" :class="player.hs_rate > 60 ? 'bg-rose-500' : 'bg-slate-400'" :style="{ width: player.hs_rate + '%' }"></div>
                    </div>
                    <span class="text-xs font-black w-12 text-right" :class="player.hs_rate > 60 ? 'text-rose-400' : 'text-slate-400'">{{ player.hs_rate }}%</span>
                  </div>
                </td>
                <td class="p-6 text-center">
                  <span class="text-2xl font-black drop-shadow-lg" :class="player.suspicion_score > 70 ? 'text-rose-500' : 'text-white'">
                    {{ player.suspicion_score }}
                  </span>
                </td>
                <td class="p-6 text-center">
                  <button @click.stop="toggleQuarantine(player.id)" class="w-10 h-10 rounded-xl bg-white/5 hover:bg-white/10 transition-all border border-white/10 flex items-center justify-center mx-auto">
                    <span class="material-symbols-rounded text-sm" :class="player.is_quarantined ? 'text-emerald-400' : 'text-rose-500'">
                      {{ player.is_quarantined ? 'lock_open' : 'lock' }}
                    </span>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <Transition name="slide-right">
      <div v-if="dossierData" class="fixed inset-y-0 right-0 w-full md:w-[480px] bg-slate-900 border-l border-white/10 shadow-[0_0_100px_rgba(0,0,0,0.8)] z-50 flex flex-col">
        <div class="p-8 border-b border-white/10 flex items-center justify-between bg-black/40 backdrop-blur-xl relative">
          <div class="absolute inset-0 bg-gradient-to-r from-rose-500/10 to-transparent opacity-50"></div>
          <div class="flex items-center gap-4 relative z-10">
            <div class="w-12 h-12 bg-rose-500/20 rounded-xl flex items-center justify-center border border-rose-500/30">
               <span class="material-symbols-rounded text-rose-500 text-2xl">policy</span>
            </div>
            <div>
              <h2 class="text-lg font-black text-white uppercase tracking-widest">Dossiê Analítico</h2>
              <p class="text-xs text-slate-400 font-mono mt-0.5">{{ dossierData.fivem_id }}</p>
            </div>
          </div>
          <button @click="dossierData = null" class="w-10 h-10 bg-white/5 rounded-full flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition-all relative z-10 border border-white/5">
            <span class="material-symbols-rounded text-sm">close</span>
          </button>
        </div>

        <div class="p-8 overflow-y-auto flex-1 space-y-10 custom-scrollbar bg-slate-900/50">
          <div>
             <h3 class="text-4xl font-black text-white mb-2 uppercase tracking-tighter">{{ dossierData.nickname }}</h3>
             <div v-if="dossierData.suspicion_score > 60" class="flex items-center gap-2 bg-rose-500/10 border border-rose-500/20 px-3 py-1.5 rounded-lg w-max">
                <span class="material-symbols-rounded text-rose-500 text-sm">warning</span>
                <span class="text-[10px] font-black uppercase tracking-widest text-rose-400">Alerta Heurístico Ativo</span>
             </div>
          </div>

          <div class="grid grid-cols-2 gap-4">
             <div class="bg-black/40 border border-white/5 p-5 rounded-2xl text-center shadow-inner">
                <span class="material-symbols-rounded text-slate-600 mb-2">report</span>
                <p class="text-[9px] uppercase tracking-widest text-slate-500 font-black mb-1">Reports</p>
                <p class="text-3xl font-black text-white">{{ dossierData.reports }}</p>
             </div>
             <div class="bg-black/40 border border-white/5 p-5 rounded-2xl text-center shadow-inner">
                <span class="material-symbols-rounded text-slate-600 mb-2">straighten</span>
                <p class="text-[9px] uppercase tracking-widest text-slate-500 font-black mb-1">Dist. Média</p>
                <p class="text-3xl font-black text-rose-400">{{ dossierData.avg_shot_distance }}m</p>
             </div>
          </div>

          <div v-if="dossierData.favorite_weapons && dossierData.favorite_weapons.length > 0">
             <h4 class="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2">
               <span class="material-symbols-rounded text-sm">track_changes</span> Padrão de Armamento
             </h4>
             <div class="space-y-3">
                <div v-for="weapon in dossierData.favorite_weapons" :key="weapon.name" class="bg-white/5 p-4 rounded-xl border border-white/5">
                   <div class="flex justify-between text-xs font-bold text-white mb-3 uppercase tracking-wider">
                      <span>{{ weapon.name }}</span>
                      <span class="text-slate-400">{{ weapon.usage }}%</span>
                   </div>
                   <div class="w-full bg-black/60 rounded-full h-1.5 overflow-hidden">
                      <div class="h-full bg-slate-300" :style="{ width: weapon.usage + '%' }"></div>
                   </div>
                </div>
             </div>
          </div>

          <div v-if="dossierData.recent_flags && dossierData.recent_flags.length > 0">
             <h4 class="text-[10px] font-black uppercase tracking-widest text-slate-500 mb-4 flex items-center gap-2">
               <span class="material-symbols-rounded text-sm">radar</span> Detecções do Sistema
             </h4>
             <ul class="space-y-2">
                <li v-for="flag in dossierData.recent_flags" :key="flag" class="flex items-start gap-3 bg-rose-500/5 border border-rose-500/10 p-4 rounded-xl">
                   <span class="material-symbols-rounded text-rose-500 text-sm mt-0.5">crisis_alert</span>
                   <span class="text-xs text-rose-200 font-medium leading-relaxed">{{ flag }}</span>
                </li>
             </ul>
          </div>
        </div>
      </div>
    </Transition>
    <div v-if="dossierData" @click="dossierData = null" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToastStore } from '../stores/toast'

const API_URL = (import.meta.env.VITE_API_URL || window.location.origin).replace(/\/+$/, '')
const router = useRouter()
const toastStore = useToastStore()

const suspects = ref([])
const loading = ref(true)
const isWorking = ref(false)
const loadingType = ref('')
const dossierData = ref(null)

const getHeaders = () => ({
  'Authorization': `Bearer ${localStorage.getItem('admin_token')}`,
  'Content-Type': 'application/json'
})

const logout = () => {
  localStorage.removeItem('admin_token')
  router.push('/login')
}

const fetchSuspects = async () => {
  loading.value = true
  try {
    const res = await fetch(`${API_URL}/api/admin/suspects`, { headers: getHeaders() })
    if (res.ok) suspects.value = await res.json()
    else if (res.status === 401) logout()
  } catch (e) {
  } finally {
    loading.value = false
  }
}

const emulateData = async () => {
  if (isWorking.value) return
  isWorking.value = true; loadingType.value = 'emulate'
  try {
    const res = await fetch(`${API_URL}/api/admin/seed_mocks`, { method: 'POST', headers: getHeaders() })
    if (res.ok) {
      await fetchSuspects()
      toastStore.showToast('Sucesso', 'Cenários emulados com sucesso.', 'success')
    }
  } catch (e) {} finally { isWorking.value = false; loadingType.value = '' }
}

const injectCoins = async () => {
  if (isWorking.value) return
  isWorking.value = true; loadingType.value = 'coins'
  try {
    const res = await fetch(`${API_URL}/api/admin/inject_coins`, { method: 'POST', headers: getHeaders() })
    if (res.ok) {
      const data = await res.json()
      toastStore.showToast('Banco Central', `Coins injetadas em ${data.affected_players} contas.`, 'success')
    }
  } catch (e) {} finally { isWorking.value = false; loadingType.value = '' }
}

const clearMocks = async () => {
  if (isWorking.value) return
  isWorking.value = true; loadingType.value = 'clear'
  try {
    const res = await fetch(`${API_URL}/api/admin/clear_mocks`, { method: 'DELETE', headers: getHeaders() })
    if (res.ok) {
      await fetchSuspects()
      toastStore.showToast('Limpeza', 'Logs apagados com sucesso.', 'success')
    }
  } catch (e) {} finally { isWorking.value = false; loadingType.value = '' }
}

const toggleQuarantine = async (playerId) => {
  try {
    const res = await fetch(`${API_URL}/api/admin/toggle_quarantine/${playerId}`, { method: 'POST', headers: getHeaders() })
    if (res.ok) {
      const data = await res.json()
      const player = suspects.value.find(p => p.id === playerId)
      if (player) {
        player.is_quarantined = data.is_quarantined
        toastStore.showToast('Sistema', `Status de quarentena atualizado.`, 'warning')
      }
    }
  } catch (e) {}
}

const openDossier = async (player) => {
  try {
    const res = await fetch(`${API_URL}/api/admin/player/${player.id}/dossier`, { headers: getHeaders() })
    if (res.ok) dossierData.value = await res.json()
  } catch (e) {}
}

onMounted(() => { fetchSuspects() })
</script>

<style scoped>
.slide-right-enter-active,
.slide-right-leave-active { transition: transform 0.3s ease; }
.slide-right-enter-from,
.slide-right-leave-to { transform: translateX(100%); }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255, 255, 255, 0.2); border-radius: 4px; }
</style>
