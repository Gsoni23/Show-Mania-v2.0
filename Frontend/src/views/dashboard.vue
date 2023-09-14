<template>
  <div >
    <section class="dashboard-container">
      
      <h2>Welcome, {{ user.name }}</h2>
      <!-- Show the admin dashboard if the user is an admin -->
      <div v-if="user && user.isadmin">
        <h1 class="dashboard-heading">Admin Dashboard</h1>
        <router-link to="/add-venue" class="btn-add-venue">Add New Venue</router-link>

        <br>

        <div class="dashboard-box">
          <div v-for="venue in user.venues" :key="venue.venue_id" class="venue-card">
            <h3>{{ venue.venue_name }}</h3>
            <div class="venue-buttons">
              <router-link :to="{ name: 'Edit_venue', params: { id: venue.venue_id }}" class="btn btn-edit">Edit</router-link>
              <button @click="deleteVenue(venue.venue_id)" class="btn btn-delete">Delete</button>
              <router-link :to="{ name: 'Show_add', params: { id: venue.venue_id }}" class="btn btn-add-show">Add New Show</router-link>
              <button @click="exportVenue(venue.venue_id)" class="btn btn-export">Export</button>

            </div>

            <hr class="dashboard-divider" />

            <div class="show-list">
              <div v-for="show in venue.shows" :key="show.show_id" class="dashboard-show-card">
                <h4>{{ show.show_name }}</h4>
                <router-link :to="{ name: 'Show_action', params: { id: show.show_id }}" class="btn btn-action">Actions</router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
            
      <!-- Show the user dashboard if the user is a normal user -->
      <div v-else-if="user && !user.isadmin">
        <h1 class="dashboard-heading">User Dashboard</h1>

        <div class="search-container">
          <input v-model="searchQuery" @input="performSearch(searchQuery)" type="text"
          placeholder="Search movies by rating, tags or movie name" class = "search-input" />
          <div v-if="searchQuery !== '' " class="search-results">
            <div v-for="result in searchResults" :key="result.show_id" class="search-result">
              <h3>{{ result.show_name }}</h3>
              <p class="movie-info">Rating: {{ result.rating }}/5</p>
              <p class="movie-info">Tags: {{ result.tags }}</p>
              <router-link :to="{ name: 'book_show', params: { show_id: result.show_id, show_name: result.show_name, show_price: result.price, venue_id: result.venue_id}}"> <button class="movie-card-booking" >Book Now</button> </router-link>

            </div>
          </div>
        </div>

      <div class="hall-list">
        <div v-for="venue in user.venues" :key="venue.venue_id" class="hall-box">
          <h2>{{ venue.venue_name }}</h2>
          <p class="hall-location">{{ venue.place }}</p>
          <div class="movie-list">
            <div v-for="show in venue.shows" :key="show.show_id" class="movie-card">
              <h3>{{ show.show_name }}</h3>
              <p class="movie-time">{{ show.start_time }} - {{ show.end_time }}</p>
              <p class="seats">Available Seats: {{ venue.capacity - show.booked_tickets }}</p>
              <p class="price">Price: ${{ show.price }}</p>
              <p class="tags">Tags: {{ show.tags }}</p>
              <p class="rating">Rating: {{ show.rating }}/5</p>
              <router-link :to="{ name: 'book_show', params: { show_id: show.show_id, show_name: show.show_name, show_price: show.price, venue_id: venue.venue_id}}"> <button class="movie-card-booking" :disabled="venue.capacity - show.booked_tickets === 0">Book Now</button> </router-link>

            </div>
          </div>
        </div>
      </div>
      </div>
    </section>
  </div>
</template>

  
<script setup>
import axios from "axios";
import store from "../store";
import router from "../router";

import { ref, onMounted } from "vue";



const errorMessage = ref("");
const searchQuery = ref("");
const searchResults = ref("");


const user = ref("");

const fetchData = async () => {
  try{

    const token = store.state.token;
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    const response = await axios.get("http://127.0.0.1:5000/home");

    user.value = response.data;
  }
  catch (error) {
    errorMessage.value = "An error occurred during user fetch. Please try again later.";
    console.error(error);
  }
};

onMounted(() => {
  // Call the function to fetch the user data when the component is mounted
  fetchData();
  
});



async function deleteVenue(venue_id) {

      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.delete(`http://127.0.0.1:5000/venue`, {params: {venue_id: venue_id}});
  
        // Handle success and show feedback to the user
        console.log(response.data.message);
        fetchData();
      } 
      catch (error) {
        // Handle error and show feedback to the user (e.g., toast message)
        errorMessage.value = 'An error occurred during venue deletion. Please try again later.';
        console.error(error);
      }
    }

async function exportVenue(venue_id) {

      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const response = await axios.get(`http://127.0.0.1:5000/export`, {params: {venue_id: venue_id}});
  
        // Handle success and show feedback to the user
        console.log(response.data.message);
        fetchData();
      } 
      catch (error) {
        // Handle error and show feedback to the user (e.g., toast message)
        errorMessage.value = 'An error occurred during venue export. Please try again later.';
        console.error(error);
      }
    }

async function performSearch(searchQuery){
  
    try {
      const token = store.state.token;
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      const response = await axios.get(`http://127.0.0.1:5000/search`, {params: {searchQuery: searchQuery}});

      searchResults.value = response.data.shows;

    } catch (error) {
      errorMessage.value = 'An error occurred during search. Please try again later.';
      console.error("Error performing search:", error);
      
      
    }
};
</script>

<style>

.dashboard-container {
  text-align: center;
  padding: 20px;
}

.dashboard-heading {
  font-size: 30px;
  margin-bottom: 20px;
  color: #333;
}

.dashboard-box {
  background-color: #f1f1f1;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.venue-card {
  margin: 20px 0;
}

.venue-buttons {
  margin-bottom: 10px;
}

.btn {
  padding: 10px 20px;
  font-size: 16px;
  border-radius: 6px;
  cursor: pointer;
  margin: 0 5px;
  border: none;
  color: #fff;
}

.btn-edit {
  background-color: #007bff;
}

.btn-delete {
  background-color: #dc3545;
}
.btn-export {
  background-color: #FF5722;
}

.btn-add-show {
  background-color: #28a745;
}

.dashboard-divider {
  border: 1px solid #ccc;
  margin: 20px 0;
}


.show-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}


.dashboard-show-card {
  width: calc(15% - 10px);
  padding: 10px;
  background-color: #cecdcd;
  border-radius: 6px;
  margin-bottom: 5px;
}

.dashboard-show-card h4 {
  margin: 0;
  color: #333;
}

.btn-action {
  background-color: #007bff;
}


.btn-add-venue {
  color: #fff;
  border: none;
  font-size: 16px;

  margin-bottom: 10px;
  cursor: pointer;
  display: inline-block;
  padding: 10px 20px;
  background-color: #FF5722;
  text-decoration: none;
  border-radius: 4px;
}
.btn-add-venue:hover {
  filter: brightness(85%);
}

.hall-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.hall-box {
  background-color: #f1f1f1;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 300px;
}

.hall-box h2 {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.hall-box .hall-location {
  color: #555;
}

.movie-list {
  margin-top: 20px;
}

.movie-card {
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.movie-card h3 {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.movie-card .movie-time {
  font-size: 14px;
  color: #555;
}

.movie-card .seats,
.movie-card .price,
.movie-card .tags,
.movie-card .rating {
  font-size: 12px;
  color: #777;
}

.movie-card-booking {
  padding: 8px 16px;
  font-size: 14px;
  border-radius: 4px;
  cursor: pointer;
  background-color: #FF5722;
  color: #fff;
  border: none;
  text-decoration: none;
}

.movie-card-booking:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.movie-card-booking:hover {
  filter: brightness(85%);
}
.search-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.search-results {
  margin-top: 10px;
}

.search-result {
  background-color: #f1f1f1;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.search-result h3 {
  margin: 0;
  color: #333;
}

.movie-info {
  margin: 5px 0;
  font-size: 14px;
  color: #777;
}

.no-results {
  margin-top: 10px;
  color: #FF5722;
}

.book-button {
  background-color: #FF5722;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  margin-top: 5px;
}

.book-button:hover {
  filter: brightness(85%);
}
</style>
