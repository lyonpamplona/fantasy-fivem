<template>
  <div class="min-h-screen bg-slate-950 flex items-center justify-center p-4 relative overflow-hidden">
    <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_10px,rgba(0,0,0,0.2)_10px,rgba(0,0,0,0.2)_20px)] pointer-events-none"></div>
    <div class="absolute inset-0 bg-gradient-to-br from-rose-900/20 to-black pointer-events-none"></div>

    <div class="w-full max-w-md bg-black/80 backdrop-blur-xl border border-rose-900/50 p-8 rounded-3xl shadow-[0_0_50px_rgba(225,29,72,0.15)] relative z-10">
      <div class="flex justify-center mb-6">
        <div class="w-16 h-16 bg-rose-500/10 border border-rose-500/30 rounded-2xl flex items-center justify-center shadow-inner">
          <span class="material-symbols-rounded text-rose-500 text-3xl">admin_panel_settings</span>
        </div>
      </div>

      <h2 class="text-2xl font-black text-white text-center uppercase tracking-widest mb-1"></h2>
      <p class="text-[10px] text-rose-400/70 text-center font-mono mb-8 uppercase tracking-widest"></p>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-[10px] font-black text-slate-500 uppercase tracking-widest mb-2">Password</label>
          <div class="relative">
            <span class="material-symbols-rounded absolute left-4 top-1/2 -translate-y-1/2 text-slate-600 text-sm">key</span>
            <input
              v-model="password"
              type="password"
              required
              class="w-full bg-slate-950 border border-slate-800 text-white text-sm rounded-xl px-11 py-3.5 focus:outline-none focus:border-rose-500 focus:ring-1 focus:ring-rose-500 transition-all font-mono"
              placeholder="••••••••"
            />
          </div>
        </div>

        <button
          type="submit"
          :disabled="isLoading"
          class="w-full py-4 bg-rose-700 hover:bg-rose-600 text-white font-black uppercase tracking-widest text-xs rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 shadow-lg"
        >
          <span v-if="isLoading" class="material-symbols-rounded animate-spin text-sm">sync</span>
          <span v-else class="material-symbols-rounded text-sm">login</span>
          {{ isLoading ? 'Autenticando...' : 'Acessar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useToastStore } from '../stores/toast'

const password = ref('')
const isLoading = ref(false)
const router = useRouter()
const toastStore = useToastStore()

const handleLogin = async () => {
  isLoading.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8001'
    const baseUrl = rawUrl.replace(/\/$/, '')

    const res = await fetch(`${baseUrl}/api/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: password.value })
    })

    if (res.ok) {
      const data = await res.json()
      localStorage.setItem('admin_token', data.token)
      toastStore.showToast('Acesso Concedido', 'Bem-vindo ao Centro de Comando.', 'success')
      setTimeout(() => {
        window.location.href = '/dashboard'
      }, 500) 
    } else {
      toastStore.showToast('Acesso Negado', 'Chave de autorização inválida.', 'error')
    }
  } catch (error) {
    toastStore.showToast('Falha de Conexão', 'Servidor de heurística inacessível.', 'error')
  } finally {
    isLoading.value = false
  }
}
</script>