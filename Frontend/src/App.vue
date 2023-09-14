<script setup>
import { RouterLink, RouterView } from 'vue-router'
import store from './store';
import router from './router';
import { computed } from 'vue';

async function handleLogout() {
  await store.dispatch('logout');
  router.push('/'); // Redirect to home page after logout
}


const isLoggedIn = computed(() => {
  return store.state.token;
});


</script>

<template>
  <head>
    <title>Show-Mania - Your Ultimate Entertainment Destination</title>
  </head>
  <body>
    <header>
      <nav>
        <div class="logo">
          <h1>Show-Mania</h1>
        </div>
        <ul class="nav-links">
          <li><router-link v-if="!isLoggedIn" to="/">Home</router-link></li>
          <li><router-link v-if="!isLoggedIn" to="/login">Login</router-link></li>
          <li><router-link v-if="!isLoggedIn" to="/signup">Signup</router-link></li>
          <li><router-link v-if="isLoggedIn" to="/" @click="handleLogout">Logout</router-link></li>
          <li><router-link v-if="isLoggedIn && !store.state.user[1]" to="/bookings">Bookings</router-link></li>

          
        </ul>
      </nav>
      
      <div class="hero">
        <h2>Welcome to Show-Mania</h2>
        <p>Discover the best shows, book your tickets, and enjoy unforgettable experiences.</p>
      </div>
    </header>
    <RouterView />
    
    <footer>
      <div class="container">
        <p>&copy; 2023 Show-Mania. All rights reserved.</p>
      </div>
    </footer>
  </body>
  
</template>

<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Header Styles */
header {
  background-color: #222;
  color: #fff;
  padding: 20px;
}

.logo h1 {
  margin: 0;
}

.nav-links {
  list-style: none;
  padding: 0;
  display: flex;
}

.nav-links li {
  margin-right: 20px;
}

.nav-links li a {
  color: #fff;
  text-decoration: none;
}

.hero {
  text-align: center;
  padding: 50px 0;
}

.hero h2 {
  margin-top: 0;
}

.cta-btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #FF5722;
  color: #fff;
  text-decoration: none;
  border-radius: 4px;
}

.btn:hover {
  filter: brightness(85%);
}



/* Footer Styles */
footer {
  background-color: #222;
  color: #fff;
  padding: 20px 0;
  text-align: center;
}

</style>