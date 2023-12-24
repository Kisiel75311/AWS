<!--frontend/src/components/GameBoard.vue-->
<template>
  <div class="game-board">
    <div v-for="(row, rowIndex) in board" :key="rowIndex" class="board-row">
      <button v-for="(cell, colIndex) in row" :key="colIndex" @click="makeMove(rowIndex, colIndex)">
        {{ cell }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'GameBoard',
  props: ['board'],
  methods: {
    makeMove(row, col) {
      this.$emit('makeMove', row, col);
    }
  }
};
</script>

<style>
.game-board {
  /* Stylowanie planszy gry */
}
.board-row {
  /* Stylowanie wiersza planszy */
}
</style>
