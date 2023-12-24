<!--frontend/src/components/GameBoard.vue-->
<template>
  <div>
    <h1>{{ message }}</h1>
    <h2>Aktualny gracz: {{ currentPlayer }}</h2>
    <button @click="startGame">Start New Game</button>
    <div class="board">
      <div v-for="(row, rowIndex) in boardState" :key="rowIndex">
        <button v-for="(cell, colIndex) in row" :key="colIndex"
                @click="makeMove(rowIndex, colIndex)"
                :disabled="cell !== ''">
          {{ cell }}
        </button>
      </div>
    </div>
    <button @click="resetGame">Reset Game</button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      boardState: [],
      currentPlayer: "",
      message: "",
    };
  },
  methods: {
    startGame() {
      axios.get("http://localhost:5000/api/start")
          .then((res) => {
            console.log("Start Game Response:", res.data);  // Logowanie odpowiedzi
            this.boardState = res.data.state;
            this.currentPlayer = res.data.current_player;
            this.message = res.data.message;
          })
          .catch((err) => {
            console.error(err);
          });
    },
    makeMove(row, col) {
      const moveData = {row, col};
      axios.post("http://localhost:5000/api/move", moveData)
          .then((res) => {
            console.log("Make Move Response:", res.data);  // Logowanie odpowiedzi
            this.boardState = res.data.state;
            this.currentPlayer = res.data.current_player;
            this.message = res.data.message;
          })
          .catch((err) => {
            console.error(err);
          });
    },
    resetGame() {
      axios.get("http://localhost:5000/api/reset")
          .then((res) => {
            console.log("Reset Game Response:", res.data);  // Logowanie odpowiedzi
            this.boardState = res.data.state;
            this.currentPlayer = res.data.current_player;
            this.message = res.data.message;
          })
          .catch((err) => {
            console.error(err);
          });
    },
  },
  created() {
    this.resetGame();
  },
  render_board() {

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

.board button {
  width: 100px;
  height: 100px;
  /* Możesz dodać dodatkowe style tutaj */
}
</style>