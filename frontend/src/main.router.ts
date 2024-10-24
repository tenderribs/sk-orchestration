import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import LogoutView from '@/views/LogoutView.vue'
import SitesView from '@/views/SitesView.vue'

import { isLoggedIn } from './helpers/useIsLoggedIn'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: DashboardView,
      beforeEnter: (to, from, next) => {
        if (isLoggedIn.value) {
          next();
        } else {
          next({ name: 'login' }); // Redirect to login if not logged in
        }
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/logout',
      name: 'logout',
      component: LogoutView
    },
    {
      path: '/sites',
      name: 'sites',
      component: SitesView
    },
  ]
})

export default router
