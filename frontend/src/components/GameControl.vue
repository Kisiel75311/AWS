<!--frontend/src/components/GameControl.vue-->
<template>
  <div class="game-control">
    <button @click="startGame">Start New Game</button>
    <button @click="resetGame">Reset Game</button>
  </div>
</template>

<template>
  <div class="game-control">
    <button @click="startGame">Start New Game</button>
    <button @click="resetGame">Reset Game</button>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'GameControl',
  methods: {
    startGame() {
      this.$emit('startGame');
    },
    resetGame() {
      this.$emit('resetGame');
    }
  }
};
</script>

<style>
.game-control {
  /* Stylowanie przycisków */
}
</style>

