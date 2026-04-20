<template>
  <div class="min-h-screen bg-[#050505] text-white font-sans relative overflow-hidden">
    
    <div v-if="isAuthRoute" class="h-screen w-full bg-[#050505]">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>

    <div v-else class="flex h-screen w-full">
      <aside class="bg-[#0a0a0c] border-r border-zinc-900 flex flex-col py-8 transition-all duration-500 ease-in-out z-40 relative shadow-[5px_0_30px_rgba(0,0,0,0.8)]" :class="isSidebarExpanded ? 'w-64' : 'w-20'">
        <div class="flex items-center gap-3 px-4 mb-12 overflow-hidden h-12" :class="isSidebarExpanded ? 'justify-start' : 'justify-center'">
          <div class="min-w-[3rem] h-12 bg-[#050505] border border-zinc-800 flex items-center justify-center clip-esports shadow-[0_0_15px_rgba(0,0,0,0.8)]">
            <span class="material-symbols-rounded text-white text-2xl">swords</span>
          </div>
          <div class="flex flex-col whitespace-nowrap transition-opacity duration-300" :class="isSidebarExpanded ? 'opacity-100' : 'opacity-0 w-0'">
            <h1 class="text-xl font-black tracking-tighter uppercase italic leading-none text-white">Fantasy <span class="text-emerald-500">Pro</span></h1>
            <span class="text-[8px] font-bold text-zinc-600 uppercase tracking-[0.2em] mt-1">Terminal de Batalha</span>
          </div>
        </div>

        <nav class="flex-1 flex flex-col gap-2 px-3">
          <router-link to="/market" v-slot="{ isActive }">
            <button class="w-full flex items-center gap-4 py-4 rounded-xl transition-all duration-300 relative group overflow-hidden" :class="[isActive ? 'bg-zinc-900 text-white border border-zinc-800 shadow-[inset_0_0_10px_rgba(0,0,0,1)]' : 'text-zinc-600 hover:bg-[#050505] hover:text-zinc-400', isSidebarExpanded ? 'px-6 justify-start' : 'px-0 justify-center']">
              <span class="material-symbols-rounded min-w-[24px]" :class="isActive ? 'text-emerald-500' : ''">storefront</span>
              <span class="text-[10px] font-black uppercase tracking-[0.2em] whitespace-nowrap transition-opacity duration-300" :class="isSidebarExpanded ? 'opacity-100' : 'opacity-0 hidden'">Mercado Negro</span>
            </button>
          </router-link>

          <router-link to="/deck" v-slot="{ isActive }">
            <button class="w-full flex items-center gap-4 py-4 rounded-xl transition-all duration-300 relative group overflow-hidden" :class="[isActive ? 'bg-zinc-900 text-white border border-zinc-800 shadow-[inset_0_0_10px_rgba(0,0,0,1)]' : 'text-zinc-600 hover:bg-[#050505] hover:text-zinc-400', isSidebarExpanded ? 'px-6 justify-start' : 'px-0 justify-center']">
              <span class="material-symbols-rounded min-w-[24px]" :class="isActive ? 'text-emerald-500' : ''">style</span>
              <span class="text-[10px] font-black uppercase tracking-[0.2em] whitespace-nowrap transition-opacity duration-300" :class="isSidebarExpanded ? 'opacity-100' : 'opacity-0 hidden'">Arsenal</span>
            </button>
          </router-link>

          <router-link to="/squad" v-slot="{ isActive }">
            <button class="w-full flex items-center gap-4 py-4 rounded-xl transition-all duration-300 relative group overflow-hidden" :class="[isActive ? 'bg-zinc-900 text-white border border-zinc-800 shadow-[inset_0_0_10px_rgba(0,0,0,1)]' : 'text-zinc-600 hover:bg-[#050505] hover:text-zinc-400', isSidebarExpanded ? 'px-6 justify-start' : 'px-0 justify-center']">
              <span class="material-symbols-rounded min-w-[24px]" :class="isActive ? 'text-emerald-500' : ''">shield</span>
              <span class="text-[10px] font-black uppercase tracking-[0.2em] whitespace-nowrap transition-opacity duration-300" :class="isSidebarExpanded ? 'opacity-100' : 'opacity-0 hidden'">Esquadrão Tático</span>
            </button>
          </router-link>
        </nav>

        <div class="mt-auto flex flex-col gap-4 px-3">
          <button @click="isSidebarExpanded = !isSidebarExpanded" class="w-full flex items-center justify-center py-4 rounded-xl bg-[#050505] border border-zinc-900 text-zinc-600 hover:text-white transition-colors">
            <span class="material-symbols-rounded transition-transform duration-500" :class="isSidebarExpanded ? 'rotate-180' : ''">chevron_right</span>
          </button>

          <div v-if="isSidebarExpanded" class="flex flex-col bg-[#050505] border border-zinc-900 rounded-xl p-4 shadow-inner transition-all duration-500">
            <span class="text-[8px] font-black text-zinc-600 uppercase tracking-widest mb-1">Capital Ativo</span>
            <span class="text-xl font-mono font-black text-emerald-500">{{ userBalance.toLocaleString() }} C$</span>
          </div>

          <button @click="logout" class="w-full flex items-center gap-4 py-4 rounded-xl text-zinc-700 hover:bg-rose-950/20 hover:text-rose-500 border border-transparent hover:border-rose-900/50 transition-colors" :class="isSidebarExpanded ? 'px-6 justify-start' : 'px-0 justify-center'">
            <span class="material-symbols-rounded min-w-[24px]">logout</span>
            <span class="text-[10px] font-black uppercase tracking-[0.2em] whitespace-nowrap transition-opacity duration-300" :class="isSidebarExpanded ? 'opacity-100' : 'opacity-0 hidden'">Desconectar</span>
          </button>
        </div>
      </aside>

      <main class="flex-1 h-screen overflow-y-auto p-4 md:p-8 relative bg-[#050505]">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>

    <ToastNotification />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useFantasyStore } from './stores/fantasy'
import { useRoute, useRouter } from 'vue-router'
import ToastNotification from './components/ToastNotification.vue'

const store = useFantasyStore()
const route = useRoute()
const router = useRouter()
const isSidebarExpanded = ref(false)

// Validação segura baseada no motor do Vue Router
const isAuthRoute = computed(() => {
  return route.path.includes('login') || route.name === 'Login'
})

const userBalance = computed(() => {
  return store.profile?.wallet_balance ?? 0
})

const logout = () => {
  // Limpeza limpa sem reload bruto
  localStorage.removeItem('token')
  sessionStorage.clear()
  store.profile = null
  
  if (!route.path.includes('login')) {
    router.push('/login')
  }
}

const authenticateSession = async () => {
  // 1. Se estiver na página de login, a tela estabiliza e não faz mais nada
  if (route.path.includes('login')) return

  // 2. Se não estiver no login, procura o token
  const token = localStorage.getItem('token')
  if (!token) {
    logout()
    return
  }

  // 3. Se tiver token, busca o perfil para garantir acesso
  if (store.fetchProfile && !store.profile) {
    await store.fetchProfile()
    
    // Se o backend recusar (mesmo com o God Mode), desloga silenciosamente
    if (!store.profile) {
      logout()
    }
  }
}

// O segredo para parar o piscar da tela:
// Apenas rodar a validação DEPOIS do Vue Router ter lido a URL completa
onMounted(async () => {
  await router.isReady()
  authenticateSession()
})

watch(() => route.path, (newPath) => {
  if (!newPath.includes('login')) {
    authenticateSession()
  }
})
</script>

<style>
.clip-esports { clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }
.clip-esports-small { clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px); }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #050505; }
::-webkit-scrollbar-thumb { background: #27272a; }
</style>