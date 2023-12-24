const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      "/api": {
        target: "http://localhost:5000", // Poprawny adres URL
        changeOrigin: true,
        pathRewrite: { "^/api": "" }
      }
    }
  }
});
