<template>
  <router-view />
</template>

<script setup>
// App.vue acts as the layout root. 
// Routing is handled by vue-router in /src/router/index.js
</script>

<style>
/* Global Resets if needed, though clean-css handles most */
html, body, #app {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* Prevent horizontal scroll */
  background: #030303; /* Obsidian Black - consistent with design */
}

body {
  overflow-y: auto; /* Allow vertical scroll for landing/login pages */
}

#app {
  overflow: visible; /* Let child components manage their own overflow */
}
</style>
