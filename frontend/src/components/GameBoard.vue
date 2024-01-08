<!--frontend-new/py-project/src/GameBoard.vue-->
<template>
  <div class="gameboard-container">
    <h1>GameBoard</h1>
    <h2>Aktualny gracz: {{ currentPlayer }}</h2>
    <button @click="startGame">Start New Game</button>
    <button @click="resetGame">Reset Game</button>
    <button @click="joinRandomGame">Join Random Game</button>
    <button @click="leaveGame">Leave Game</button>
    <div v-if="message" class="message">{{ message }}</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div class="board">
      <div v-for="(row, rowIndex) in boardState" :key="rowIndex" class="board-row">
        <button v-for="(cell, colIndex) in row" :key="colIndex"
                @click="makeMove(gameId, rowIndex, colIndex)"
                :disabled="cell !== '.'"
                class="cell">
          {{ cell === '.' ? '' : cell }}
        </button>
      </div>
    </div>

    <button @click="fetchLeaderboard">Show Leaderboard</button>
    <div v-if="showLeaderboard" class="leaderboard">
      <h2>Leaderboard</h2>
      <ul>
        <li v-for="player in leaderboard" :key="player.id">
          {{ player.login }} - {{ player.elo_rating }} Points
        </li>
      </ul>
    </div>


    <div class="games-list">
      <h2>Dostępne gry:</h2>
      <ul>
        <li v-for="game in games" :key="game.id">
          Gra #{{ game.id }} - Gracze: {{ countPlayers(game) }}/2
          <button :disabled="isGameFull(game)" @click="joinGame(game.id)">Dołącz do gry</button>
        </li>
      </ul>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      boardState: [],
      currentPlayer: "",
      gameId: null,
      message: "",
      errorMessage: "",
      games: [],
      jwtUserId: this.getJwtUserId(),
      leaderboard: [],
      showLeaderboard: false,
    };
  },
  mounted() {
    this.fetchGames();
    this.fetchLeaderboard();
    this.pollGameStatus = setInterval(this.fetchCurrentGame, 2000);
  },
  methods: {
    getJwtUserId() {
      const token = localStorage.getItem('jwtToken');
      if (token) {
        const payloadBase64 = token.split('.')[1];
        const decodedJson = atob(payloadBase64);
        const decoded = JSON.parse(decodedJson);
        return decoded.identity;
      }
      return null;
    },
    fetchGames() {
      axios.get('/api/all_games')
          .then(response => {
            this.games = response.data.games;
          })
          .catch(this.handleError);
    },
    startGame() {
      axios.get('/api/start', {headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}})
          .then(response => {
            this.handleResponse(response);
            this.fetchGames();
          })
          .catch(this.handleError);
    },
    makeMove(gameId, row, col) {
      const postData = {
        gameId: this.gameId,
        row: row,
        col: col
      };

      axios.post('/api/move', postData, {
        headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}
      })
          .then(response => {
            this.handleResponse(response);
          })
          .catch(this.handleError);
    },

    resetGame() {
      axios.get(`/api/reset?gameId=${this.gameId}`,
          {headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}})
          .then(response => {
            this.handleResponse(response);
          })
          .catch(this.handleError);
    },
    joinGame(gameId) {
      axios.post('/api/join', {gameId},
          {headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}})
          .then(response => {
            this.handleResponse(response);
            this.fetchGames();
          })
          .catch(this.handleError);
    },
    fetchCurrentGame() {
      if (this.gameId) {
        axios.get(`/api/game/${this.gameId}`,
            {headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}})
            .then(response => {
              this.handleResponse(response);
            })
            .catch(this.handleError);
      }
    },
    handleResponse(res) {
      this.boardState = res.data.boardState;
      this.currentPlayer = res.data.currentPlayer;
      this.gameId = res.data.gameId;
      this.message = res.data.message;
    },
    handleError(error) {
      this.errorMessage = error.response.data.error;
    },
    countPlayers(game) {
      return (game.player1_id ? 1 : 0) + (game.player2_id ? 1 : 0);
    },
    isGameFull(game) {
      return this.countPlayers(game) === 2;
    },
    joinRandomGame() {
      axios.post('/api/join_random', {}, {
        headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}
      })
          .then(response => {
            this.handleResponse(response);
            this.fetchGames();
          })
          .catch(this.handleError);
    },

    leaveGame() {
      axios.post('/api/leave', {}, {
        headers: {"Authorization": `Bearer ${localStorage.getItem('jwtToken')}`}
      })
          .then(response => {
            this.handleResponse(response);
            // Additional logic to handle leaving the game
          })
          .catch(this.handleError);
    },

    fetchLeaderboard() {
      axios.get('/api/leaderboard')
          .then(response => {
            this.leaderboard = response.data.players;
            this.showLeaderboard = true;
          })
          .catch(this.handleError);
    },
  },
  beforeUnmount() {
    if (this.pollGameStatus) {
      clearInterval(this.pollGameStatus);
    }
  }
};
</script>

<style>
.gameboard-container {
  /* Tutaj dodaj swoje style */
}

.board {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  gap: 10px;
  max-width: 300px;
  margin: auto;
}

.cell {
  width: 100px;
  height: 100px;
  border: 1px solid #000;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2em;
  cursor: pointer;
}

.leaderboard {
  margin-top: 20px;
}

.leaderboard ul {
  list-style: none;
  padding: 0;
}

.leaderboard li {
  margin-bottom: 5px;
}

/* Dodaj tutaj dodatkowe style, jeśli potrzebne */
</style>
