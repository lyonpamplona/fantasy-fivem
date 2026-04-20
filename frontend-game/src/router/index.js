import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/deck' },
  { path: '/deck', component: () => import('../views/Deck.vue') },
  { path: '/squad', component: () => import('../views/Squad.vue') },
  { path: '/market', component: () => import('../views/Market.vue') },
  { path: '/:pathMatch(.*)*', redirect: '/deck' }
]

export default createRouter({ history: createWebHistory(), routes })