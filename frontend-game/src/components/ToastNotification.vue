<template>
  <Transition name="toast">
    <div v-if="toastStore.show" class="fixed bottom-10 right-10 z-[9999] flex items-center gap-4 px-6 py-4 rounded-2xl shadow-[0_10px_40px_rgba(0,0,0,0.5)] border backdrop-blur-xl transition-all" :class="toastStore.type === 'success' ? 'bg-emerald-950/90 border-emerald-500/30' : (toastStore.type === 'error' ? 'bg-rose-950/90 border-rose-500/30' : 'bg-amber-950/90 border-amber-500/30')">
      <span class="material-symbols-rounded text-3xl drop-shadow-md" :class="toastStore.type === 'success' ? 'text-emerald-400' : (toastStore.type === 'error' ? 'text-rose-400' : 'text-amber-400')">
        {{ toastStore.type === 'success' ? 'check_circle' : (toastStore.type === 'error' ? 'error' : 'warning') }}
      </span>
      <div>
        <h4 class="font-black text-white text-sm uppercase tracking-wider mb-0.5">{{ toastStore.title }}</h4>
        <p class="font-medium text-xs" :class="toastStore.type === 'success' ? 'text-emerald-200' : (toastStore.type === 'error' ? 'text-rose-200' : 'text-amber-200')">{{ toastStore.message }}</p>
      </div>
      <button @click="toastStore.closeToast" class="ml-4 text-white/50 hover:text-white transition-colors">
        <span class="material-symbols-rounded text-sm">close</span>
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { useToastStore } from '../stores/toast'
const toastStore = useToastStore()
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.toast-enter-from,
.toast-leave-to { opacity: 0; transform: translateY(50px) scale(0.9); }
</style>