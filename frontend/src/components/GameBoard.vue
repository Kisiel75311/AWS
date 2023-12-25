<!--frontend/src/components/GameBoard.vue-->
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
    };
  },
  methods: {
    startGame() {
      axios.get("http://localhost:5000/api/start", {
        headers: {
          "Content-Type": "application/json"
        }
      })
          .then((res) => {
            this.boardState = res.data.boardState;
            this.currentPlayer = res.data.currentPlayer;
            this.gameId = res.data.gameId;
            this.message = res.data.message;
            this.$forceUpdate();
          })
          .catch((err) => {
            console.error(err);
          });
    },
    makeMove(row, col) {
      const moveData = {row, col, gameId: this.gameId};
      axios.post("http://localhost:5000/api/move", moveData, {
        headers: {
          "Content-Type": "application/json"
        }
      })
          .then((res) => {
            this.boardState = res.data.boardState;
            this.currentPlayer = res.data.currentPlayer;
            this.message = res.data.message;
          })
          .catch((err) => {
            console.error(err);
          });
    },
    resetGame() {
      axios.get(`http://localhost:5000/api/reset?gameId=${this.gameId}`, {
        headers: {
          "Content-Type": "application/json"
        }
      })
          .then((res) => {
            this.boardState = res.data.boardState;
            this.currentPlayer = res.data.currentPlayer;
            this.message = res.data.message;
          })
          .catch((err) => {
            console.error(err);
          });
    },
  },
  created() {
    this.startGame();
  },
};
</script>

<style>
/* Styl dla komponentu gry */
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

.board button {
  width: 100px;
  height: 100px;
  /* Możesz dodać dodatkowe style tutaj */
}
</style>
