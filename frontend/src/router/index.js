// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import GameBoard from '@/components/GameBoard';
import LoginComponent from '@/components/LoginComponent';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/start'  // Dodajemy przekierowanie z '/' na '/start'
    },
    {
      path: '/game',
      name: 'GameBoard',
      component: GameBoard
    },
    {
      path: '/start',
      name: 'LoginComponent',
      component: LoginComponent
    },
    // Możesz dodać tutaj inne ścieżki
  ]
});

export default router;