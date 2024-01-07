<template>
  <div>
    <h1>{{ message }}</h1>
    <h2>Aktualny gracz: {{ currentPlayer }}</h2>
    <button @click="startGame">Start New Game</button>
    <button @click="resetGame">Reset Game</button>
    <div class="board">
      <div v-for="(row, rowIndex) in boardState" :key="rowIndex">
        <button v-for="(cell, colIndex) in row" :key="colIndex"
                @click="makeMove(rowIndex, colIndex)"
                :disabled="cell !== ''"
                class="cell">
          {{ cell }}
        </button>
      </div>
    </div>

    <div v-if="games.length">
      <h2>Dostępne gry:</h2>
      <ul>
        <li v-for="game in games" :key="game.id">
          Gra #{{ game.id }} -
          <button @click="joinGame(game.id)">Dołącz</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      boardState: [],
      currentPlayer: "",
      gameId: null,
      message: "",
      games: [], // Lista dostępnych gier
    };
  },
  methods: {
    startGame() {
      axios.get("/api/start", {
        headers: {
          "Authorization": `Bearer ${this.getToken()}`,
          "Content-Type": "application/json"
        }
      })
          .then((res) => {
            this.handleResponse(res);
          })
          .catch((err) => {
            this.handleError(err);
          });
    },
    makeMove(row, col) {
      const moveData = {row, col, gameId: this.gameId};
      axios.post("/api/move", moveData, {
        headers: {
          "Authorization": `Bearer ${this.getToken()}`,
          "Content-Type": "application/json"
        }
      })
          .then((res) => {
            this.handleResponse(res);
          })
          .catch((err) => {
            this.handleError(err);
          });
    },
    resetGame() {
      axios.get(`/api/reset?gameId=${this.gameId}`, {
        headers: {
          "Authorization": `Bearer ${this.getToken()}`,
          "Content-Type": "application/json"
        }
      })
          .then((res) => {
            this.handleResponse(res);
          })
          .catch((err) => {
            this.handleError(err);
          });
    },
    fetchGames() {
      axios.get("/api/all_games", {
        headers: {
          "Authorization": `Bearer ${this.getToken()}`,
          "Content-Type": "application/json"
        }
      })
          .then(response => {
            this.games = response.data.games;
          })
          .catch(error => {
            console.error(error);
            // Obsługa błędów
          });
    },
    joinGame(gameId) {
      axios.post("/api/join", {gameId}, {
        headers: {
          "Authorization": `Bearer ${this.getToken()}`,
          "Content-Type": "application/json"
        }
      })
          .then(response => {
            this.handleResponse(response);
          })
          .catch(error => {
            this.handleError(error);
          });
    },
    getToken() {
      return localStorage.getItem('jwtToken');
    },
    handleResponse(res) {
      this.boardState = res.data.boardState;
      this.currentPlayer = res.data.currentPlayer;
      this.message = res.data.message;
      this.gameId = res.data.gameId;
    },
    handleError(err) {
      console.error(err);
      if (err.response && err.response.data) {
        this.message = err.response.data.error || 'Wystąpił błąd.';
      } else {
        this.message = 'Wystąpił problem z połączeniem z serwerem.';
      }
    }
  },
  created() {
    this.startGame();
    this.fetchGames();
  },
};
</script>

<style>
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

/* Dodaj tutaj dodatkowe style, jeśli potrzebne */
</style>
