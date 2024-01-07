<!--LoginComponent.vue-->
<template>
  <div class="login-container">
    <h1>Logowanie</h1>
    <form @submit.prevent="loginUser">
      <div>
        <label for="username">Nazwa użytkownika:</label>
        <input type="text" id="username" v-model="username">
      </div>
      <div>
        <label for="password">Hasło:</label>
        <input type="password" id="password" v-model="password">
      </div>
      <button type="submit">Zaloguj się</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async loginUser() {
      // logika logowania...
      axios.post('/auth/login', {
        username: this.username,
        password: this.password
      })
          .then(response => {
            // Zapisanie tokenu JWT do localStorage
            localStorage.setItem('jwtToken', response.data.token);
            // Wyświetlenie powiadomienia o sukcesie
            this.errorMessage = 'Pomyślnie zalogowano. Przekierowywanie...';

            // Przekierowanie do widoku /game po 1 sekundzie
            setTimeout(() => {
              this.$router.push('/game');
            }, 1000);

          })
          .catch(err => {
            this.handleError(err);
          });
    },
    handleError(err) {
      if (err.response) {
        // Błąd odpowiedzi HTTP inny niż 2xx
        this.errorMessage = err.response.data.error || 'Wystąpił błąd serwera.';
      } else if (err.request) {
        // Żądanie zostało wysłane, ale nie otrzymano odpowiedzi
        this.errorMessage = 'Brak odpowiedzi z serwera.';
      } else {
        // Coś poszło nie tak przy tworzeniu żądania
        this.errorMessage = 'Błąd podczas wysyłania żądania.';
      }
    }
  }
};
</script>

<style>
.login-container {
  /* Style według preferencji */
}
</style>
