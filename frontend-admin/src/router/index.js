import { createRouter, createWebHistory } from 'vue-router'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  { 
    path: '/', 
    redirect: '/login' 
  },
  { 
    path: '/login', 
    component: AdminLogin,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('admin_token')) {
        next('/dashboard')
      } else {
        next()
      }
    }
  },
  { 
    path: '/dashboard', 
    component: AdminDashboard,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('admin_token')) {
        next()
      } else {
        next('/login')
      }
    }
  },
  { 
    path: '/:pathMatch(.*)*', 
    redirect: '/dashboard' 
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router