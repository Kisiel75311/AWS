<!--frontend/src/Login.vue-->
<template>
  <div>
    <form @submit.prevent="login">
      <!-- Pola formularza logowania -->
      <input v-model="username" type="text" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    login() {
      // Wywołanie API do logowania
      axios.post('/auth/login', {
        username: this.username,
        password: this.password
      })
      .then(response => {
        // Obsługa odpowiedzi, np. zapisanie tokenu
      })
      .catch(error => {
        console.error(error);
      });
    }
  }
};
</script>
