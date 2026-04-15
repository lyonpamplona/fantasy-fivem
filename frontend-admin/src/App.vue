<template>
  <div v-if="fatalError" class="min-h-screen bg-rose-950 text-white p-10 font-mono">
    <h1 class="text-3xl font-black mb-4">⚠️ Erro Crítico no Frontend</h1>
    <div class="bg-black/50 p-6 rounded-xl border border-rose-500 overflow-auto">
      <p class="text-rose-400">{{ fatalError }}</p>
    </div>
    <button @click="resetError" class="mt-6 px-6 py-2 bg-white text-black font-bold rounded hover:bg-slate-200">
      Voltar para o Login
    </button>
  </div>

  <div v-else class="min-h-screen bg-slate-950 font-sans text-white">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <ToastNotification />
  </div>
</template>

<script setup>
import { ref, onErrorCaptured } from 'vue'
import { useRouter } from 'vue-router'
import ToastNotification from './components/ToastNotification.vue'

const router = useRouter()
const fatalError = ref(null)

onErrorCaptured((err) => {
  console.error("Vue Crash Capturado:", err)
  fatalError.value = err.toString()
  return false
})

const resetError = () => {
  fatalError.value = null
  localStorage.removeItem('admin_token')
  router.push('/login')
}
</script>

<style>
.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from,
.fade-leave-to { opacity: 0; }
</style>