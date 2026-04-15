import { defineStore } from 'pinia'
import { buildApiUrl, buildWsUrl } from '../utils/api'

export const useFantasyStore = defineStore('fantasy', {
  state: () => ({
    isAuthenticated: false,
    balance: 0,
    cards: [],
    ws: null
  }),
  actions: {
    async login(token) {
      localStorage.setItem('jwt_token', token)
      this.isAuthenticated = true
      await this.fetchProfile()
      await this.fetchCards()
      this.connectWebSocket()
    },
    async fetchProfile() {
      try {
        const res = await fetch(buildApiUrl('/api/cards/user/me/profile'), {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('jwt_token')}` }
        })
        if (res.ok) {
          const data = await res.json()
          this.balance = data.wallet_balance
        }
      } catch (e) {}
    },
    async fetchCards() {
      try {
        const res = await fetch(buildApiUrl('/api/cards/user/me'), {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('jwt_token')}` }
        })
        if (res.ok) {
          this.cards = await res.json()
        }
      } catch (e) {}
    },
    async burnCards(cardIds) {
      try {
        const res = await fetch(buildApiUrl('/api/cards/burn'), {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('jwt_token')}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(cardIds)
        })
        if (res.ok) {
          const newCard = await res.json()
          await this.fetchCards()
          return newCard
        }
      } catch (e) {}
      return null
    },
    connectWebSocket() {
      if (this.ws) return
      this.ws = new WebSocket(buildWsUrl('/ws/cards'))
      this.ws.onmessage = (event) => {
        const updates = JSON.parse(event.data)
        updates.forEach(u => {
          const card = this.cards.find(c => c.id === u.card_id)
          if (card) {
            card.xp = u.xp
            card.level = u.level
            card.kills = u.kills
          }
        })
      }
    }
  }
})
