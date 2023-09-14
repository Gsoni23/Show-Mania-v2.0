<template>
    <div class="bookings-page">
      <h1 class="bookings-heading">My Bookings</h1>
      <div v-if="bookings.length > 0" class="bookings-list">
        <div v-for="booking in bookings" :key="booking.booking_id" class="booking-card">
          <h3 class="booking-show-name">{{ booking.show_name }}</h3>
          <p class="booking-venue">Venue: {{ booking.venue_name }} - {{ booking.venue_location }}</p>
          <p class="booking-timings">Show Timings: {{ booking.start_time }} - {{ booking.end_time }}</p>
          <p class="booking-rating">Rating: {{ booking.rating }}/5</p>
          <p class="booking-tickets">Number of Tickets: {{ booking.tickets }}</p>
        </div>
      </div>
      <div v-else class="no-bookings">
        <p>No bookings found.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import axios from 'axios';
  import store from '../store';
  
  const bookings = ref([]);
  
  onMounted(async () => {
    try {
      // Fetch the user's bookings from the backend API
      const token = store.state.token;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const response = await axios.get('http://127.0.0.1:5000/bookings');
  
      // Set the bookings data to the response data
      bookings.value = response.data.bookings;
    } catch (error) {
      console.error('Error fetching bookings:', error);
    }
  });
  </script>
  
  <style>
  .bookings-page {
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .bookings-heading {
    font-size: 24px;
    margin-bottom: 20px;
    color: #333;
  }
  
  .bookings-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
  
  .booking-card {
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  
  .booking-show-name {
    font-size: 18px;
    font-weight: bold;
    color: #333;
  }
  
  .booking-venue {
    font-size: 14px;
    color: #666;
  }
  
  .booking-timings {
    font-size: 14px;
    color: #666;
  }
  
  .booking-rating {
    font-size: 14px;
    color: #666;
  }
  
  .booking-tickets {
    font-size: 14px;
    color: #666;
  }
  
  .no-bookings {
    text-align: center;
    color: #666;
  }
  </style>
  