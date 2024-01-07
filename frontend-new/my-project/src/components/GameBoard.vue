<template>
  <div class="gameboard-container">
    <h1>GameBoard</h1>

    <h2>Aktualny gracz: {{ currentPlayer }}</h2>
    <button @click="startGame">Start New Game</button>
    <button @click="resetGame">Reset Game</button>

    <div class="message">{{ message }}</div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

    <div class="board">
      <div v-for="(row, rowIndex) in boardState" :key="rowIndex" class="board-row">
        <button v-for="(cell, colIndex) in row" :key="colIndex"
                @click="makeMove(rowIndex, colIndex)"
                :disabled="cell !== '' || currentPlayer !== jwtUserId"
                class="cell">
          {{ cell }}
        </button>
      </div>
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
      games: [], // Lista dostępnych gier
      jwtUserId: this.getJwtUserId() // Wyciąga ID użytkownika z tokenu JWT
    };
  },
  mounted() {
    // this.jwtUserId = this.getJwtUserId();
    this.fetchGames();
  },
  methods: {
    getJwtUserId() {
      // Funkcja do wyodrębnienia ID użytkownika z tokenu JWT
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
      const token = localStorage.getItem('jwtToken');
      axios.get('/api/start', {headers: {'Authorization': `Bearer ${token}`}})
          .then(response => {
            this.handleResponse(response);
            this.fetchGames();
          })
          .catch(this.handleError);
    },
    makeMove(row, col) {
      const token = localStorage.getItem('jwtToken');
      const moveData = {row, col, gameId: this.gameId};
      axios.post("/api/move", moveData, {
        headers: {'Authorization': `Bearer ${token}`},
        params: {gameId: this.gameId}
      })
          .then((res) => {
            this.handleResponse(res);
          })
          .catch((err) => {
            this.handleError(err);
          });
    },
    resetGame() {
      const token = localStorage.getItem('jwtToken');
      axios.get('/api/reset', {
        headers: {'Authorization': `Bearer ${token}`},
        params: {gameId: this.gameId}
      })
          .then(this.handleResponse)
          .catch(this.handleError);
    },
    handleResponse(res) {
      this.boardState = res.data.boardState;
      this.currentPlayer = res.data.currentPlayer;
      this.message = res.data.message;
      this.gameId = res.data.gameId;
      this.errorMessage = ""; // Clear any previous errors
    },
    handleError(err) {
      if (err.response) {
        this.errorMessage = err.response.data.error || 'An error occurred on the server.';
      } else if (err.request) {
        this.errorMessage = 'The request was made but no response was received.';
      } else {
        this.errorMessage = 'Something went wrong in setting up the request.';
      }
    },
    countPlayers(game) {
      return (game.player1_id ? 1 : 0) + (game.player2_id ? 1 : 0);
    },
    isGameFull(game) {
      return this.countPlayers(game) === 2;
    },
    joinGame(gameId) {
      // Logika dołączania do gry
      console.log('Joining game:', gameId);
      // Tutaj dodać kod dołączania do gry
    }
  }
};
</script>

<style>
.gameboard-container {
  /* Your styles */
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
}

.board-row {
  /* Your styles for the board rows */
}

.error-message {
  color: red;
  /* Styles for error messages */
}

.message {
  /* Styles for general messages */
}

.games-list {
  /* Styles for the list of available games */
}
</style>
