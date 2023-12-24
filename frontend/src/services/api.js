// frontend/src/services/api.js
// src/services/api.js

import axios from 'axios';

const API_URL = '10.0.1.2:8080';

export default {
  startGame() {
    return axios.get(`${API_URL}/game/start`);
  },
  makeMove(row, col) {
    return axios.post(`${API_URL}/game/move`, { row, col });
  },
  resetGame() {
    return axios.get(`${API_URL}/game/reset`);
  }
};
