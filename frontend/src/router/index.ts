import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import QuizView from '../views/QuizView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login',
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
    },
    {
      path: '/quiz',
      name: 'quiz',
      component: QuizView,
      meta: { requiresAuth: true },
    },
  ],
})

// Navigation guard for authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if ((to.path === '/login' || to.path === '/register') && token) {
    next('/quiz')
  } else {
    next()
  }
})

export default router
