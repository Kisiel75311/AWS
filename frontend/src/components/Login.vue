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
      axios.post('/auth/login', {
        username: this.username,
        password: this.password
      })
          .then(response => {
            // Zapisanie tokenu JWT do localStorage
            localStorage.setItem('jwtToken', response.data.token);

            // Możesz tutaj dodać przekierowanie lub inną logikę po zalogowaniu
            this.$router.push('/game'); // Przekierowanie do komponentu gry, jeśli jest dostępne
          })
          .catch(error => {
            console.error(error);
            if (error.response && error.response.data) {
              alert(error.response.data.error);
            }
          });
    }
  }
};
</script>
