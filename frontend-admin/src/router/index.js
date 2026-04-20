import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/login' },
  { 
    path: '/login', 
    component: () => import('../views/AdminLogin.vue'),
    beforeEnter: (to, from, next) => {
      localStorage.getItem('admin_token') ? next('/dashboard') : next()
    }
  },
  { 
    path: '/dashboard', 
    component: () => import('../views/AdminDashboard.vue'),
    beforeEnter: (to, from, next) => {
      localStorage.getItem('admin_token') ? next() : next('/login')
    }
  },
  { path: '/:pathMatch(.*)*', redirect: '/dashboard' }
]

export default createRouter({ history: createWebHistory(), routes })