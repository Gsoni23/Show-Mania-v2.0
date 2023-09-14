<template>
    <div>
      <form @submit.prevent="handleSubmit" class="add-venue-form">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <h2>Add New Venue</h2>
        <div class="form-group">
          <label for="venue_name">Venue Name:</label>
          <input type="text" id="venue_name" v-model="venue_name" required>
        </div>
        <div class="form-group">
          <label for="place">Place:</label>
          <input type="text" id="place" v-model="place" required>
        </div>
        <div class="form-group">
          <label for="capacity">Capacity:</label>
          <input type="number" id="capacity" v-model="capacity" required>
        </div>
        <button type="submit" class="btn-addvenue">Add Venue</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  
  const venue_name = ref('');
  const place = ref('');
  const capacity = ref('');
  let errorMessage = ref('');

  const router = useRouter();
  
  async function handleSubmit() {
    try {
      const response = await axios.post('http://127.0.0.1:5000/venue', {
        venue_name: venue_name.value,
        place: place.value,
        capacity: capacity.value,
      });
      // Handle success and show feedback to the user (e.g., toast message)
      console.log('Venue created:', response.data);
      router.push('/dashboard'); // Redirect to admin dashboard after successful creation
    } catch (error) {
      // Handle error and show feedback to the user (e.g., toast message)
      errorMessage.value = 'An error occurred during venue creation. Please try again later.';
      console.error(error);
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

.add-venue-form {
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

.btn-addvenue {
  width: 10%;
  padding: 10px;
  background-color: #FF5722;
  color: #fff;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-addvenue:hover {
    filter: brightness(85%);
  }
</style>
  