<template>
  <Transition name="toast">
    <div v-if="toastStore.show" class="fixed top-6 right-6 z-[9999] min-w-[280px] max-w-sm flex items-start gap-4 p-4 bg-[#0a0a0c] border shadow-[0_10px_30px_rgba(0,0,0,0.8)] clip-esports-small transition-all" :class="toastStore.type === 'success' ? 'border-emerald-600' : (toastStore.type === 'error' ? 'border-rose-600' : 'border-yellow-500')">
      
      <div class="mt-0.5 flex-shrink-0">
        <span class="material-symbols-rounded text-lg drop-shadow-md" :class="toastStore.type === 'success' ? 'text-emerald-500' : (toastStore.type === 'error' ? 'text-rose-500' : 'text-yellow-500')">
          {{ toastStore.type === 'success' ? 'check_circle' : (toastStore.type === 'error' ? 'error' : 'warning') }}
        </span>
      </div>

      <div class="flex-1 flex flex-col">
        <h4 class="text-[10px] font-black uppercase tracking-[0.2em] text-white mb-0.5">{{ toastStore.title }}</h4>
        <p class="text-[10px] font-mono leading-tight text-zinc-400">{{ toastStore.message }}</p>
      </div>

      <button @click="toastStore.closeToast" class="ml-2 text-zinc-600 hover:text-white transition-colors flex-shrink-0">
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
.clip-esports-small { clip-path: polygon(8px 0, 100% 0, 100% calc(100% - 8px), calc(100% - 8px) 100%, 0 100%, 0 8px); }

.toast-enter-active,
.toast-leave-active { transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
.toast-enter-from,
.toast-leave-to { opacity: 0; transform: translateX(50px) scale(0.95); }
</style>