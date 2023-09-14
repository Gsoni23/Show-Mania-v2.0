<!-- views/Login.vue -->
<template>
  <div>
    <form @submit.prevent="handleLogin" class="login-form">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

      <h2>Login</h2>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="email" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit" class="btn btn-login">Login</button>
    </form>
  </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';
  
  const email = ref('');
  const password = ref('');
  let errorMessage = ref('');
  
  const router = useRouter();
  
 
async function handleLogin() {
  try {
    const response = await axios.post('http://127.0.0.1:5000/login', { email: email.value, password: password.value });
    console.log(response.data.token);
    store.commit('setToken', response.data.token);
    store.commit('setUser', [response.data.user_id, response.data.isadmin]);

    router.push('/dashboard');
  } catch (error) {
    if (error.response && error.response.status === 401) {
          errorMessage.value = error.response.data.message;
        } 
        else {
        // Handle other types of errors (network errors, server errors, etc.)
        errorMessage.value = 'An error occurred during login. Please try again later.';
        console.error(error);} 
  }
}

</script>
<style>
.error-message {
  color: #dc3545;
  font-size: 16px;
  font-weight: bold;
  padding: 10px;
  background-color: #f8d7da;
  border-radius: 4px;
  text-align: center;
}

.login-form {
  max-width: 4000px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f1f1f1;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-weight: bold;
}
.form-group input {
  width: 50%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn-login {
  width: 10%;
  padding: 10px;
  background-color: #FF5722;
  color: #fff;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>