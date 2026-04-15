<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-950 p-4 relative overflow-hidden">
    <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-rose-900/20 via-slate-950 to-slate-950"></div>

    <div class="relative z-10 w-full max-w-md bg-slate-900/60 backdrop-blur-2xl border border-white/10 rounded-[30px] p-10 shadow-2xl">
      <div class="text-center mb-10">
        <div class="w-16 h-16 bg-rose-500/10 rounded-2xl flex items-center justify-center mx-auto mb-4 border border-rose-500/20">
          <span class="material-symbols-rounded text-rose-500 text-3xl">admin_panel_settings</span>
        </div>
        <h1 class="text-3xl font-black text-white tracking-tighter uppercase">Acesso Restrito</h1>
        <p class="text-sm text-slate-400 mt-2 font-medium">Insira sua credencial de segurança.</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-[10px] font-black uppercase tracking-widest text-slate-500 mb-2 ml-1">Credencial Administrativa</label>
          <div class="relative">
            <span class="material-symbols-rounded absolute left-4 top-1/2 -translate-y-1/2 text-slate-500">key</span>
            <input 
              v-model="password" 
              type="password" 
              required
              class="w-full bg-black/40 border border-white/10 rounded-xl py-4 pl-12 pr-4 text-white focus:outline-none focus:border-rose-500/50 focus:ring-1 focus:ring-rose-500/50 transition-all font-mono text-sm"
              placeholder="••••••••••••"
            >
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-rose-600 hover:bg-rose-500 text-white font-black uppercase tracking-widest py-4 rounded-xl transition-all flex items-center justify-center gap-2 shadow-[0_0_20px_rgba(225,29,72,0.3)] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="material-symbols-rounded animate-spin text-lg">sync</span>
          <span v-else class="material-symbols-rounded text-lg">login</span>
          {{ isLoading ? 'Verificando...' : 'Autenticar' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const API_URL = (import.meta.env.VITE_API_URL || window.location.origin).replace(/\/+$/, '')
const router = useRouter()
const password = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  if (!password.value || isLoading.value) return
  isLoading.value = true
  
  try {
    const res = await fetch(`${API_URL}/api/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: password.value })
    })

    if (res.ok) {
      const data = await res.json()
      localStorage.setItem('admin_token', data.token)
      router.push('/dashboard')
    } else {
      alert("Acesso Negado: Credencial Inválida")
      password.value = ''
    }
  } catch (error) {
    alert("Erro de conexão com o servidor.")
  } finally {
    isLoading.value = false
  }
}
</script>
