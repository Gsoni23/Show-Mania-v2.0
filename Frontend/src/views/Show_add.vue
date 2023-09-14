<template>
    <div>
      <form @submit.prevent="handleSubmit" class="add-show-form">
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <h2>Add New Show</h2>
          <div class="form-group">
            <label for="show_name">Show Name:</label>
            <input type="text" id="show_name" v-model="show_name" required>
          </div>
          <div class="form-group">
            <label for="rating">Rating:</label>
            <input type="number" id="rating" v-model="rating" required>
          </div>
          <div class="form-group">
            <label for="start_time">Start Time:</label>
            <input type="time" id="start_time" v-model="start_time" required>
          </div>
          <div class="form-group">
            <label for="end_time">End Time:</label>
            <input type="time" id="end_time" v-model="end_time" required>
          </div>
          <div class="form-group">
            <label for="tags">Tags:</label>
            <input type="text" id="tags" v-model="tags" required>
          </div>
          <div class="form-group">
            <label for="price">Ticket Price:</label>
            <input type="number" id="price" v-model="price" required>
          </div>
        <button type="submit" class="btn-addshow">Add Show</button>
      </form>
    </div>
</template>

<script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useRouter } from 'vue-router';
  import store from '../store';
  
  const route = useRouter();

  const show_name = ref('');
  const rating = ref('');
  const start_time = ref('');
  const end_time = ref('');
  const tags = ref('');
  const price = ref('');

  const venue_id = route.currentRoute.value.params.id;
  
  let errorMessage = ref('');

  
  
  async function handleSubmit() {
    try {
        const token = store.state.token;
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        const response = await axios.post('http://127.0.0.1:5000/show', {
        show_name: show_name.value,
        rating: rating.value,
        venue_id: venue_id,
        start_time: start_time.value,
        end_time: end_time.value,
        tags: tags.value,
        price: price.value,
      });
      // Handle success and show feedback to the user

      console.log(response.data.message);
      route.push('/dashboard');

    } catch (error) {
      // Handle error and show feedback to the user (e.g., toast message)
      errorMessage.value = 'An error occurred during show creation. Please try again later.';
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

.add-show-form {
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

.btn-addshow {
  width: 10%;
  padding: 10px;
  background-color: #FF5722;
  color: #fff;
  text-align: center;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-addshow:hover {
    filter: brightness(85%);
  }
</style>
  