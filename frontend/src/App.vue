<template>
  <div id="app">
    <GameBoard :board="board" @makeMove="handleMakeMove"/>
    <GameControl @startGame="handleStartGame" @resetGame="handleResetGame"/>
    <GameStatus :statusMessage="statusMessage"/>
  </div>
</template>

<script>
import GameBoard from './components/GameBoard.vue';
import GameControl from './components/GameControl.vue';
import GameStatus from './components/GameStatus.vue';
import api from '@/services/api';

export default {
  name: 'App',
  components: {
    GameBoard,
    GameControl,
    GameStatus
  },
  data() {
    return {
      board: [['', '', ''], ['', '', ''], ['', '', '']],
      statusMessage: 'Welcome to Tic-Tac-Toe!'
    };
  },
  methods: {
    handleStartGame() {
      api.startGame()
        .then(response => {
          this.statusMessage = response.data.message;
          // Zaktualizuj stan planszy, jeśli potrzebny
        })
        .catch(error => {
          console.error('Start game error:', error);
          this.statusMessage = 'Error starting the game.';
        });
    },
    handleMakeMove(row, col) {
      api.makeMove(row, col)
        .then(response => {
          this.statusMessage = response.data.message;
          // Aktualizacja stanu planszy z odpowiedzią
          // Możesz potrzebować dodatkowej logiki tutaj
        })
        .catch(error => {
          console.error('Make move error:', error);
          this.statusMessage = 'Error making a move.';
        });
    },
    handleResetGame() {
      api.resetGame()
        .then(response => {
          this.statusMessage = response.data.message;
          // Resetowanie stanu planszy
          this.board = [['', '', ''], ['', '', ''], ['', '', '']];
        })
        .catch(error => {
          console.error('Reset game error:', error);
          this.statusMessage = 'Error resetting the game.';
        });
    },
  }
};
</script>
