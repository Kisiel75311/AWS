<!--frontend/src/app.vue-->
<template>
  <div id="app">
    <Game />
  </div>
</template>

<script>
import Game from './components/GameBoard.vue';

export default {
  name: 'App',
  components: {
    Game,
  },
};
</script>
