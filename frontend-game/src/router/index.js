import { createRouter, createWebHistory } from 'vue-router'
import Deck from '../views/Deck.vue'
import Squad from '../views/Squad.vue'
import Packs from '../views/Packs.vue'
import Market from '../views/Market.vue'

const routes = [
  { path: '/', redirect: '/deck' },
  { path: '/deck', component: Deck },
  { path: '/squad', component: Squad },
  { path: '/packs', component: Packs },
  { path: '/market', component: Market }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router