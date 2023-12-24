<!--frontend/src/components/GameStatus.vue-->
<template>
  <div class="game-status">
    <p>{{ statusMessage }}</p>
  </div>
</template>

<script>
export default {
  name: 'GameStatus',
  props: ['statusMessage']
};
</script>

<style>
.game-status {
  /* Stylowanie statusu gry */
}
</style>
