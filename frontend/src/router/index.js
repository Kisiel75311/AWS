import Vue from 'vue';
import Router from 'vue-router';
import GameBoard from '@/components/GameBoard';
import Login from "@/components/Login.vue";

Vue.use(Router);

export default new Router({
  mode: 'history', // Używa history API HTML5 do usuwania znaku hash (#) z URL
  routes: [
    {
      path: '/game', // Adres URL, pod którym będzie dostępny komponent GameBoard
      name: 'GameBoard',
      component: GameBoard
    },
    {
      path: '/login', // Adres URL, pod którym będzie dostępny komponent Login
      name: 'Login',
      component: Login
    },
    // Tutaj możesz dodać inne ścieżki do Twoich komponentów
  ]
});
