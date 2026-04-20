<template>
  <div class="min-h-screen bg-[#050505] flex items-center justify-center relative overflow-hidden font-sans">
    
    <div class="absolute inset-0 pointer-events-none">
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] blur-[150px] rounded-full bg-emerald-900/20 opacity-50 animate-pulse"></div>
      <div class="absolute inset-0 bg-[repeating-linear-gradient(45deg,transparent,transparent_4px,rgba(255,255,255,0.01)_4px,rgba(255,255,255,0.01)_8px)]"></div>
    </div>

    <div class="relative z-10 w-full max-w-md bg-[#0a0a0c]/80 backdrop-blur-2xl border border-zinc-800 p-10 flex flex-col items-center clip-esports shadow-[0_0_50px_rgba(0,0,0,0.8)]">
      
      <div class="w-20 h-20 bg-[#050505] border border-zinc-700 flex items-center justify-center rotate-45 mb-8 shadow-[0_0_20px_rgba(16,185,129,0.2)]">
        <span class="material-symbols-rounded text-4xl text-emerald-500 -rotate-45">swords</span>
      </div>

      <h1 class="text-4xl font-black text-white tracking-tighter uppercase italic mb-2">Fantasy <span class="text-emerald-500">Pro</span></h1>
      <p class="text-[10px] font-mono text-zinc-500 uppercase tracking-[0.3em] mb-12 text-center">Terminal de Acesso Restrito</p>

      <button @click="loginDevMode" :disabled="isProcessing" class="w-full flex items-center justify-center gap-4 py-4 bg-[#5865F2] hover:bg-[#4752C4] text-white transition-colors clip-esports-small group shadow-[0_0_20px_rgba(88,101,242,0.3)] disabled:opacity-50">
        <span v-if="isProcessing" class="material-symbols-rounded animate-spin">sync</span>
        <svg v-else class="w-6 h-6 fill-current group-hover:scale-110 transition-transform" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.317 4.3698a19.7913 19.7913 0 00-4.8851-1.5152.0741.0741 0 00-.0785.0371c-.211.3753-.4447.8648-.6083 1.2495-1.8447-.2762-3.68-.2762-5.4868 0-.1636-.3933-.4058-.8742-.6177-1.2495a.077.077 0 00-.0785-.037 19.7363 19.7363 0 00-4.8852 1.515.0699.0699 0 00-.0321.0277C.5334 9.0458-.319 13.5799.0992 18.0578a.0824.0824 0 00.0312.0561c2.0528 1.5076 4.0413 2.4228 5.9929 3.0294a.0777.0777 0 00.0842-.0276c.4616-.6304.8731-1.2952 1.226-1.9942a.076.076 0 00-.0416-.1057c-.6528-.2476-1.2743-.5495-1.8722-.8923a.077.077 0 01-.0076-.1277c.1258-.0943.2517-.1923.3718-.2914a.0743.0743 0 01.0776-.0105c3.9278 1.7933 8.18 1.7933 12.0614 0a.0739.0739 0 01.0785.0095c.1202.099.246.1981.3728.2924a.077.077 0 01-.0066.1276 12.2986 12.2986 0 01-1.873.8914.0766.0766 0 00-.0407.1067c.3604.698.7719 1.3628 1.225 1.9932a.076.076 0 00.0842.0286c1.961-.6067 3.9495-1.5219 6.0023-3.0294a.077.077 0 00.0313-.0552c.5004-5.177-.8382-9.6739-3.5485-13.6604a.061.061 0 00-.0312-.0286zM8.02 15.3312c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9555-2.4189 2.157-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.9555 2.4189-2.1569 2.4189zm7.9748 0c-1.1825 0-2.1569-1.0857-2.1569-2.419 0-1.3332.9554-2.4189 2.1569-2.4189 1.2108 0 2.1757 1.0952 2.1568 2.419 0 1.3332-.946 2.4189-2.1568 2.4189z"/></svg>
        <span class="text-[11px] font-black uppercase tracking-[0.2em]">{{ isProcessing ? 'Autenticando...' : 'Autenticar (Dev Mode)' }}</span>
      </button>

      <div class="mt-8 pt-6 border-t border-zinc-900 w-full text-center">
         <span class="text-[8px] font-mono text-zinc-600 uppercase tracking-widest">Conexão de Teste Administrativa</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isProcessing = ref(false)

const loginDevMode = async () => {
  isProcessing.value = true
  try {
    const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const baseUrl = rawUrl.replace(/\/$/, '')
    
    // Chama a nossa rota secreta que criámos no auth.py
    const res = await fetch(`${baseUrl}/api/auth/dev-login/dev_test_123`)
    if (res.ok) {
      const data = await res.json()
      // Guarda o token no navegador
      localStorage.setItem('token', data.access_token)
      // Empurra o jogador para o Deck, o que liberta a navegação!
      router.push('/deck')
    } else {
      console.error("Falha ao contactar a API de testes.")
    }
  } catch (error) {
    console.error("Servidor offline:", error)
  } finally {
    isProcessing.value = false
  }
}
</script>

<style scoped>
.clip-esports { clip-path: polygon(30px 0, 100% 0, 100% calc(100% - 30px), calc(100% - 30px) 100%, 0 100%, 0 30px); }
.clip-esports-small { clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px); }
</style>