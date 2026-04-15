<template>
  <div class="min-h-screen bg-slate-950 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-slate-950 to-black font-sans selection:bg-[var(--md-sys-color-primary)] selection:text-white">
    <nav class="sticky top-0 z-50 backdrop-blur-2xl bg-black/40 border-b border-white/10 px-6 py-4 flex justify-between items-center shadow-2xl">
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 bg-[var(--md-sys-color-primary)] rounded-xl flex items-center justify-center shadow-[0_0_20px_var(--md-sys-color-primary)]">
          <span class="material-symbols-rounded text-white font-black">bolt</span>
        </div>
        <span class="text-2xl font-black text-white tracking-tighter uppercase drop-shadow-md">Fantasy <span class="text-[var(--md-sys-color-primary)]">FiveM</span></span>
      </div>

      <div class="flex bg-black/40 p-1.5 rounded-2xl border border-white/5">
        <router-link to="/deck" class="px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest transition-all duration-300 flex items-center gap-2" active-class="bg-white/10 text-white shadow-inner" exact-active-class="bg-white/10 text-white shadow-inner">
          <span class="material-symbols-rounded text-sm">style</span> Meu Deck
        </router-link>
        <router-link to="/squad" class="px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest transition-all duration-300 text-slate-400 hover:text-white flex items-center gap-2" active-class="bg-white/10 text-white shadow-inner" exact-active-class="bg-white/10 text-white shadow-inner">
          <span class="material-symbols-rounded text-sm">sports_esports</span> Formação
        </router-link>
        <router-link to="/packs" class="px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest transition-all duration-300 text-slate-400 hover:text-white flex items-center gap-2" active-class="bg-[var(--md-sys-color-primary)] text-white shadow-[0_0_15px_var(--md-sys-color-primary)]" exact-active-class="bg-[var(--md-sys-color-primary)] text-white shadow-[0_0_15px_var(--md-sys-color-primary)]">
          <span class="material-symbols-rounded text-sm">shopping_bag</span> Loja
        </router-link>
        <router-link to="/market" class="px-6 py-2.5 rounded-xl font-bold text-xs uppercase tracking-widest transition-all duration-300 text-slate-400 hover:text-white flex items-center gap-2" active-class="bg-emerald-600 text-white shadow-[0_0_15px_#059669]" exact-active-class="bg-emerald-600 text-white shadow-[0_0_15px_#059669]">
          <span class="material-symbols-rounded text-sm">storefront</span> Mercado
        </router-link>
      </div>
    </nav>

    <main class="max-w-[1600px] mx-auto p-6 md:p-10 h-[calc(100vh-88px)]">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <ToastNotification />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useToastStore } from './stores/toast'
import ToastNotification from './components/ToastNotification.vue'
import { buildWsUrl } from './utils/api'

const toastStore = useToastStore()
let ws = null

const connectWebSocket = () => {
  ws = new WebSocket(buildWsUrl('/ws/feed'))
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'drop') {
      const isLegendary = data.rarity === 'LEGENDARY'
      toastStore.showToast(
        'Drop Global', 
        `${data.player} acabou de tirar ${data.card_player} (${data.rarity})!`, 
        isLegendary ? 'warning' : 'success'
      )
    }
  }
  
  ws.onclose = () => {
    setTimeout(connectWebSocket, 5000)
  }
}

onMounted(() => {
  connectWebSocket()
})

onUnmounted(() => {
  if (ws) ws.close()
})
</script>

<style>
.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s ease, transform 0.3s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; transform: translateY(10px); }
</style>
