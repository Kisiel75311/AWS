// playwright.config.js
const config = {
  use: {
    browserName: 'firefox', // Ustawienie Firefoxa jako przeglądarki
    headless: false, // Uruchomienie w trybie głowicznym
    // Możesz także określić inne opcje, takie jak rozmiar okna przeglądarki itp.
  },
  // Tutaj możesz dodać więcej ustawień konfiguracyjnych, jeśli są potrzebne
};

module.exports = config;
