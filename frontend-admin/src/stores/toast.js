import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useToastStore = defineStore('toast', () => {
  const show = ref(false)
  const title = ref('')
  const message = ref('')
  const type = ref('success') 
  let timeout = null

  const showToast = (newTitle, newMessage, newType = 'success') => {
    title.value = newTitle
    message.value = newMessage
    type.value = newType
    show.value = true

    
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => {
      show.value = false
    }, 5000)
  }

  const closeToast = () => {
    show.value = false
  }

  return { show, title, message, type, showToast, closeToast }
})