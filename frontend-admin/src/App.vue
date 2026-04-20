<template>
  <div class="min-h-screen bg-slate-950 font-sans selection:bg-rose-500 selection:text-white">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
    <ToastNotification />
  </div>
</template>

<script setup>
import ToastNotification from './components/ToastNotification.vue'
</script>

<style>
.fade-enter-active, .fade-leave-active { transition: opacity 0.2s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>