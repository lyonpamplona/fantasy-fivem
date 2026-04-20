import { createRouter, createWebHistory } from 'vue-router'

// Importe as suas vistas (Verifique se os nomes dos ficheiros estão corretos com os seus)
import Login from '../views/Login.vue'
import Market from '../views/Market.vue'
import Deck from '../views/Deck.vue'
import Squad from '../views/Squad.vue'

const routes = [
  { path: '/', redirect: '/deck' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/market', name: 'Market', component: Market, meta: { requiresAuth: true } },
  { path: '/deck', name: 'Deck', component: Deck, meta: { requiresAuth: true } },
  { path: '/squad', name: 'Squad', component: Squad, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// O Porteiro Relaxado (Navigation Guard)
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  // Se a rota precisa de login e não há token, vai para o login
  if (requiresAuth && !token) {
    next('/login')
  } 
  // Se já tem token e tenta ir para o login, vai para o deck
  else if (to.path === '/login' && token) {
    next('/deck')
  } 
  // Caso contrário, navegação livre!
  else {
    next()
  }
})

export default router