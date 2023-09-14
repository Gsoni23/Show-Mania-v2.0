<template>
    <div>
      <form @submit.prevent="updateVenue" class="add-venue-form">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <h2>Edit Venue</h2>
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
        <button type="submit" class="btn-addvenue">Update</button>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';
  
  const venue_name = ref('');
  const place = ref('');
  const capacity = ref('');
  let errorMessage = ref('');

  const route = useRouter();
  const venue_id = route.currentRoute.value.params.id;

  
// Fetch the show details from the backend API when the component is mounted
onMounted(async () => {
      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get('http://127.0.0.1:5000/venue', {params : {venue_id:venue_id}});
        venue_name.value = response.data.venue_name;
        place.value = response.data.place;
        capacity.value = response.data.capacity;

        console.log(response.data);

      } catch (error) {
        console.error(error);
        
      }
    });
  
async function updateVenue() {
      try {

        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.patch('http://127.0.0.1:5000/venue', {
            venue_name: venue_name.value,
            place: place.value,
            capacity: capacity.value,
        }, {
          params: {
            venue_id: venue_id
          }
        });
  
  
        // Handle success and show feedback to the user
        console.log(response.data.message);
        route.push('/dashboard');
      } catch (error) {
        errorMessage.value = 'An error occurred during venue updation. Please try again later.';
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
  