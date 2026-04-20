import { defineStore } from 'pinia'

export const useFantasyStore = defineStore('fantasy', {
  state: () => ({
    profile: null,
    cards: [],
    packs: [],
    isProfileFetching: false, // Bloqueia pedidos paralelos
    isCardsFetching: false
  }),
  getters: {
    user: (state) => state.profile,
  },
  actions: {
    getHeaders() {
      const token = localStorage.getItem('token')
      return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    },
    async fetchProfile() {
      // Se já estiver a carregar, aborta o novo pedido para parar a "ametralhadora"
      if (this.isProfileFetching) return
      
      const token = localStorage.getItem('token')
      if (!token) return

      this.isProfileFetching = true
      try {
        const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const baseUrl = rawUrl.replace(/\/$/, '')
        
        const response = await fetch(`${baseUrl}/api/user/me/profile`, {
          headers: this.getHeaders()
        })
        
        if (response.ok) {
          const data = await response.json()
          this.profile = data
        } else if (response.status === 401 || response.status === 404) {
          // Em vez de limpar o token imediatamente e forçar o logout (que causava o loop),
          // Apenas limpamos os dados do estado do Vue em silêncio.
          // Deixamos a responsabilidade de expulsar o utilizador para o App.vue
          this.profile = null
        }
      } catch (error) {
        console.warn("Erro de rede ao buscar perfil:", error)
      } finally {
        this.isProfileFetching = false
      }
    },
    async fetchCards() {
      if (this.isCardsFetching) return
      
      const token = localStorage.getItem('token')
      if (!token) return

      this.isCardsFetching = true
      try {
        const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const baseUrl = rawUrl.replace(/\/$/, '')
        
        const response = await fetch(`${baseUrl}/api/cards/user/me`, {
          headers: this.getHeaders()
        })
        
        if (response.ok) {
          const data = await response.json()
          this.cards = data
        }
      } catch (error) {
        console.warn("Erro de rede ao buscar arsenal:", error)
      } finally {
        this.isCardsFetching = false
      }
    },
    async fetchPacks() {
      const token = localStorage.getItem('token')
      if (!token) return

      try {
        const rawUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000'
        const baseUrl = rawUrl.replace(/\/$/, '')
        
        const response = await fetch(`${baseUrl}/api/packs/user/me`, {
          headers: this.getHeaders()
        })
        
        if (response.ok) {
          const data = await response.json()
          this.packs = data
        }
      } catch (error) {}
    }
  }
})