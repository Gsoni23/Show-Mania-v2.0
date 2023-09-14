<template>
    <div class="booking-page">
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <h2>{{ show_name }}</h2>
      <p class="price">Price per ticket: ${{ show_price }}</p>
      <div class="input-group">
        <label for="tickets">No. of Tickets:</label>
        <input
          type="number"
          id="tickets"
          v-model="tickets"
          min="1"
          :max="100"
        />
      </div>
      <p class="total">Total Amount: ${{ TotalAmount }}</p>
      <button @click="bookTickets">Book Now</button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, computed } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';

  const route = useRouter();
  const venue_id = route.currentRoute.value.params.venue_id;
  const show_id = route.currentRoute.value.params.show_id;
  const show_name = route.currentRoute.value.params.show_name;
  const show_price = route.currentRoute.value.params.show_price;

  const tickets = ref(1);
  let errorMessage = ref('');

  const TotalAmount = computed(() => {
  return show_price * tickets.value;
  });

  async function bookTickets() {
    try {
      const token = store.state.token;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const response = await axios.post('http://127.0.0.1:5000/bookings', {
        show_id: show_id,
        venue_id: venue_id,
        tickets: tickets.value,
      });
      
      // Handle success and show feedback to the user
      console.log(response.data.message);
      route.push('/dashboard');
    } catch (error) {
      if (error.response && error.response.status === 403) {
          errorMessage.value = error.response.data.message;
        } 
        else {
        // Handle other types of errors (network errors, server errors, etc.)
        errorMessage.value = 'An error occurred during ticket booking. Please try again later.';
        console.error(error);}
    }
  }
  
  </script>
  
  <style>
  .booking-page {
    max-width: 4000px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f1f1f1;
    border-radius: 4px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .booking-page h2 {
    font-size: 20px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }
  
  .booking-page .price {
    font-size: 14px;
    color: #555;
  }
  
  .booking-page .input-group {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .booking-page .input-group label {
    margin-right: 10px;
    font-size: 14px;
    color: #333;
  }
  
  .booking-page .input-group input {
    width: 50px;
    padding: 5px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .booking-page .total {
    font-size: 14px;
    color: #555;
    margin-bottom: 10px;
  }
  
  .booking-page button {
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 4px;
    cursor: pointer;
    background-color: #FF5722;
    color: #fff;
    border: none;
  }
  
  .booking-page button:hover {
    filter: brightness(85%);
  }
  </style>
  